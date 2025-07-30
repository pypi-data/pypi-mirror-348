# `dr2cuts.py` — test after dr2-like cut updates 

This script is used to verify that two different versions of the module (one using `get_tds()`, the other not) produce **exactly the same TDS** when run on the same mock dataset.

## Purpose

- Apply both the `get_tds()`-based and `get_tds()`-free pipelines to the same mock dataset.
- Ensure that the resulting TDS files are **identical**.
- Consistency is verified via MD5 checksums of the `.parquet` output files.

---

## Tests (for futher reference)

### commit: 16ab62eb019

```bash
(georges-dev) user@host $ ./dr2cuts.py --mock 0 georges/workflow/mocks/dc1.v2/ 
2025-05-09 18:49:06,780 INFO sparse_dot_mkl found. Building hessian should be faster.
2025-05-09 18:49:11,693 INFO loading lemaitre filterlib from <snip>
2025-05-09 18:49:12,497 INFO removing 3012 SNe with less than 2 bands: ['HSC_4' 'HSC_5' 'HSC_7' ... 'ZTF_15729' 'ZTF_15776' 'ZTF_15830']
2025-05-09 18:49:17,516 INFO removing 6795 SNe with less than 5 points: ['HSC_4' 'HSC_5' 'HSC_7' ... 'ZTF_15865' 'ZTF_15867' 'ZTF_15869']
2025-05-09 18:49:22,288 INFO removing 9432 SNe with less than 2 points before max: ['HSC_1' 'HSC_5' 'HSC_7' ... 'ZTF_15855' 'ZTF_15867' 'ZTF_15869']
2025-05-09 18:49:25,748 INFO removing 6775 SNe with less than 2 points after max: ['HSC_4' 'HSC_7' 'HSC_8' ... 'ZTF_15858' 'ZTF_15865' 'ZTF_15869']
2025-05-09 18:49:25,753 INFO 964 SNe killed because out of range in color
2025-05-09 18:49:25,764 INFO 64 SNe killed because out of range in x1
2025-05-09 18:49:45,172 WARNING bandpass MEGACAM6::g not in filterlib -- retrieving it from sncosmo
2025-05-09 18:49:45,196 WARNING bandpass MEGACAM6::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:49:45,205 WARNING bandpass MEGACAM6::i2 not in filterlib -- retrieving it from sncosmo
2025-05-09 18:49:45,214 WARNING bandpass MEGACAM6::r not in filterlib -- retrieving it from sncosmo
2025-05-09 18:49:45,223 WARNING bandpass MEGACAM6::z not in filterlib -- retrieving it from sncosmo
2025-05-09 18:49:45,233 WARNING bandpass ztf::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:49:45,680 INFO indexing light curves
2025-05-09 18:49:53,252 INFO indexing spectra
```

### commit: 93eb7ad5469e

