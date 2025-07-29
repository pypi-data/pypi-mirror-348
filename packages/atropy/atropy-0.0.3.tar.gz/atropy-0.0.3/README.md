# `atropy`: Dynamical Low-Rank Solver for Stochastic Reaction Networks

## Objective
`atropy` solves the chemical master equation (CME) with the dynamical low-rank approximation.
<!-- TODO: Add a low-level description what atropy actually does. -->

`atropy` allows the user to build models and run simulations. Examples of use can be found on our [project website](https://atropy.gitlab.io/).

## Requirements
- C/C++ and Fortran compilers
- Python (>=3.10)

The following compilers were successfully tested:
- gcc-14
- Apple Clang 16 + gfortran-14
- Clang 20 + Flang 20
<!-- MacOS: For OpenBLAS, the gfortran library has to be indicated 
in the LIBRARY_PATH  -->
<!-- TODO: Add Stefan's compiler configuration -->

## Installation

Download the package with `pip` or `uv` by invoking
```shell
pip install atropy
```
or
```shell
uv pip install atropy
```

<!-- The package is installed in `<path_to_environment>/lib/python<python_version>/site-packages` with all the dependencies, which were also downloaded from PyPI. -->

<!-- ## Example problems

After installation several example problems can be run. Those can be found in `<path_to_atropy>/src/examples`. One can run a problem by executing
```shell
python3 <path_to_atropy>/src/examples/run_lambda_phage.py
```

If successful, output files should be generated in the current working directory. -->
