from setuptools import setup

setup(
    name="QFM",
    version="0.1.1",
    long_description="QFM",
    long_description_content_type="text/markdown",
    packages=["qfm"],
    install_requires=["numpy",  "h5py", "matplotlib", "pandas"],
)
