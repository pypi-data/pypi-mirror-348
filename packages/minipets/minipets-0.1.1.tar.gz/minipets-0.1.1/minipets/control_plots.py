"""
Data cuts control plots
"""
import os
import logging
import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns
from nacl.dataset import TrainingDataset
from saltworks import plottools

plt.rcParams["legend.numpoints"] = 1
plt.rcParams["xtick.major.size"] = 21
plt.rcParams["xtick.minor.size"] = 5
plt.rcParams["ytick.major.size"] = 21
plt.rcParams["ytick.minor.size"] = 5
plt.rcParams["xtick.minor.visible"] = True  # See minor tick
plt.rcParams["text.usetex"] = False  # use Latex
plt.rcParams["axes.linewidth"] = 2  # width axes
plt.rcParams["axes.labelsize"] = 16  #
plt.rcParams["ytick.labelsize"] = 12  # fontsize of tick labels
plt.rcParams["xtick.labelsize"] = 12  # fontsize of tick labels
plt.rcParams["ytick.direction"] = "inout"  ## direction: in, out, or inout
plt.rcParams["xtick.direction"] = "inout"  ## direction: in, out, or inout

plt.rcParams["xtick.major.top"] = True  # draw x axis top major ticks
plt.rcParams["xtick.major.bottom"] = True  # draw x axis bottom major ticks
plt.rcParams["xtick.minor.top"] = True  ## draw x axis top minor ticks
plt.rcParams["xtick.minor.bottom"] = True  # draw x axis bottom minor ticks
plt.rcParams["axes.titlesize"] = 16  # Set title font size
plt.rcParams["axes.titleweight"] = "bold"  # Set title font weight to bold
plt.rcParams["ytick.major.left"] = True  # draw y axis left major ticks
plt.rcParams["ytick.major.right"] = True  # draw y axis right major ticks
plt.rcParams["ytick.minor.left"] = True  ## draw y axis left minor ticks
plt.rcParams["ytick.minor.right"] = True  # draw y axis right minor ticks
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "heavy"


def compa_hist(sne, output="figs", survey=None, show=True):
    """Make histograms of SN parameters"""
    sne_good = sne[sne.valid == 1]
    sne_bad = sne[sne.valid == 0]

    if survey is not None:
        sne_good = sne_good[sne_good.survey == survey]
        sne_bad = sne_bad[sne_bad.survey == survey]
    _suffix = survey if survey is not None else "all"
    fig, axes = plt.subplots(4, 1, figsize=(8, 16))

    for _j, _pname in enumerate(["z", "tmax", "x1", "c"]):
        bin_edges = np.histogram_bin_edges(
            np.concatenate([sne_good[_pname], sne_bad[_pname]]), bins="auto"
        )
        sns.histplot(
            sne_good[_pname],
            color="red",
            alpha=0.4,
            label="Good",
            kde=True,
            bins=bin_edges,
            ax=axes[_j],
        )
        sns.histplot(
            sne_bad[_pname],
            color="blue",
            label="Cut DR2",
            alpha=0.4,
            kde=True,
            bins=bin_edges,
            ax=axes[_j],
        )
        if _j==0:
            axes[_j].set_title(_suffix)
        axes[_j].set_ylabel("# SN")
        axes[_j].legend(prop={"weight": "bold"})
        axes[_j].set_xlabel(_pname)
        axes[_j].text(0.15, 0.8, _pname, transform=axes[_j].transAxes)

    for ax in axes:
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight("bold")

    plt.subplots_adjust(hspace=0.1)
    plt.tight_layout()

    if output is not None:
        os.makedirs(output, exist_ok=True)
        plt.savefig(
            f"{output}/distribution_comparison_{_suffix}.png",
            dpi=300,
            bbox_inches="tight",
        )
    if show:
        plt.show()

    return fig, axes


