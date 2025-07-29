"""JAX TPU Embedding versioning utilities

For releases, the version is of the form:
  xx.yy.zz

For nightly builds, the date of the build is added:
  xx.yy.zz-devYYYMMDD
"""

_base_version = "0.1.0"
_version_suffix = "dev20250516"

# Git commit corresponding to the build, if available.
__git_commit__ = "2d0481f090796a29004dc74ef5bcda2a0e9c0a90"

# Library version.
__version__ = _base_version + _version_suffix

