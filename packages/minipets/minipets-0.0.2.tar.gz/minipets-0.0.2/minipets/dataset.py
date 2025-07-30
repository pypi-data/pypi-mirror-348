"""
dataset.py
- load sn, lightcurve and spectra data from different input formats
- flag data rejected by light dr2 cuts (no time grid computations)
"""
import logging
import pathlib
import numpy as np
import pickle
import pandas as pd

from lemaitre import bandpasses

from nacl.models import salt2
from nacl import TrainingDataset
from nacl.models.salt2 import SALT2Like

from .utils import make_sne_nacl, make_lc_nacl

logger = logging.getLogger(__name__)


bandpass_convert = {
    'MEGACAMPSF::g': 'megacam6::g',
    'MEGACAMPSF::r': 'megacam6::r',
    'MEGACAMPSF::y': 'megacam6::i2',
    'MEGACAMPSF::z': 'megacam6::z',
    'MEGACAMPSF::i': 'megacam6::i',
    'MEGACAM6::g': 'megacam6::g',
    'MEGACAM6::r': 'megacam6::r',
    'MEGACAM6::i2': 'megacam6::i2',
    'MEGACAM6::z': 'megacam6::z',
    'MEGACAM6::i': 'megacam6::i',
    'hsc::y': 'hsc::Y',
    'ztfr':'ztf::r',
    'ztfg':'ztf::g',
    'ztfi':'ztf::I',
    'ztf::i':'ztf::I'

}


class PerDataFrameIndexProxy:

    def __init__(self, parent, df_name):
        self._parent = parent
        self._df_name = df_name

    def __getattr__(self, attr):

        # sn_index, band_index etc ...
        if attr in self._parent._index_sources:
            return self._get_index_column(attr)

        # sn_set, sn_map etc.
        if attr.endswith('_set') or attr.endswith('_map'):
            base = attr.removesuffix('_set').removesuffix('_map')
            index_name = f"{base}_index"

            # ensure the index exists
            self._get_index_column(index_name)

            if attr.endswith("_set"):
                return getattr(self._parent, f"{index_name}_uniques")
            else:
                return getattr(self._parent, f"{index_name}_mapping")

        raise AttributeError(f"No such attribute: {attr}")

    def _get_index_column(self, index_name):
        """
        """
        df = getattr(self._parent, self._df_name)
        df_cache = self._parent._index_df.setdefault(self._df_name, pd.DataFrame(index=df.index))

        if index_name not in df_cache.columns:
            self._parent._create_index(index_name)

        return df_cache[index_name]


class IndexesAccessor:

    def __init__(self, parent):
        self._parent = parent

    def __getattr__(self, df_name):
        if not hasattr(self._parent, df_name):
            raise AttributeError(f"no dataframe named '{df_name}' in parent.")
        return PerDataFrameIndexProxy(self._parent, df_name)



