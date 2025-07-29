
Sylvie's gists in order to create pypi and conda packages are found [here](https://gist.github.com/slgentil)

In order to release a new version of the library:

- update tag in `conda/meta.yaml`, `conda/convert_upload.sh`, `doc/conf.py`
- if need be, update python versions in `setup.cfg`, `conda/conda_build_config.yaml`, `conda/convert_upload.sh`, `github/ci.yaml`
- install libraries required to compile and export packages in `base` environment:

```
conda activate base
conda install conda-build conda-verify anaconda-client
```

- run in library root dir (`pynsitu/`):

``` 
conda build -c pyviz -c conda-forge -c apatlpo --output-folder ${HOME}/Code/wheels/  ./conda
```

- run `convert_upload.sh` to produce and upload packages

- create release on github

---

## new notes

Create pypi package: [Pypi doc](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

https://conda-forge.org/docs/maintainer/adding_pkgs/

https://pypi.org/manage/unverified-account/?next=%2Fmanage%2Fprojects%2F


1. Create a conda environment to build

```
conda create -n pypi pip
conda activate pypi
pip install "black[jupyter]"
python3 -m pip install --upgrade build
```

2. Package files

```
python3 -m build
```




https://github.com/pyOpenSci/pyosPackage/blob/main/pyproject.toml