from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("fs-comfyui-frontend-package")
except PackageNotFoundError:
    __version__ = "unknown"
