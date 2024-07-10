from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in eyeplus/__init__.py
from eyeplus import __version__ as version

setup(
	name="eyeplus",
	version=version,
	description="Eyeplus",
	author="Eyeplus",
	author_email="Eyeplus",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