class Dataset:
    """Containers for sn, spec and light curves data, compatible with nacl data
    format, and on which cut can be applied.
    """

    def __init__(self, sn_data=None, lc_data=None, spec_data=None, **kwargs):

        self._sn = kwargs.get('sn_path')
        self._lc = kwargs.get('lc_path')
        self._spec = kwargs.get('spec_path')

        self._sn = pathlib.Path(self._sn) if self._sn is not None else None
        self._lc = pathlib.Path(self._lc) if self._lc is not None else None
        self._spec = pathlib.Path(self._spec) if self._spec is not None else None

        flib = bandpasses.get_filterlib()  # Initialise filters
        self._flib = kwargs.get("filterlib", flib)
        self.logger = kwargs.get("logger", logger)
        self.basis = kwargs.get("basis", None)

        self.sigma_pars = kwargs.get('sigma_pars', None)
        
        self._sn_data = sn_data
        self._lc_data = lc_data
        self._spec_data = spec_data
        self._data_cut = []

        self._index_df = {}
        self._index_sources = {
            'sn_index': [('sn_data', 'sn'), ('lc_data', 'sn')],
            'band_index': [('lc_data', 'band')],
            'lc_index': [('lc_data', 'lc')]
        }
        self.indexes = IndexesAccessor(self)

    @classmethod
    def from_nacl(cls, tds):
        sn_data = pd.DataFrame(tds.sn_data.nt)
        lc_data = pd.DataFrame(tds.lc_data.nt)
        spec_data = pd.DataFrame(tds.spec_data.nt)
        return Dataset(sn_data=sn_data,
                       lc_data=lc_data,
                       spec_data=spec_data,
                       basis=tds.basis,
                       flib=tds.filterlib)

    @property
    def sn_data(self):
        if self._sn_data is None and self._sn is not None:
            self._sn_data = pd.read_parquet(self._sn)
            self._hack_sn_format()
        return self._sn_data

    @property
    def lc_data(self):
        if self._lc_data is None and self._lc is not None:
            self._lc_data = pd.read_parquet(self._lc)
            self._hack_lc_format()
        return self._lc_data

    @property
    def spec_data(self):
        if self._spec_data is None and self._spec is not None:
            self._spec_data = pd.read_parquet(self._spec)
            self._hack_spec_format()
        return self._spec_data

    @property
    def bands(self):
        return self.lc_data.band.unique()

    @property
    def sne(self):
        return self.sn_data.sn.unique()

    def _hack_lc_format(self):
        pass

    def _hack_sn_format(self):
        pass

    def _hack_spec_format(self):
        pass

    def _create_index(self, index_name):
        """
        create `saltworks.DataProxy`-like indexes
        """
        sources = self._index_sources[index_name]
        values = []

        for df_name, col_name in sources:
            df = getattr(self, df_name)
            values.append(df[col_name])

        all_values = pd.concat(values).unique()
        index_array, uniques_array = pd.factorize(all_values)
        mapping = dict(zip(uniques_array, index_array))

        setattr(self, f"{index_name}_mapping", mapping)
        setattr(self, f"{index_name}_uniques", uniques_array)

        for df_name, col_name in sources:
            df = getattr(self, df_name)
            df_index = df.index
            cache = self._index_df.setdefault(df_name, pd.DataFrame(index=df.index))
            cache[index_name] = df[col_name].map(mapping)

    def get_tds(self):
        """ Return a NaCl training dataset
        """
        sn_data = self.sn_data.to_records(index=False)
        lc_data = self.lc_data.to_records(index=False)
        spec_data = self.spec_data.to_records(index=False)

        return TrainingDataset(sne=sn_data,
                               lc_data=lc_data,
                               spec_data=spec_data,
                               basis=self.basis,
                               filterlib=self._flib)

    def dr2_like_cuts(self, **kw):
        """ Cuts defined by ZTF DR2

        Parameters
        ----------
        n_bands_min: min number of bands for a SN, default 2
        n_points_min: min number of points for a SN, default 5
        n_points_before: min number of points before tmax, default 2
        n_points_after: min number of points after tmax, default 2
        c_min: min color, default -0.2
        c_max: max color, default 0.8
        abs_x1_max: max absolute value of x1, default 3
        """
        self._at_least_n_bands(n_bands_min=kw.get('n_bands_min', 2))
        self._at_least_n_points(kw.get('n_points_min', 5),
                                within=kw.get('n_points_within'))
        self._at_least_n_points(kw.get('n_points_before', 2),
                                before_max=True, within=kw.get('n_points_within'))
        self._at_least_n_points(kw.get('n_points_after', 2), after_max=True,
                                within=kw.get('n_points_within'))
        self._param_range(c_min=kw.get("c_min", -0.2),
                          c_max=kw.get("c_max", 0.8),
                          abs_x1_max=kw.get("abs_x1_max", 3))

        # additional cuts based on the PeTS or NaCl SN parameter uncertainties
        self._sigma_param_below('x1', maxval=kw.get('max_sigma_x1', 1.))
        self._sigma_param_below('c', maxval=kw.get('max_sigma_c', 0.1))
        self._sigma_param_below('tmax', maxval=kw.get('max_sigma_tmax', 1.))
        # Don't know how to implement the fitprob cut

        cut_info = {
            'snname': self.sn_data.sn[self.sn_data.valid==1].tolist(),
            'N_tot': sum(self.sn_data.valid==1) ,
            'SN_cut': self.sn_data.sn[self.sn_data.valid==0].tolist(),
            'N_cut': sum(self.sn_data.valid==0),
            'cut': 'dr2 like cut'
        }
        self._data_cut.append(cut_info)
        return pd.DataFrame(self._data_cut)

    def minz_survey(self, survey, z_min):
        """ Cut SN with redshift below z_min for a given survey
        """
        killed_sne = (self.sn_data["survey"] == survey) & (self.sn_data["z"]<z_min)
        self.logger.info(f'{killed_sne.sum()} SNe killed from {survey} '
                         f'because out of range in z (z<{z_min})')
        self.logger.info(f'SNe: {list(np.unique(self.sn_data.sn[killed_sne]))}')
        self.sn_data.valid *= (~killed_sne).astype(int)

        removed_sn= list(set(self.sn_data.sn.unique()) - set(self.sn_data.loc[~killed_sne, 'sn'].unique()))
        cut_info = {
            'snname': self.sn_data.loc[~killed_sne, 'sn'].unique().tolist(),
            'N_tot': len(self.sn_data.loc[~killed_sne, 'sn'].unique()),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),
            'cut': f'{survey}_out_range_z'
        }
        self._data_cut.append(cut_info)


    def _param_range(self, c_min=-0.2, c_max=0.8, abs_x1_max=3):
        """ Cut SN parameter out of range.
        """
        killed_sne = (self.sn_data["c"]>c_max) | (self.sn_data["c"]<c_min)
        self.logger.info(f'{killed_sne.sum()} SNe killed because out of range in color')
        self.sn_data.valid *= (~killed_sne).astype(int)

        removed_sn= list(set(self.sn_data.sn.unique()) - set(self.sn_data.loc[~killed_sne, 'sn'].unique()))
        cut_info = {
            'snname': self.sn_data.loc[~killed_sne, 'sn'].unique().tolist(),
            'N_tot': len(self.sn_data.loc[~killed_sne, 'sn'].unique()),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),
            'cut': 'out_c_range'
        }
        self._data_cut.append(cut_info)

        killed_sne = np.abs(self.sn_data["x1"])>abs_x1_max
        self.logger.info(f'{killed_sne.sum()} SNe killed because out of range in x1')
        self.sn_data.valid *= (~killed_sne).astype(int)

        removed_sn= list(set(self.sn_data.sn.unique()) - set(self.sn_data.loc[~killed_sne, 'sn'].unique()))
        cut_info = {
            'snname': self.sn_data.loc[~killed_sne, 'sn'].unique().tolist(),
            'N_tot': len(self.sn_data.loc[~killed_sne, 'sn'].unique()),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),
            'cut': 'out_x1_range'
        }
        self._data_cut.append(cut_info)

    def _sigma_param_below(self, param_name, maxval):
        """
        Cut on reconstructed parameter uncertainty
        """
        if not hasattr(self, 'sigma_pars'):
            return

        sig = self.sigma_pars[param_name]
        killed_sne = sig > maxval
        self.logger.info(f"{killed_sne.sum()} SNe killed because 'sigma_{param_name}' above {maxval}")
        self.sn_data.valid *= (~killed_sne).astype(int)

        removed_sn = list(set(self.sn_data.sn.unique()) - set(self.sn_data.loc[~killed_sne, 'sn'].unique()))
        cut_info = {
            'snname': self.sn_data.loc[~killed_sne, 'sn'].unique().tolist(),
            'N_tot': len(self.sn_data.loc[~killed_sne, 'sn'].unique()),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),
            'cut': f'sigma_{param_name}'
        }
        self._data_cut.append(cut_info)

    def _at_least_n_bands(self, n_bands_min=2):
        """ Cut SN with less than n bands.
        """
        n_bands = len(self.bands)
        n_sne = len(self.sne)

        band_index_bins = np.arange(-0.5, n_bands+0.5, 1.)
        sn_index_bins = np.arange(-0.5, n_sne+0.5, 1.)
        c, _, _ = np.histogram2d(self.indexes.lc_data.sn_index,
                                 self.indexes.lc_data.band_index,
                                 bins=(sn_index_bins, band_index_bins))
        c[c>1] = 1.
        n_bands = c.sum(axis=1)
        cut_index = np.argwhere(n_bands < n_bands_min).flatten()
        to_remove = self.indexes.sn_data.sn_set[cut_index]
        self.logger.info(f'removing {len(cut_index)} SNe with less '
                         f'than {n_bands_min} bands: {to_remove}')
        self.sn_data.loc[self.sn_data.sn.isin(to_remove), 'valid'] = 0

        cut_info = {
            'snname': self.sn_data.sn[~np.isin(self.sn_data.sn,
                                               self.indexes.sn_data.sn_set[cut_index])],
            'N_tot': sum(~np.isin(self.sn_data.sn,
                                  self.indexes.sn_data.sn_set[cut_index])),
            'SN_cut': to_remove,
            'N_cut': len(to_remove),
            'cut': 'n_bands_min'
        }
        self._data_cut.append(cut_info)

        return to_remove

    def _at_least_n_points(self, n_pts_min, before_max=False, after_max=False, within=None):
        """ Cut SN with less than n points.
        """
        # tds = self.get_tds()
        n_sne = len(self.sne)

        tmax = np.zeros(len(self.sn_data))
        tmax[self.indexes.sn_data.sn_index] = self.sn_data.tmax
        zz = np.asarray(self.sn_data.z)
        index = np.asarray(self.indexes.lc_data.sn_index)
        zz = zz[index]
        dt = (self.lc_data.mjd - tmax[self.indexes.lc_data.sn_index]).to_numpy() / (1. + zz)
        tmax_index_bins = np.arange(-50., 101., 1.)
        sn_index_bins = np.arange(-0.5, n_sne+0.5, 1.)
        if before_max and not after_max:
            idx = dt<0.
            nn = 'before'
        elif after_max and not before_max:
            idx = dt>0.
            nn = 'after'
        else:
            idx = np.ones_like(dt).astype(bool)
            nn = 'tot'
        idx &= (self.lc_data.valid > 0)
        if within:
            idx &= (dt>within[0]) & (dt<within[-1])

        c, _, _ = np.histogram2d(self.indexes.lc_data.sn_index[idx],
                                 dt[idx],
                                 bins=(sn_index_bins, tmax_index_bins))
        c[c>1.] = 1.
        n_pts = c.sum(axis=1)
        cut_index = np.argwhere(n_pts < n_pts_min).flatten()
        to_remove = self.indexes.sn_data.sn_set[cut_index]

        msg = f'removing {len(cut_index)} SNe with less than {n_pts_min} points'

        cut_info = {
            'snname': self.sn_data.sn[~np.isin(self.sn_data.sn, self.indexes.sn_data.sn_set[cut_index])],
            'N_tot': sum(~np.isin(self.sn_data.sn, self.indexes.sn_data.sn_set[cut_index])),
            'SN_cut': to_remove,
            'N_cut': len(to_remove),
            'cut': f'n_pts_min_{nn}'
        }
        self._data_cut.append(cut_info)


        if before_max and not after_max:
            msg += f' before max: {to_remove}'
        elif not before_max and after_max:
            msg += f' after max: {to_remove}'
        else:
            msg += f': {to_remove}'
        logging.info(msg)
        self.sn_data.loc[self.sn_data.sn.isin(to_remove), 'valid'] = 0
        return to_remove

    def select_sne_with_data(self):
        """Make sure that all the LC points are spectra have a counterpart in
        the sn index
        """
        # select the valid stuff only
        sn = self.sn_data[self.sn_data.valid == 1]
        lc = self.lc_data[self.lc_data.valid == 1]
        lc = lc[lc.sn.isin(sn.sn)]

        if self.spec_data is not None:
            spec = self.spec_data[self.spec_data.valid == 1]
            spec = spec[spec.sn.isin(sn.sn)]

        # reselect the sne which have light curves
        idx = sn.sn.isin(lc.sn.unique())
        sn = sn[idx]

        # and reselect the spectra and lc which correspond to these SNe
        lc = lc[lc.sn.isin(sn.sn)]
        if self.spec_data is not None:
            spec = spec[spec.sn.isin(sn.sn)]
        else:
            spec = None
        return sn, lc, spec

    def _select_sne_with_data_deprecated(self):
        """Make sure that all the LC points are spectra have a counterpart in
        the sn index

        """
        # select the valid sne only
        sn_data = self._sn_data[self._sn_data.valid == 1]

        # select the lc and spec which are valid and which correspond to the selected sne
        lc_data = self._lc_data[(self._lc_data.sn.isin(sn_data.sn)) & self._lc_data.valid == 1]
        spec_data = self._spec_data[(self._spec_data.sn.isin(sn_data.sn)) & self._spec_data.valid == 1]

        # now, re-select the supernovae which have light curves
        idx = sn_data.sn.isin(lc_data.sn.unique())
        sn_data = sn_data[idx]

        # and reselect the spectra and lc which correspond to these SNe
        spec_data = spec_data[spec_data.sn.isin(sn_data.sn)]
        lc_data = lc_data[lc_data.sn.isin(sn_data.sn)]

        return sn_data, lc_data, spec_data

    def filter_lc_data(self, **kw):
        """Filter the light curves points that are either out of range or
        don't pass minimal quality cuts

        Parameters
        ----------
        lc_phase_range : tuple (min, max), phase range in day.
               default (-50, 100)
        """
        min_phase, max_phase = kw.get('lc_phase_range',  (-50., 100.))
        ph = pd.merge(self.lc_data[['sn', 'mjd']],
                      self.sn_data[['sn', 'tmax', 'z']],
                      on='sn',
                      how='left')
        phase = (ph.mjd - ph.tmax) / (1. + ph.z)
        killed_data_points = ((phase < min_phase) | (phase > max_phase)).to_numpy()
        frac = 100. * killed_data_points.sum() / len(killed_data_points)
        self.logger.info(f'filtering {killed_data_points.sum()} photometric points'
                         f'out of phase range [{min_phase},{max_phase}] ({frac:.2f}%)')
        self.lc_data['valid'] *= (~killed_data_points).astype(int)

        removed_sn= list(set(self.lc_data.sn.unique()) - set(self.lc_data.loc[~killed_data_points, 'sn'].unique()))
        cut_info = {
            'snname': self.lc_data.loc[~killed_data_points, 'sn'].unique().tolist(),
            'N_tot': len(self.lc_data.loc[~killed_data_points, 'sn'].unique()),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),
            'cut': 'phot_phase_range'
        }
        self._data_cut.append(cut_info)


    def filter_spec_data(self, **kw):
        """Filter the spectra that are either out of range, or do no pass
        minimal quality cuts

        Parameters
        ----------
        spec_phase_range : tuple (min, max), phase range in day.
               default (-20, 100)
        spec_wavelength_range: tuple (min, max), wavelength range in A.
               default (2000, 11000)
        spec_buggy_snr_limit : float
               default 1.E10
        spec_low_snr_limit : float
               default 0.1
        """
        # spectra that are out of phase range
        min_phase, max_phase = kw.get('spec_phase_range',  (-20., 100.))
        min_wl, max_wl = kw.get('spec_wavelength_range', (2000., 11000.))
        ph = pd.merge(self.spec_data[['sn', 'mjd', 'wavelength']],
                      self.sn_data[['sn', 'tmax', 'z']],
                      on='sn',
                      how='left')
        phase = (ph.mjd - ph.tmax) / (1. + ph.z)
        killed_data_points = ((phase < min_phase) | (phase > max_phase)).to_numpy()
        frac = 100. * killed_data_points.sum() / len(killed_data_points)
        self.logger.info(f'filtering {killed_data_points.sum()} spectroscopic '
                         f'points out of phase range [{min_phase},{max_phase}] ({frac:.2f}%)')
        self.spec_data['valid'] *= (~killed_data_points).astype(int)

        removed_sn= list(set(self.spec_data.sn.unique()) - set(self.spec_data.loc[~killed_data_points, 'sn'].unique()))

        cut_info = {
            'snname': self.spec_data.loc[~killed_data_points, 'sn'].unique().tolist(),
            'N_tot': len(self.spec_data.loc[~killed_data_points, 'sn'].unique()),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),
            'cut': 'spec_phase_range'
        }
        self._data_cut.append(cut_info)
        # spectrum samples that are out of the allowed wavelength range
        wl = ph.wavelength / (1. + ph.z)
        killed_data_points = ((wl < min_wl) | (wl > max_wl)).to_numpy()
        frac = 100. * killed_data_points.sum() / len(killed_data_points)
        self.logger.info(f'filtering {killed_data_points.sum()} spectroscopic '
                         f'points out of wavelength range [{min_wl},{max_wl}] ({frac:.2f}%)')
        self.spec_data['valid'] *= (~killed_data_points).astype(int)


        removed_sn= list(set(self.spec_data.sn.unique()) - set(self.spec_data.loc[~killed_data_points, 'sn'].unique()))

        cut_info = {
            'snname': self.spec_data.loc[~killed_data_points, 'sn'].unique().tolist(),
            'N_tot': len(self.spec_data.loc[~killed_data_points, 'sn'].unique()),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),
            'cut': 'spec_wl_range'
        }
        self._data_cut.append(cut_info)


        # spectrum samples that have negative or zero uncertainties
        # samples with zero flux
        negative_or_zero_fluxerr = (self.spec_data.fluxerr <= 0.)
        self.logger.info(f'filtering {negative_or_zero_fluxerr.sum()} '
                         f'spectroscopic points with negative or zero fluxerr')
        self.logger.info(f'you may want to inspect spectra: {self.spec_data.spec[negative_or_zero_fluxerr].unique()}')
        self.spec_data['valid'] *= (~negative_or_zero_fluxerr).astype(int)

        removed_sn= self.spec_data.sn[negative_or_zero_fluxerr].unique()
        keep_sn=np.setdiff1d(np.unique(self.spec_data.sn), removed_sn)
        
        cut_info = {
            'snname': keep_sn,
            'N_tot': len(keep_sn),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),            
            'cut': 'negative_or_zero_fluxerr'  
        }
        self._data_cut.append(cut_info)


        # spectrum samples with obviously erroneous SNR
        snr = np.abs(self.spec_data.flux / self.spec_data.fluxerr)
        spec_buggy_snr_limit = float(kw.get('spec_buggy_snr_limit', 1.E10))
        buggy_snr = (snr > spec_buggy_snr_limit) | np.isinf(snr) | np.isnan(snr)
        self.logger.info(f'filtering {buggy_snr.sum()} spectroscopic '
                         f'points with obviously buggy SNR (>{spec_buggy_snr_limit})')
        self.logger.info(f'you may want to inspect spectra: {self.spec_data.spec[buggy_snr].unique()}')
        self.spec_data['valid'] *= (~buggy_snr).astype(int)

        removed_sn= self.spec_data.sn[buggy_snr].unique()
        keep_sn=np.setdiff1d(np.unique(self.spec_data.sn), removed_sn)
        
        cut_info = {
            'snname': keep_sn,
            'N_tot': len(keep_sn),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),            
            'cut': 'buggy_snr'  
        }
        self._data_cut.append(cut_info)
        
        # remove spectra with low average SNR
        snr = pd.DataFrame({'spec': self.spec_data.spec,
                            'snr': self.spec_data.flux / self.spec_data.fluxerr}
                           ).groupby('spec')['snr'].apply('median')
        self.median_spec_snr = snr
        spec_low_snr_limit = kw.get('spec_low_snr_limit', 0.1)
        self.low_snr_spectra = snr.index[(snr < spec_low_snr_limit)]
        low_snr = self.spec_data.spec.isin(self.low_snr_spectra)
        self.logger.info(f'filtering {len(self.low_snr_spectra)} spectra '
                         f'with very low snr ({spec_low_snr_limit}) '
                         f': {low_snr.sum()} points')
        self.spec_data['valid'] *= (~low_snr).astype(int)
        removed_sn= list(set(self.spec_data.sn.unique()) - set(self.spec_data.loc[~low_snr, 'sn'].unique()))
        cut_info = {
            'snname': self.spec_data.loc[~low_snr, 'sn'].unique().tolist(),
            'N_tot': len(self.spec_data.loc[~low_snr, 'sn'].unique()),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),
            'cut': 'low_snr'
        }
        self._data_cut.append(cut_info)

    def filter_sne(self, **kw):
        """Filter the supernovae that don't pass very minimal quality cuts

        Parameters
        ----------
        min_mwebv: minimum mwebv, default 0.25
        """
        # select the supernovae with a valid x0
        killed_sne = (self.sn_data.x0 == 999.) # todo: replace with nan

        removed_sn= list(set(self.sn_data.sn.unique()) - set(self.sn_data.loc[~killed_sne, 'sn'].unique()))
        cut_info = {
            'snname': self.sn_data.loc[~killed_sne, 'sn'].unique().tolist(),
            'N_tot': len(self.sn_data.loc[~killed_sne, 'sn'].unique()),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),
            'cut': 'invalid_x0'
        }
        self._data_cut.append(cut_info)

        killed_ebv = (self.sn_data.mwebv > kw.get('min_mwebv', 0.25))

        removed_sn= list(set(self.sn_data.sn.unique()) - set(self.sn_data.loc[~killed_ebv, 'sn'].unique()))
        cut_info = {
            'snname': self.sn_data.loc[~killed_ebv, 'sn'].unique().tolist(),
            'N_tot': len(self.sn_data.loc[~killed_ebv, 'sn'].unique()),
            'SN_cut': removed_sn,
            'N_cut': len(removed_sn),
            'cut': 'E(B-V)>0.25'
        }
        self._data_cut.append(cut_info)

        # discard all the supernova with an unreasonnable
        # amount of Galactic extinction
        killed_sne |= (self.sn_data.mwebv > kw.get('min_mwebv', 0.25))

        # discard all the supernovae with no valid data
        self.logger.info(f'{killed_sne.sum()} SNe killed because either x0 invalid or E(B-V)>0.25')
        self.sn_data.valid *= (~killed_sne).astype(int)

    def range_flag(self, **kw):
        """ Flag out of range as defined by keywords
        """
        cut_info = {
            'snname': self.lc_data.sn.unique().tolist(),
            'N_tot': len(self.lc_data.sn.unique()),
            'SN_cut': 'None',
            'N_cut': '0',
            'cut': 'None'
        }
        self._data_cut.append(cut_info)

        self.filter_lc_data(**kw)
        if self.spec_data is not None:
           self.filter_spec_data(**kw)

        self.filter_sne(**kw)
        if 'z_min' in kw:
           for survey, z in kw['z_min'].items():
                self.minz_survey(survey, float(z))

        cut_info = {
            'snname': self.sn_data.sn[self.sn_data.valid==1].tolist(),
            'N_tot': sum(self.sn_data.valid==1) ,
            'SN_cut': self.sn_data.sn[self.sn_data.valid==0].tolist(),
            'N_cut': sum(self.sn_data.valid==0),
            'cut': 'all range cut'
        }

        # Ajouter les données dans la liste
        self._data_cut.append(cut_info)
        return pd.DataFrame(self._data_cut)

    def flag_data(self, **kw):
        """ Flag outliers as defined by keywords.
            data_cut: summary with all the cuts
        """
        self.range_flag(**kw)
        c2 = self.dr2_like_cuts(**kw)
        return c2

    def apply_cut(self):
        """ Apply all cuts and check SN counterparts in all tables.
        """
        sn, lc, spec = self.select_sne_with_data()
        self._sn_data = sn
        self._lc_data = lc
        self._spec_data = spec

    def filter_data(self, **kw):
        """ Flag and cut.
        """
        self.flag_data(**kw)
        self.apply_cut()

