import warnings
warnings.filterwarnings("ignore")

from os.path import join as pjoin
from minipets import SimDataset

def test_sim():
    ds = SimDataset()
    logs = "/work/data/ztf/ztf_survey.pkl"
    ds.generate(logs, N=3000, nacl_flux=True, noise=True)
    ds.filter_data()
