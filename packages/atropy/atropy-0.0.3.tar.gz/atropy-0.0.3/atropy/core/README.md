# `atropy_core`: DLR approximation for the kinetic CME

- [`atropy_core`: DLR approximation for the kinetic CME](#atropy_core-dlr-approximation-for-the-kinetic-cme)
  - [Objective](#objective)
  - [Requirements](#requirements)
  - [Optional requirements](#optional-requirements)
  - [Installation](#installation)
    - [Intel MKL](#intel-mkl)
    - [OpenMP](#openmp)
    - [pybind11](#pybind11)
    - [Python environment](#python-environment)
  - [Run the program](#run-the-program)
  - [Input](#input)
    - [Preparing input data](#preparing-input-data)
  - [Output](#output)
  - [Example problems](#example-problems)
  - [References](#references)

## Objective
`atropy_core` solves the chemical master equation (CME),
$$\partial_t{P}(t,\mathbf{x}) = \sum_{\mu = 0}^{M-1}\left(\alpha_\mu(\mathbf{x}-\bm{\nu}_\mu)P(t,\mathbf{x}-\bm{\nu}_\mu) - \alpha_\mu(\mathbf{x})P(t,\mathbf{x})\right)$$

according to the algorithm proposed in \[1\], which is based on the projector-splitting integrator for tree tensor networks \[2\].

$P(t,\mathbf{x})\,\mathrm{d}t$ is the probability of finding a population number of $\mathbf{x} = (x_0, \dots, x_{N-1})$ molecules of species $S_0, \dots, S_{N-1}$ at time $t$.
The CME describes the time evolution of this probability distribution $P(t,\mathbf{x})$ in a chemical reaction network with $N$ different species $S_0, \dots, S_{N-1}$, which can react via $M$ reaction channels $R_0, \dots, R_{M-1}$. For a given reaction $\mu$, the stoichiometric vector $\bm{\nu}_\mu$ denotes the population change by that reaction and the propensity functions $\alpha_\mu(\mathbf{x})$ and $\alpha_\mu(\mathbf{x}-\bm{\nu}_\mu)$ are proportional to the transition probabilities $T(\mathbf{x}+\bm{\nu}_\mu|\mathbf{x})$ and $T(\mathbf{x}|\mathbf{x}-\bm{\nu}_\mu)$.

`atropy_core` makes use of the low-rank framework `Ensign` \[3\].

## Requirements
- C++20 compatible C++ compiler
- CMake (3.27 or later)
- Eigen 3.4
- netCDF4 (built together with HDF5)
- Python (>3.10)

Check via `nc-config --has-hdf5`, whether HDF5 was used in the netCDF4 build.

## Optional requirements
- Fortran compiler (if OpenBLAS is used)
- Intel MKL
- OpenMP

See below for a description how Intel MKL and OpenMP can be enabled.

## Installation
Build the program in the `<build>` directory by executing
```shell
cmake -B <build> -DCMAKE_BUILD_TYPE=Release
cmake --build <build>
```
in the project root. The generated executable `atropy_core` can be found in `<build>`.

To enable compiler options for debugging, use `-DCMAKE_BUILD_TYPE=Debug` instead.
Unit tests for C++ files are provided in the `tests` folder. They can be built by activating the `-DBUILD_TESTING` flag. Run the tests with
```shell
ctest --test-dir <build>
```

### Intel MKL
If you prefer to use Intel MKL as the BLAS and LAPACK backend instead of OpenBLAS set the `-DMKL_INCLUDEDIR` and `-DMKL_LIBDIR` variables and build with
```shell
cmake -B <build> -DCMAKE_BUILD_TYPE=Release -DMKL_ENABLED=ON
cmake --build <build>
```
Make sure to add the MKL libraries to your `LD_LIBRARY_PATH`, i.e.
```shell
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/intel/mkl/lib/intel64_lin/
```
before running the executable.
<!-- TODO: This step could be avoided by adding a 
`target_link_directories` command for MKL in Ensign CMakeLists.txt -->

### OpenMP
OpenMP can be activated via
```shell
cmake -B <build> -DCMAKE_BUILD_TYPE=Release -DOPENMP=ON
```
Make sure that the `OMP_NUM_THREADS` environment variable is in accordance with your hardware specification and run the unit tests via 
```shell
ctest --test-dir <build>
```
to ensure that OpenMP and `atropy_core` work correctly.

**macOS:** Note that XCode compilers do not support OpenMP. For using OpenMP on macOS, a manual installation (e.g. of `gcc11`) is required and the `CXX`, `CC` and `FC` environment variables have to be set accordingly.

### pybind11
The tree tensor network integrator `IntegrateTTN` of `atropy_core`,
```c++
IntegrateTTN(std::string input, std::string output, int snapshot, double tau, double tfinal, unsigned int substeps, char method)
```
where parameters are the same as the command line arguments for `atropy_core` (cf. [next section](#run-the-program)), is available in the pybind11 module `atropy_core_pybind11` and thus can be used in Python. The Python wrapper for `atropy_core`, called `atropy`, makes use of this module. Build `atropy_core` with the `-DPYBIND11_ENABLED` flag to generate the pybind11 module.

**macOS:** pybind11 might not find the `Python.h` header during the CMake build process.
In that case, set `export CPLUS_INCLUDE_PATH=<path/to/python/include>` accordingly.

### Python environment
To use the Python programs included in `atropy_core`, a Python environment with external packages specified in `pyproject.toml` needs to be configured and enabled. This can be done using uv pip install or classical pip install.

For uv:
```shell
uv venv my_venv --python <python_version>
source my_venv/bin/activate
uv pip install .
```

For Python venv:
```shell
python -m venv path/to/my_venv
source path/to/my_venv/bin/activate
pip install .
```
For anaconda:
```shell
conda create -n my_venv python
conda activate my_venv
pip install .
```
All scripts have to be executed from the project root. When using a IDE, make sure to adjust the settings accordingly.
Unit tests for Python files are located in the `atropy_core/tests` folder. They can be run in the Python environment via
```shell
pytest atropy_core/tests
```

## Run the program
`atropy_core` has to be run with
```
  ./build/atropy_core [OPTION...]
```
and expects the following command line arguments:
- `-i`, `--input`: Name of the input .nc file (default: `input/input.nc`)
- `-o`, `--output`: Name of the output folder, stored in `output/`
- `-s`, `--snapshot`: Number of steps between two snapshots
- `-t`, `--tau`: Time step size
- `-f`, `--tfinal`: Final integration time
- `-n`, `--substeps`: Number of integration substeps (default: `1`)
- `-m`, `--method`: Integration method (`e` (explicit Euler), `r` (explicit RK4), `i` 
                      (implicit Euler), `c` (Crank-Nicolson)) (default: `i`)
- `-h`, `--help`: Print usage

## Input
Input netCDF files have to be stored as `input/input.nc` (the directory can be changed using the `-i` flag) and can be generated with the input scripts provided in `atropy_core/examples`.

**Caution:** As `Ensign` stores arrays in column-major (Fortran) order, it is assumed that input arrays also follow this convention.
<!-- TODO: Give more detais -->

<!-- TODO: ### Binning -->

### Preparing input data
Let us consider the input script `set_lambda_phage.py` located in the `atropy_core/examples` folder, which generates input data for the lambda phage model. It gives an example on how the initial conditions have to be set up. A short documentation for this script is provided by
```shell
python3 atropy_core/examples/set_lambda_phage.py --help
```
<!-- TODO: ### Describe examples in more detail -->

Note that `atropy_core` assumes that the propensity function is factorizable for the species in different partitions. However, the input scripts rely on the `ReactionSystem` class (cf. `atropy_core/reaction.py`), which assumes that the propensity function is factorizable in *all* species. This is a valid assumption for most scenarios. For problems where species in a partition are not factorizable, the propensity function can be adjusted manually after initializing the `Tree` with the method `initialize`.

<!-- #### Writing a model file with the `ReactionSystem` class
The model file contains all reactions $`R_\mu`$ ($`\mu=1,\dots,M`$) of the specific problem and has to be imported in the input scripts. -->

<!-- TODO: More detailed description. -->


## Output
`atropy_core` automatically creates a folder in `output/` with a name set by the `-o`/`--output` parameter.
The low-rank factors and coupling coefficients as well as the chosen model parameters are stored in this folder as `output_t<ts>.nc` (`<ts>` denotes the time step) in intervals according to the `-s`/`--snapshot` parameter.

<!-- TODO: Describe the structure of the .netCDF file -->

## Example problems
Input generation scripts for the example problems (toggle switch, lambda phage and reaction cascade) are provided in `atropy_core/examples` and the corresponding model files can be found in `atropy_core/examples/models`.

The Python file `output_helper.py` contains helper functions such as `readTree` and the `TimeSeries` class for plotting the NetCDF files.

## References
\[1\] Einkemmer, L., Mangott, J., and Prugger, M.: "A hierarchical dynamical low-rank algorithm for the stochastic description of large reaction networks", *arXiv*, <https://arxiv.org/abs/2407.11792> (2024)

\[2\] Ceruti, G., Lubich, C., and Walach, H.: "Time integration of Tree Tensor networks", *SIAM J. Numer. Anal.* **59** (2021)
<!-- Lubich, C., Oseledets, I.: "A projector-splitting integrator for dynamical low-rank approximation", BIT Numerical Mathematics **54** (2014) -->

\[3\] Cassini, F., and Einkemmer, L.: "Efficient 6D Vlasov simulation using the dynamical low-rank framework Ensign", *Comp. Phys. Comm.* **280** (2022)
