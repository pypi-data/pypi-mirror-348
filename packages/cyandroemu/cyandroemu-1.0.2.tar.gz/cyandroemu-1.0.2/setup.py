from setuptools import setup, find_packages
import codecs
import os
#
here = os.path.abspath(os.path.dirname(__file__))
#
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

VERSION = '''1.0.2'''
DESCRIPTION = '''Very fast Android automation framework with 7 backends (uiautomator 1+2, fragment parser, window dump ...)'''

# Setting up
setup(
    name="cyandroemu",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/cyandroemu',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['Cython', 'numpy', 'pandas', 'regex', 'requests', 'setuptools', 'sheller'],
    keywords=['android', 'bot', 'uiautomator', 'magisk', 'kernelsu'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['Cython', 'numpy', 'pandas', 'regex', 'requests', 'setuptools', 'sheller'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*