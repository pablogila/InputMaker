from setuptools import setup
import re

DESCRIPTION = 'Thoth'
LONG_DESCRIPTION = "'Text Handling & Optimization Toolkit Helper', or Thoth, is a tool to assist in the creation, modification and analysis of text files, with a special focus in (but not limited to) ab-initio calculations."
AUTHOR = 'Pablo Gila-Herranz'
AUTHOR_EMAIL = 'pgila001@ikasle.ehu.eus'

def get_version():
    with open('thoth/__init__.py', 'r') as file:
        content = file.read()
        version_match = re.search(r"version\s*=\s*'([^']+)'", content)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version.")

setup(
        name="thoth", 
        version=get_version(),
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['thoth'],
        install_requires=['pandas'],
        license='AGPL-3.0',
        keywords=['python', 'thoth', 'text', 'inputmaker', 'DFT', 'Density Functional Theory', 'MD', 'Molecular Dynamics'],
        classifiers= [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: Other OS",
        ]
)
