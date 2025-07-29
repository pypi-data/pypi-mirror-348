# Symbolic Aggregate approXimation #

This package implements the Symbolic Aggregate approXimation (SAX) algorithm in C++ with Python bindings using pybind11. SAX is a time series discretization method that represents a continuous-valued time series as a (sliding window of) symbolic representation(s). 

[Jessica Lin's SAX page](http://cs.gmu.edu/~jessica/sax.htm)

[Eamonn Keogh's SAX page](http://www.cs.ucr.edu/~eamonn/SAX.htm)

# Installation
The easiest way to install `sax-ts` is via pip:
```
pip install sax-ts
```

If you want to run the tests locally, install the optional dependencies:
```
pip install "sax-ts[test]"
```

You can then import the `sax` and `paa` functions as follows:
```Python
from sax_ts import sax, paa
```
# References

P. Patel, E. Keogh, J. Lin and S. Lonardi, "Mining motifs in massive time series databases," 2002 IEEE International Conference on Data Mining, 2002. Proceedings., Maebashi City, Japan, 2002, pp. 370-377, doi: 10.1109/ICDM.2002.1183925.

J. Lin, E. Keogh, S. Lonardi, and B. Chiu, "A symbolic representation of time series, with implications for streaming algorithms," In Proceedings of the 8th ACM SIGMOD workshop on Research issues in data mining and knowledge discovery, 2003, pp. 2-11, doi: 10.1145/882082.882086.

J. Lin, E. Keogh, L. Wei, and S. Lonardi, "Experiencing SAX: a novel symbolic representation of time series," Data Min Knowl Disc, vol. 15, pp. 107–144, Apr. 2007, doi: 10.1007/s10618-007-0064-z.