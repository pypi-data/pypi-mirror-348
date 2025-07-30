"""Plugin for Solidipes with solid mechanics components"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("solidipes_solid_mech_plugin")
except PackageNotFoundError:
    pass
