#!/usr/bin/env python
#
# This is an example to show how to apply the DR2 cuts to a dataset
#
# I wrote it to make sure that I obtain the exact same results with the
# get_tds() version of the dr2cuts (slow) and the get_tds()-free version Too big
# to make a real test out of it unfortunately.
#
from argparse import ArgumentParser
import pathlib
import pandas
from minipets import Dataset


def load_dataset(input_dir, mock_number):
    """
    """
    sn_data = pandas.read_parquet(input_dir / f'sn_data_{mock_number}.parquet')
    lc_data = pandas.read_parquet(input_dir / f'lc_data_{mock_number}.parquet')
    spec_data = pandas.read_parquet(input_dir / f'spec_data_{mock_number}.parquet')
    return Dataset(sn_data, lc_data, spec_data)


if __name__ == '__main__':
    parser = ArgumentParser(description='apply the default DR2 cuts and dump the resulting tds')
    parser.add_argument('--output',
                        type=pathlib.Path,
                        default=pathlib.Path('tds.parquet'),
                        help='output tds name')
    parser.add_argument('--mock',
                        default=0,
                        type=int,
                        help='mock number')
    parser.add_argument('input_mock_dir',
                        type=pathlib.Path,
                        help='input mock directory')

    args = parser.parse_args()

    dset = load_dataset(args.input_mock_dir, args.mock)
    dset.dr2_like_cuts()
    tds = dset.get_tds()
    tds.to_parquet(args.output)
