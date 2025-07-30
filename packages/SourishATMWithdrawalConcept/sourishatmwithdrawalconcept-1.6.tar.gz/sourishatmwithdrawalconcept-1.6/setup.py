import pathlib
import setuptools

setuptools.setup(
    name='SourishATMWithdrawalConcept',
    version='1.6',
    description=pathlib.Path('README.md').read_text(),
    packages=setuptools.find_packages(exclude=["tests","data"]),
)