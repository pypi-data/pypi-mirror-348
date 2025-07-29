import os
import subprocess
from setuptools import setup, find_packages, Command

class MakeBuild(Command):
    description = "Build the C++ shared library using Makefile"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Run make in the src directory.
        cwd = os.path.join(os.path.dirname(__file__), "src")
        subprocess.check_call(["make", "clean"], cwd=cwd)
        subprocess.check_call(["make"], cwd=cwd)
        # Optionally, copy the built shared library into the package folder.
        # For example:
        target = os.path.join(os.path.dirname(__file__), "co2_potential", "libCO2CO2.so")
        src_lib = os.path.join(cwd, "libCO2CO2.so")
        if os.path.exists(src_lib):
            import shutil
            shutil.copy(src_lib, target)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="co2_potential",
    version="0.3.1",
    author="Olaseni Sode",
    license="MIT",
    author_email="osode@calstatela.edu",
    description="A Python package interfacing with the CO2CO2 shared library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # Include the shared library in the co2_potential package.
        "co2_potential": ["libCO2CO2.so"],
    },
    cmdclass={
        "build_ext": MakeBuild,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires=">=3.6",
)