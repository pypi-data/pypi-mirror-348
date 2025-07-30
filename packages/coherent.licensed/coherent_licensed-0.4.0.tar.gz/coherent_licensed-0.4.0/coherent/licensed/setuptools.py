import contextlib
import functools
import pathlib
import warnings

from . import resolve


def do_nothing(*args, **kwargs):
    return None


def if_depended(func):
    with contextlib.suppress(FileNotFoundError):
        project = pathlib.Path('pyproject.toml').read_text(encoding='utf-8')
        if 'coherent.licensed' in project:
            return func
    warnings.warn("Avoid installing this plugin for projects that don't depend on it.")
    return do_nothing


def _finalize_license_files(dist):
    """
    Resolve the license expression into a license file.
    """
    license = pathlib.Path('LICENSE')
    dist.metadata.license_files = [str(license)]
    if license.exists():
        return
    license.write_text(resolve(dist.metadata.license_expression))


@if_depended
def inject(dist):
    """
    Patch the dist to resolve the license expression.

    This hook is called before `dist.parse_config_files` has been called, so
    the license expression has not been loaded yet, so patch _finalize_license_files
    to write out the license after expressions are loaded.
    """
    dist._finalize_license_files = functools.partial(_finalize_license_files, dist)
