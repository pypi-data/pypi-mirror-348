from os.path import join as pjoin
from minipets import MockDataset
from minipets import compa_hist, compa_bin, plot_sn

dc1 = "/work/soft/sn-nacl/letsgo/DC1_0_batch999"

def test_filter_data():
    mock = MockDataset(sn_path=pjoin(dc1, 'DC1_0_batch_999.sn.parquet'),
                       lc_path=pjoin(dc1, 'DC1_0_batch_999.lc.parquet'),
                       spec_path=pjoin(dc1, 'DC1_0_batch_999.spec.parquet'))
    mock.filter_data()

if __name__ == '__main__':
    mock = MockDataset(sn_path=pjoin(dc1, 'DC1_0_batch_999.sn.parquet'),
                       lc_path=pjoin(dc1, 'DC1_0_batch_999.lc.parquet'),
                       spec_path=pjoin(dc1, 'DC1_0_batch_999.spec.parquet'))
    df_cut = mock.flag_data()
    compa_hist(mock.sn_data)
    compa_bin(mock.sn_data)
    tds = mock.get_tds()
    f = plot_sn(tds, df_cut, snname='ZTF_1035900', flag=None, photo=True, spec=True)
