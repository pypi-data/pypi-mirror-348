from setuptools import setup, find_packages

setup(
    name='pyvfp64',
    version='0.0.6.1',
    description='A Python wrapper for vfp_to_json.exe to convert VFP data to pandas DataFrame',
    author='Lewis Morris',
    author_email='lewis@arched.dev',
    packages=find_packages(exclude=['pyvfp64.bin']),  # Exclude the bin folder from being treated as a package
    include_package_data=True,
    package_data={
        'pyvfp64': ['bin/vfp_to_json.exe'],  # Include the exe file as package data
    },
    install_requires=[
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
    ],
    python_requires='>=3.6',
)
