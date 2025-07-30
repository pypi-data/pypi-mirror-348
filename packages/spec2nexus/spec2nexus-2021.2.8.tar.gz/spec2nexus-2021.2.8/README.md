# spec2nexus

Reads SPEC data files, writes into NeXus HDF5 files:

    $ spec2nexus  path/to/file/specfile.dat

Writes `path/to/file/specfile.hdf5`

- Conda install:  `conda install -c conda-forge spec2nexus`
- Pip install:  `pip install spec2nexus`

## Provides

### Applications

- [**spec2nexus**](https://prjemian.github.io/spec2nexus/spec2nexus.html) :
  Convert [SPEC](https://certif.com) data
  files to [NeXus](https://nexusformat.org) [HDF5](https://hdfgroup.org)

- [**extractSpecScan**](https://prjemian.github.io/spec2nexus/extractSpecScan.html) :
  Save columns from SPEC data file scan(s) to TSV files

- [**specplot**](https://prjemian.github.io/spec2nexus/specplot.html) :
  plot a SPEC scan to an image file

- [**specplot\_gallery**](https://prjemian.github.io/spec2nexus/specplot_gallery.html) :
  call **specplot** for all scans in a list of files, makes a web gallery

### Libraries

- [**spec**](https://prjemian.github.io/spec2nexus/spec.html) :
  python binding to read SPEC data files

- [**eznx**](https://prjemian.github.io/spec2nexus/eznx.html) :
  (Easy NeXus) supports writing NeXus HDF5 files using h5py

## Package Information

term | description
--- | ---
**copyright** | (c) 2014-2022, Pete R. Jemian
**links** | [documentation](https://prjemian.github.io/spec2nexus),  [release notes](https://github.com/prjemian/spec2nexus/wiki/Release-Notes),  [source code](https://github.com/prjemian/spec2nexus)
**citation** | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6264513.svg)](https://doi.org/10.5281/zenodo.6264513)
**license** | [![Creative Commons Attribution 4.0 International Public License](https://anaconda.org/conda-forge/spec2nexus/badges/license.svg)](https://prjemian.github.io/spec2nexus/license.html)  [LICENSE](https://prjemian.github.io/spec2nexus/license.html)
**current releases** | [![image](https://img.shields.io/github/tag/prjemian/spec2nexus.svg)](https://github.com/prjemian/spec2nexus/tags)    [![image](https://img.shields.io/github/release/prjemian/spec2nexus.svg)](https://github.com/prjemian/spec2nexus/releases)
**conda-forge** | [![https://anaconda.org/conda-forge/spec2nexus](https://anaconda.org/conda-forge/spec2nexus/badges/installer/conda.svg)](https://anaconda.org/conda-forge/spec2nexus)    [![https://anaconda.org/conda-forge/spec2nexus](https://anaconda.org/conda-forge/spec2nexus/badges/version.svg)](https://anaconda.org/conda-forge/spec2nexus)   [![Anaconda-Server Badge](https://anaconda.org/conda-forge/spec2nexus/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/spec2nexus)
**PyPI** | [![https://pypi.python.org/pypi/spec2nexus](https://badge.fury.io/py/spec2nexus.svg)](https://badge.fury.io/py/spec2nexus)    [![image](https://img.shields.io/pypi/v/spec2nexus.svg)](https://pypi.python.org/pypi/spec2nexus/)
**current builds** | [![Anaconda-Server Badge](https://anaconda.org/conda-forge/spec2nexus/badges/platforms.svg)](https://anaconda.org/conda-forge/spec2nexus)   ![Python Package using Conda](https://github.com/prjemian/spec2nexus/workflows/Python%20Package%20using%20Conda/badge.svg)
**test & review** | [![image](https://img.shields.io/pypi/pyversions/spec2nexus.svg)](https://pypi.python.org/pypi/spec2nexus)   [![image](https://coveralls.io/repos/github/prjemian/spec2nexus/badge.svg?branch=main)](https://coveralls.io/github/prjemian/spec2nexus?branch=main)    [![Total alerts](https://img.shields.io/lgtm/alerts/g/prjemian/spec2nexus.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/prjemian/spec2nexus/alerts/)   [![Codacy Badge](https://app.codacy.com/project/badge/Grade/58888d7def9e4cedb167b94c8fe53a26)](https://www.codacy.com/gh/prjemian/spec2nexus/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=prjemian/spec2nexus&amp;utm_campaign=Badge_Grade)
**author** | Pete R. Jemian
**email** | prjemian@gmail.com

## NOTE about support for Python version 2

spec2nexus ended development for Python 2 with release 2021.1.7, 2019-11-21.
For more information, visit https://python3statement.org/.
