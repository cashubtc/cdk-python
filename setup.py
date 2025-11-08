"""Setup script for cdk-python binary distribution."""

from setuptools import setup, Distribution


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name."""

    def has_ext_modules(self):
        """Indicate that this package has binary extensions.

        This ensures platform-specific wheel tags are generated even though
        the extensions are pre-built Rust libraries rather than being built
        during the wheel creation process.
        """
        return True


setup(distclass=BinaryDistribution)
