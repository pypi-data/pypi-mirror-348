"""
utilitary functions to:
- convert data from skysurvey to nacl and vice versa
"""

import numpy as np

def make_sne_nacl(data):
    """Convert skysurvey df into nacl recarray.
    
    data: skysurvey snia catalog as pd.dataframe
    """
    sn_data_dtype = np.dtype([
        ('sn', '<i8'), ('z', '<f8'), ('tmax', '<f8'), ('x1', '<f8'),
        ('x0', '<f8'), ('c', '<f8'), ('mwebv', '<f8'), ('valid', '<i8'), ('IAU', 'O')])
    N = len(data)
    sne = np.recarray((N), dtype=sn_data_dtype)
    sne["sn"] = data.index.values
    sne["z"] = data["z"]
    sne["tmax"] = data["t0"]
    sne["x1"] = data["x1"]
    sne["x0"] = data["x0"]
    sne["c"] = data["c"]
    sne["valid"] = np.ones((N))
    return sne

def make_lc_nacl(data):
    """Convert skysurvey df into nacl recarray.
    
    data: skysurvey lc catalog as pd.dataframe
    """
    lc_data_dtype = np.dtype([
        ('sn', '<i8'), ('mjd', '<f8'), ('flux', '<f8'), ('fluxerr', '<f8'),
        ('band', 'O'), ('magsys', 'O'), ('exptime', '<f8'), ('valid', '<i8'),
        ('lc', '<i8'), ('zp', '<f8'), ('mag_sky', '<f8'), ('seeing', '<f8'),
        ('x', '<f8'),('y', '<f8'), ('sensor_id', '<i8')])
    N = len(data)
    lc = np.recarray((N), dtype=lc_data_dtype)
    lc["sn"] = [l[0] for l in data.index.values.tolist()]
    lc["mjd"] = data["mjd"]
    lc["flux"] = data["flux"]
    lc["fluxerr"] = data["fluxerr"]
    lc["band"] = data["band"]
    lc["zp"] = data["zp"]
    lc['magsys'] = data["zpsys"]
    lc["valid"] = np.ones((N))
    k = 0
    for b in np.unique(lc["band"]):
            for sn in np.unique(lc["sn"]):
                _sel = (lc["sn"] == sn) & (lc["band"] == b)
                lc['lc'][_sel] = k
                k += 1
    return lc
