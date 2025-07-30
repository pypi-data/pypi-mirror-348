from setuptools import setup, find_packages

setup(
    name="blackbit",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,              # use MANIFEST.in or package_data
    package_data={
        "blackbit_pkg": ["data/blackbit.exe"],  
    },
    entry_points={
        "console_scripts": [
            "blackbit = blackbit_pkg.launcher:main",
        ],
    },
    author="Your Name",
    description="BlackBit standalone tool",
)