``` bash
(georges) xxx@host $ ./dr2cuts.py --mock 0 georges/workflow/mocks/dc1.v2/ --output tds_bis.parquet
2025-05-09 18:51:33,768 INFO sparse_dot_mkl found. Building hessian should be faster.
2025-05-09 18:51:33,792 INFO sparse_dot_mkl found. Building hessian should be faster.
2025-05-09 18:51:34,862 INFO sparse_dot_mkl found. Building hessian should be faster.
2025-05-09 18:51:37,991 INFO loading lemaitre filterlib from <snip>
2025-05-09 18:51:57,741 WARNING bandpass MEGACAM6::g not in filterlib -- retrieving it from sncosmo
2025-05-09 18:51:57,782 WARNING bandpass MEGACAM6::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:51:57,792 WARNING bandpass MEGACAM6::i2 not in filterlib -- retrieving it from sncosmo
2025-05-09 18:51:57,801 WARNING bandpass MEGACAM6::r not in filterlib -- retrieving it from sncosmo
2025-05-09 18:51:57,810 WARNING bandpass MEGACAM6::z not in filterlib -- retrieving it from sncosmo
2025-05-09 18:51:57,829 WARNING bandpass ztf::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:51:58,299 INFO indexing light curves
2025-05-09 18:52:05,648 INFO indexing spectra
2025-05-09 18:52:40,149 INFO removing 3012 SNe with less than 2 bands: ['HSC_13433' 'HSC_13458' 'SNLS_1532' ... 'HSC_13604' 'HSC_13089'
 'HSC_16007']
2025-05-09 18:53:01,638 WARNING bandpass MEGACAM6::g not in filterlib -- retrieving it from sncosmo
2025-05-09 18:53:01,650 WARNING bandpass MEGACAM6::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:53:01,652 WARNING bandpass MEGACAM6::i2 not in filterlib -- retrieving it from sncosmo
2025-05-09 18:53:01,655 WARNING bandpass MEGACAM6::r not in filterlib -- retrieving it from sncosmo
2025-05-09 18:53:01,657 WARNING bandpass MEGACAM6::z not in filterlib -- retrieving it from sncosmo
2025-05-09 18:53:01,660 WARNING bandpass ztf::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:53:02,097 INFO indexing light curves
2025-05-09 18:53:09,254 INFO indexing spectra
2025-05-09 18:53:47,238 INFO removing 6795 SNe with less than 5 points: ['ZTF_6859' 'HSC_1911' 'HSC_8388' ... 'HSC_2335' 'HSC_16007' 'HSC_3584']
2025-05-09 18:54:07,243 WARNING bandpass MEGACAM6::g not in filterlib -- retrieving it from sncosmo
2025-05-09 18:54:07,270 WARNING bandpass MEGACAM6::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:54:07,273 WARNING bandpass MEGACAM6::i2 not in filterlib -- retrieving it from sncosmo
2025-05-09 18:54:07,275 WARNING bandpass MEGACAM6::r not in filterlib -- retrieving it from sncosmo
2025-05-09 18:54:07,277 WARNING bandpass MEGACAM6::z not in filterlib -- retrieving it from sncosmo
2025-05-09 18:54:07,279 WARNING bandpass ztf::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:54:07,746 INFO indexing light curves
2025-05-09 18:54:14,996 INFO indexing spectra
2025-05-09 18:54:54,618 INFO removing 9432 SNe with less than 2 points before max: ['ZTF_6859' 'HSC_1911' 'HSC_8388' ... 'SNLS_2908' 'HSC_16007' 'HSC_3584']
2025-05-09 18:55:14,427 WARNING bandpass MEGACAM6::g not in filterlib -- retrieving it from sncosmo
2025-05-09 18:55:14,429 WARNING bandpass MEGACAM6::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:55:14,431 WARNING bandpass MEGACAM6::i2 not in filterlib -- retrieving it from sncosmo
2025-05-09 18:55:14,434 WARNING bandpass MEGACAM6::r not in filterlib -- retrieving it from sncosmo
2025-05-09 18:55:14,436 WARNING bandpass MEGACAM6::z not in filterlib -- retrieving it from sncosmo
2025-05-09 18:55:14,438 WARNING bandpass ztf::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:55:14,874 INFO indexing light curves
2025-05-09 18:55:22,283 INFO indexing spectra
2025-05-09 18:56:00,874 INFO removing 6775 SNe with less than 2 points after max: ['HSC_1911' 'HSC_13433' 'ZTF_7070' ... 'HSC_16007' 'HSC_3584' 'HSC_3600']
2025-05-09 18:56:01,041 INFO 964 SNe killed because out of range in color
2025-05-09 18:56:01,054 INFO 64 SNe killed because out of range in x1
2025-05-09 18:56:21,179 WARNING bandpass MEGACAM6::g not in filterlib -- retrieving it from sncosmo
2025-05-09 18:56:21,183 WARNING bandpass MEGACAM6::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:56:21,185 WARNING bandpass MEGACAM6::i2 not in filterlib -- retrieving it from sncosmo
2025-05-09 18:56:21,187 WARNING bandpass MEGACAM6::r not in filterlib -- retrieving it from sncosmo
2025-05-09 18:56:21,189 WARNING bandpass MEGACAM6::z not in filterlib -- retrieving it from sncosmo
2025-05-09 18:56:21,191 WARNING bandpass ztf::i not in filterlib -- retrieving it from sncosmo
2025-05-09 18:56:21,640 INFO indexing light curves
2025-05-09 18:56:28,930 INFO indexing spectra
```

### Consistency check

``` bash
(georges-dev) xxx@host $ md5sum tds.*.parquet
135b1125e1a0e14598c885e40dcc1920  tds.lc.parquet
2e2318f100933d44d61611d695d52097  tds.sn.parquet
1f4a698776ad30744e48e0c150ac74da  tds.spec.parquet
(georges) xxx@host $ md5sum tds_bis.*.parquet
135b1125e1a0e14598c885e40dcc1920  tds_bis.lc.parquet
2e2318f100933d44d61611d695d52097  tds_bis.sn.parquet
1f4a698776ad30744e48e0c150ac74da  tds_bis.spec.parquet
```
