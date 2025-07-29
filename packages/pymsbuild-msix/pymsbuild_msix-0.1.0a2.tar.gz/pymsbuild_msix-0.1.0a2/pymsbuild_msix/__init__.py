from . import _types
from ._types import *

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.1"

try:
    NEXT_INCOMPATIBLE_VERSION = "{}.0".format(int(__version__.partition(".")[0]) + 1)
    PYMSBUILD_REQUIRES_SPEC = f"pymsbuild-msix>={__version__},<{NEXT_INCOMPATIBLE_VERSION}"
except ValueError:
    PYMSBUILD_REQUIRES_SPEC = "pymsbuild-msix"


def build(buildstate):
    "Build an MSIX"
    from ._build import do_build
    return do_build(buildstate)


def pack(buildstate):
    "Pack an MSIX previously built with --layout-dir set."
    from ._build import do_pack
    return do_pack(buildstate)

__all__ = ["build", *_types.__all__]
