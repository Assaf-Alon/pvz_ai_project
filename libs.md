# libs.txt - External Software Used
All relevant installation instructions can be found on the main README.md file
Installation instruction can be found on the main README.md.

## Python Packages
- numpy
- pandas
- matplotlib
- scipy
- seaborn
- statsmodels
- pillow


## List of Linux dependencies for compiling the c++ environment:
- clang-format
- clang-tidy
- clang-tools
- clangd
- libc++-dev
- libc++1
- libc++abi-dev
- libc++abi1
- libclang-dev
- libclang1
- liblldb-dev
- libllvm-ocaml-dev
- libomp-dev
- libomp5
- lld
- lldb
- llvm-dev
- llvm-runtime
- llvm
- python3-clang
- libpython3-dev
- make
- libgmp3-dev
- libomp-dev
- swig

## Dependency details
- llvm: A collection of modular and reusable compiler and toolchain technologies. It is used to compile the C++ code. Supports both compilation and analysis.
- libomp: The OpenMP runtime library. It is used to run the C++ code in parallel.
- libgmp: The GNU Multiple Precision Arithmetic Library. It is used to perform arbitrary precision arithmetic.
- libpython3-dev: The development files for the Python3 interpreter. It is used to compile the C++ code with Python bindings.
- swig: Simplified Wrapper and Interface Generator. It is used to connect C++ code with Python code. [SWIG Download](https://www.swig.org/download.html)

## Runtime Related Software
Singularity - used to build and run container images (similar to Docker). Singularity is used instead of Docker because it allowes installation without root permissions, which is unavailable in the LAMBDA cluster.
- [Release 4.1.3 - GitHub](https://github.com/sylabs/singularity/releases/tag/v4.1.3)
- [SingularityCE Quick Start Guide](https://docs.sylabs.io/guides/latest/user-guide/quick_start.html)