class SimDataset(Dataset):
    """ Data are generated from survey logs using skysurvey.
    """

    def _hack_sn_format(self):
        self.logger.debug('_hack_sn_format')
        self._sn_data = pd.DataFrame(make_sne_nacl(self._sn_data))

    def _hack_lc_format(self):
        self.logger.debug('_hack_sn_format')
        self._lc_data = pd.DataFrame(make_lc_nacl(self._lc_data))

    def generate(
            self, logs, N=12000, tstart=56_000, tstop=60_000, nacl_flux=True, noise=True
    ):
        """From existing logs produced by skysurvey, build a dataset at the nacl format

        logs: pickle file
        N: number of snia event

        """
        import skysurvey
        # Draw SN1a
        snia = skysurvey.SNeIa()
        data = snia.draw(size=N, tstart=tstart, tstop=tstop, inplace=True)

        # Load survey
        survey = pickle.load(open(logs, "rb"))

        # Combine to make a dataset
        dset = skysurvey.dataset.DataSet.from_targets_and_survey(
            snia, survey, incl_error=False, phase_range=[-20, 50]
        )
        # Return in nacl format
        self._sn_data = data
        self._hack_sn_format()
        self._lc_data = dset.data
        self._hack_lc_format()

        if nacl_flux:
            flux = self._nacl_flux()
            self._lc_data["flux"] = flux
        if noise:
            self._lc_data["flux"] = np.random.normal(self.lc_data["flux"],
                                                     self.lc_data["fluxerr"])

    def _nacl_flux(self, dust_extinction_model=None):
        """Use NaCl salt2 like model to compute lc fluxes."""
        tds = self.get_tds()
        model = SALT2Like(tds, dust_extinction_model=dust_extinction_model)

        # Set SN param with values generated by skysurvey
        pars = model.init_pars()
        flux = model(pars)
        return flux


