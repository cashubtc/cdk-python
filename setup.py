"""Setup script for cdk-python binary distribution."""

from setuptools import setup


def has_ext_modules(self):
    """Indicate that this package has binary extensions."""
    return True


# Monkey patch to indicate we have binary extensions
# This ensures platform-specific wheel tags are generated
setup.__class__.has_ext_modules = has_ext_modules

setup()
