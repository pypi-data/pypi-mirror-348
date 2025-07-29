import functools
import pathlib

from . import resolve


def _finalize_license_files(dist):
    """
    Resolve the license expression into a license file.
    """
    license = pathlib.Path('LICENSE')
    dist.metadata.license_files = [str(license)]
    if license.exists():
        return
    license.write_text(resolve(dist.metadata.license_expression))


def inject(dist):
    """
    Patch the dist to resolve the license expression.

    This hook is called before `dist.parse_config_files` has been called, so
    the license expression has not been loaded yet, so patch _finalize_license_files
    to write out the license after expressions are loaded.
    """
    dist._finalize_license_files = functools.partial(_finalize_license_files, dist)