class MockDataset(Dataset):
    """ Data are read from official DC.
    """

    _maybe_missing_cols = [("sensor_id", 0),
                           ("x", 0.),
                           ("y", 0.),
                           ("ccd", 0),
                           ("amp", 0),
                           ("magsys", 'ab'),
                           ("mag_sky", np.nan),
                           ("seeing", np.nan),
                           ("exptime", np.nan)]

    def _hack_sn_format(self):
        """Adapt the mock sn_index structure

        The DC1 mock SN index structure (the structure that contains the SN
        names, redshift and more generally, meta data) differs a bit from what
        is expected in a TDS. This function makes what is needed (essentially
        column name reshuffling).

        .. note:
           Ideally, this function should not exist. Please update the
           upcoming mock formats so that it can be safely removed for the next
           DC's

        """
        self.logger.debug('_hack_sn_format')
        column_names = {'t0': 'tmax'}
        if 'zcmb' in self.sn_data.columns and 'z' not in self.sn_data.columns:
            column_names['zcmb'] = 'z'
        self._sn_data = self.sn_data.rename(columns=column_names)

    def _hack_lc_format(self):
        """Adapt the light curve dataframe structure

        This function standardizes the column names, ensures required fields are
        present, and converts types appropriately

        .. note:
           Ideally, this function should not exist. Please update the
           upcoming mock formats so that it can be safely removed for the next
           DC's
        """
        # we need the sn index
        sn_data = self.sn_data
        lc_data = self.lc_data

        self.logger.debug('_hack_lc_format')
        # a few column names need to be changed
        column_names = {
            "time": "mjd",
            "name": "sn",
            "rcid": "sensor_id"
        }
        self.logger.debug('_hack_lc_format: renaming columns')
        lc_data = lc_data.rename(columns={k: v
                                          for k,v in column_names.items()
                                          if k in lc_data.columns and v not in lc_data.columns})

        # some additional fields may be missing
        self.logger.debug('_hack_lc_format: adding missing fields')
        for col, default_val in MockDataset._maybe_missing_cols:
            if col not in lc_data.columns:
                lc_data[col] = default_val

        # convert data types safely
        self.logger.debug('_hack_lc_format: converting data types')
        numeric_cols = ['x', 'y']
        for col in numeric_cols:
            lc_data[col] = pd.to_numeric(lc_data[col], errors='coerce', downcast='float')

        if 'sensor_id' in lc_data.columns:
            lc_data['sensor_id'] = pd.to_numeric(lc_data['sensor_id'],
                                                 errors='coerce').astype('Int64')
        if 'rcid' in lc_data.columns:
            lc_data['rcid'] = pd.to_numeric(lc_data['rcid'],
                                            errors='coerce').astype('Int64')

        # the band names need to be slightly adapted
        self.logger.debug('_hack_lc_format: band names')
        lc_data['band'] = lc_data["band"].map(bandpass_convert).fillna(lc_data["band"])

        # build a unique name for each light curves
        self.logger.debug('_hack_lc_format: unique lc name')
        lc_data["lc"] = lc_data["sn"].astype(str) + lc_data["band"].astype(str)

        # add the sn redshift to the light curves (mandatory)
        self.logger.debug('_hack_lc_format: adding redshift column to lc file')
        lc_data = pd.merge(lc_data, sn_data[['sn', 'z']], on='sn', how='left')

        # TODO: qqe part dans le code original, il y a ca
        # TODO: c'est encore necessaire ?
        #    lcs = lcs.rename(columns={"sn":"sn_id"})

        self._lc_data = lc_data

    def _hack_spec_format(self):
        """Adapt the spectrum dataframe structure

        The DC1 mock light curve dataframe differs a bit from what is expected
        in a TDS. This function adapts the column names and add the missing
        fields.

        .. note:
           Ideally, this function should not exist. Please update the
           upcoming mock formats so that it can be safely removed for the next
           DC's
        """
        sn_data = self.sn_data
        spec_data = self.spec_data

        self.logger.debug('_hack_spec_format')
        spec_data['exptime'] = np.nan

        self.logger.debug('_hack_spec_format: converting "valid" field and checkin for NaNs')
        spec_data['valid'] = pd.to_numeric(spec_data['valid'],
                                           errors='coerce').astype('Int64')
        spec_data.loc[spec_data.valid.isna(), 'valid'] = 1

        self.logger.debug('_hack_spec_format: adding redshift column to spec file')
        spec_data = pd.merge(spec_data, sn_data[['sn', 'z']], on='sn', how='left')
        self._spec_data = spec_data
