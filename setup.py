from setuptools import setup
import re

DESCRIPTION = 'InputMaker'
LONG_DESCRIPTION = 'Tool to assist in the creation of input files for several ab-initio codes.'
AUTHOR = 'Pablo Gila-Herranz'
AUTHOR_EMAIL = 'pgila001@ikasle.ehu.eus'

def get_version():
    with open('inputmaker/common.py', 'r') as file:
        content = file.read()
        version_match = re.search(r"version\s*=\s*'([^']+)'", content)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version.")

setup(
        name="inputmaker", 
        version=get_version(),
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['inputmaker'],
        install_requires=['ase'],
        license='AGPL-3.0',
        keywords=['python', 'inputmaker', 'DFT', 'Density Functional Theory', 'MD', 'Molecular Dynamics'],
        classifiers= [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: Other OS",
        ]
)
