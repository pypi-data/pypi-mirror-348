# Detect number of threads to build with.
ifndef CPU_COUNT
	NUM_THREADS = 1
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		NUM_THREADS = $(shell nproc || 1)
	endif
	ifeq ($(UNAME_S),Darwin)
		NUM_THREADS = $(shell sysctl -n hw.physicalcpu)
	endif
	ifeq ($(findstring MSYS_NT,$(UNAME_S)),MSYS_NT)
		NUM_THREADS = ${NUMBER_OF_PROCESSORS}
	endif
else
	NUM_THREADS = $(CPU_COUNT)
endif

# Ideally we should use a packaging tool command like pip here instead of just `python
# setup.py build_ext` because calling `setup.py` directly does not respect PEP 517 and
# does not regenerate version.py when it's deleted (e.g. with a `make realclean`) and
# does not build in an isolated environment. Unfortunately the pip command is far
# slower, and rebuilds extensions even if nothing has changed, so for now we keep the
# `setup.py` command and instead just make sure that the build dependencies specified in
# `pyproject.toml` are present in the local environment, which seems to allow version.py
# to get rebuilt.

ifeq ($(findstring MSYS_NT,$(UNAME_S)),MSYS_NT)
# See https://gitlab.com/ifosim/finesse/finesse3/-/issues/438
# See https://gitlab.com/ifosim/finesse/finesse3/-/issues/463
	BUILD_CMD = python setup.py build_ext -j $(NUM_THREADS) --inplace --compiler=msvc
	CONDA_YML = environment-win.yml
else
	BUILD_CMD = python setup.py build_ext -j $(NUM_THREADS) --inplace
	CONDA_YML = environment.yml
endif

# use mamba when available because it is faster
ifeq ($(shell mamba 2> /dev/null || echo 0), 0)
	CONDA_CMD = conda
else
	CONDA_CMD = mamba
endif

default:
	$(BUILD_CMD)

debug:
	CYTHON_DEBUG=1 $(BUILD_CMD)

# Build Cython extensions with the CYTHON_TRACE flag enabled to allow coverage tracking.
coverage:
	CYTHON_COVERAGE=1 $(BUILD_CMD)

clean:
	if [ -d builddir ];then \
		find builddir -type f -name "*.[ch]" -delete ; \
		find builddir -type d -empty -delete ;\
	fi
	find . -name "*.so" -type f -delete
	find . -name "*.dll" -type f -delete
	find . -name "*.pyd" -type f -delete

realclean: clean
	git clean -fX

# Install Finesse as a local package.
install-pep517:
	python -m pip install .

# Install Finesse as a local package (within conda environment, which provides all of the
# required dependencies).
install-conda:
	python -m pip install . --no-build-isolation --no-deps

# See https://gitlab.com/ifosim/finesse/finesse3/-/issues/438
# See https://gitlab.com/ifosim/finesse/finesse3/-/issues/463
# Use this to compile and install finesse into the current environment in a development mode
develop-windows:
	$(BUILD_CMD)
	python setup.py develop

# Use this to compile and install finesse into the current environment
install-windows:
	$(BUILD_CMD)
	python setup.py install --no-compile

# Install/reinstall Finesse as a local editable package.
develop-pep517:
	# Build using the PEP 517 build backend. Build dependencies must be already
	# available on the current system (system build dependencies, e.g. SuiteSparse) or
	# installable by pip via PyPI (Python build dependencies, e.g. Cython).
	python -m pip install -e .[test,docs,lint,inplacebuild]

conda-update:
	# Update the current conda environment with the appropriate environment file
	$(CONDA_CMD) env update --solver libmamba -f $(CONDA_YML)

# Install/reinstall Finesse as a local editable package (within conda environment).
develop-conda: conda-update
	# Build in-tree, using dependencies provided by the conda environment.
	python -m pip install -e . --no-build-isolation --no-deps
