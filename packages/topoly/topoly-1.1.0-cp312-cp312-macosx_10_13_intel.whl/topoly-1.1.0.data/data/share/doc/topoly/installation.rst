.. installation:

Topoly requirements
=======================

Topoly is supported on the following Operating Systems:

* Linux 64 bit - for example RedHat/Centos 7 or newer, Ubuntu 18.04 or newer
* Intel-based (x86_64) Mac: Mac OS X 10.10 or higher
* M1/M2 (Apple Silicon - arm64) Mac: Mac OS X 12.0 or higher
    * No GPU acceleration (On Linux and Intel-based Mac it is available for the Alexander polynomial applied to matrix calculations)
* Windows 64 bit (Windows 10 or later) - supported but with limitations:
    * No GPU (CUDA) acceleration
    * The HOMFLY-PT polynomial has a limited functionality

The Topoly PyPI packages contain both Python code as well as executable
binaries and compiled shared libraries written in C and C++. Some algorithms,
Alexander, in particular, have two implementations, one of which is faster but
requires a CUDA compatible GPU and the CUDA framework version 7.5 or newer. The
PyPI packages for Linux are built following the ManyLinux2014 specification
that imposes the requirement of compatibility with Linux systems starting with
CentOS 7, so most modern distributions are supported. Topoly packages for Intel-based
(x86_64) Macs are built on Mac OS 10.10 Yosemite so this is the oldest version of Mac OS X
supported. The M1/M2 (Apple Silicon) arm64 packages are built on Mac OS 12.0 Monterey and available for Python 3.[8-11]
Both Linux and Intel-based Mac OS X packages are available for Python 3, in particular for
versions 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12 and 3.13 (>=3.11 are not available for Intel-based Mac).
The Windows packages are built on Windows 10 64 Bit using MinGW but since they contain statically
compiled c++ code, they should run on any Windows 10/11 installation.

Python 2.x is not supported!

The Topoly Python modules require the following dependent packages to be 
installed: matplotlib>=3.0.0, numpy>=1.15, argparse>=1.4, biopython>1.60, 
scipy>1.0.0. In case Topoly is installed using pip, these dependencies should 
be installed automatically. Since version 1.1.0 topoly supports also numpy 2.x.


Package structure
======================

PyPI packages can be installed in Python virtual environments such as venv
or virtualenv. This is the RECOMMENDED way of installing topoly.
In that case Python modules, executables and libraries will be
found in folders relative to the main directory of the virtual environment.

All available versions of packages contain:

* Python modules that should be installed to the relevant Python 3 modules 
  location::

        $USER/.local/lib/python3.x/site-packages

  in case of an installation run by a specific user or::

        /usr/local/lib/python3.x/site-packages

  in case the installation is run by the administrator

* Executables and shared libraries that should be installed in::

        $USER/.local/bin
        $USER/.local/lib

  or::

        /usr/local/bin
        /usr/local/lib

* Documentation and test examples available in::

        $USER/.local/share/doc/topoly

  or::

        /usr/local/share/doc/topoly