def compa_bin(sne, output="figs", survey=None, show=True):
    """Make binplot of SN parameters"""
    #pylint: disable=too-many-locals
    sne_good = sne[sne.valid == 1]
    sne_bad = sne[sne.valid == 0]

    if survey is not None:
        sne_good = sne_good[sne_good.survey == survey]
        sne_bad = sne_bad[sne_bad.survey == survey]
    _suffix = survey if survey is not None else "all"

    nbins = 10
    bins = np.linspace(
        sne_good["z"].min(),
        sne_good["z"].max() + abs(sne_good["z"].max() * 1e-7),
        nbins,
    )
    bins_bad = np.linspace(
        sne_bad["z"].min(), sne_bad["z"].max() + abs(sne_bad["z"].max() * 1e-7), nbins
    )
    fig = plt.figure(figsize=(8, 6))
    fig.subplots_adjust(hspace=0.0)

    ax0 = plt.subplot2grid((3, 1), (0, 0), rowspan=1)
    ax1 = plt.subplot2grid((3, 1), (1, 0), rowspan=1, sharex=ax0)
    ax2 = plt.subplot2grid((3, 1), (2, 0), rowspan=1)
    for _pname, _ax in zip(["x0", "x1", "c"], [ax0, ax1, ax2]):

        xbinned_p, yplot_p, yerr_p = plottools.binplot(
            sne_good.z.values, sne_good[_pname].values, nbins=nbins, noplot=True
        )
        xbinned_p_bad, yplot_p_bad, yerr_p_bad = plottools.binplot(
            sne_bad.z.values, sne_bad[_pname].values, nbins=nbins, noplot=True
        )

        _bins = bins if len(bins) == len(xbinned_p) else bins[0:len(xbinned_p)]
        _bins_bad = bins_bad if len(bins_bad) == len(xbinned_p_bad) else bins_bad[0:len(xbinned_p_bad)]

        xerr_p = np.array([_bins, _bins]) - np.array([xbinned_p, xbinned_p])
        xerr_p_bad = np.array([_bins_bad, _bins_bad]) - np.array(
            [xbinned_p_bad, xbinned_p_bad]
        )


        _ax.errorbar(
            xbinned_p,
            yplot_p,
            yerr=yerr_p,
            xerr=abs(xerr_p),
            marker="s",
            color="r",
            alpha=0.9,
            ms=6,
            ls="None",
            label="Good",
        )
        _ax.errorbar(
            xbinned_p_bad,
            yplot_p_bad,
            yerr=yerr_p_bad,
            xerr=abs(xerr_p_bad),
            marker="s",
            color="k",
            alpha=0.9,
            ms=6,
            ls="None",
            label="Cut DR2",
        )

        _ax.set_xlabel("zhel")
        _ax.set_ylabel(_pname)

        if _ax!=ax2:
            _ax.set_xticklabels([])
            
        if _pname=="x0":
            _ax.set_title(_suffix)
            _ax.legend()    

    if output is not None:
        os.makedirs(output, exist_ok=True)
        plt.savefig(
            f"{output}/binned_redshift_{_suffix}.png", dpi=300, bbox_inches="tight"
        )
    if show:
        plt.show()

    return fig, [ax0, ax1, ax2]
    
    
def plot_sn(tds, df_cut, snname, flag=None, photo=True, spec=False):
    """
    Make lightcurve or spectrum plot
    
    Give a sn name or give a flag name.
    If a flag name is given, we select randomly a SN cutted using this flag
    
    df_cut: Dataframe with all the cuts. This is the result of flag_data
    name: str (name of the SN)
    flag: 'None', 'phot_phase_range', 'spec_phase_range', 'spec_wl_range',
       'negative_or_zero_fluxerr', 'buggy_snr', 'low_snr', 'invalid_x0',
       'E(B-V)>0.25', 'n_bands_min', 'n_pts_min_tot', 'n_pts_min_before',
       'n_pts_min_after', 'out_c_range', 'out_x1_range', 'All'
    
    photo: Boolean if you want the photometry or not
    spec: Boolean if you want the spectrum or not
    """    
        
    if snname is None:
        assert flag is not None
        #Select randomly a SN cutted using the flag   
        snname = df_cut[df_cut.cut==flag].SN_cut.values[0]
        if len(snname)>0:
            snname = random.choice(snname)
            logging.info(f"choosing {snname}")
        else:
            logging.info('No sn to choose from, check flag name')	
    else:
        filtered_df = df_cut[df_cut["SN_cut"].apply(lambda x:
                                                    snname in x if isinstance(x, list) else False)]    
        flag = filtered_df.cut	
        
    if photo:
        tds.plot_lcs(f'{snname}')
    if spec:
        speclist = np.unique(tds.spec_data.nt[tds.spec_data.sn==snname].spec)
        if len(speclist)>0:
            specname = speclist[0]
            tds.plot_spectrum(specname)
        else:
            logging.info(f'No spectrum for {snname}')

    return flag,snname
    
    
def compa_snr(df_ini,df_fin, survey=None, instru=None, show=True,snr_max=500,bins=100,name_ini='No DR2',name_fin='DR2'):
	"""
	Function to comapre the SNR of two spect dataframe.
	
	df1: DataFrame for example the spectra after range cut but before DR2 cuts
	
	df2: DataFrame for example the spectra after all the cuts

	survey: str  can be ZTF, SNLS, HSC
	instru: str  No available for the moment
	snr_max: float useful to cut the figure
	bins: float histrogram bins
	
	name_ini= str  name of the df_ini, e.g. no DR2
	name_fin= str  name of the df_fin, e.g.  DR2
		"""    

	df_ini['snr']=df_ini.flux/df_ini.fluxerr
	df_fin['snr']=df_fin.flux/df_fin.fluxerr

	df_ini=df_ini[df_ini['snr']<snr_max]
	df_fin=df_fin[df_fin['snr']<snr_max]


	_suffix = survey if survey is not None else "all"
	if survey is not None:

		df_ini = df_ini[df_ini['sn'].str.startswith(survey)]
		df_fin = df_fin[df_fin['sn'].str.startswith(survey)]


	if instru is not None:
		df_ini = df_ini[df_ini.instru == instru]
		df_fin = df_fin[df_fin.instru == instru]	


	plt.hist(df_ini['snr'],bins=bins,label=name_ini)
	plt.hist(df_fin['snr'],bins=bins,label=name_fin)

	plt.yscale('log')
	plt.title(_suffix)
	plt.legend()
	if show:
		plt.show()    
	else:
		plt.close()
