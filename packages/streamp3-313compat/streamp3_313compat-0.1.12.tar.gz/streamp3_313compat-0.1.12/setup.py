import setuptools
from distutils.core import setup
from distutils.extension import Extension
import os # Import the os module

# Get the directory of the setup.py file
# This is a robust way to specify paths relative to the setup file
setup_dir = os.path.dirname(os.path.abspath(__file__))

setup(name='streamp3-313compat',
      version='0.1.12',
      description="streaming mp3 decoder",
      long_description=open('README.md', 'r').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/benjie-git/streamp3-313compat/',
      author="Brent M. Spell",
      author_email='brent@pylon.com',
      packages=setuptools.find_packages(),
      setup_requires=['Cython'],
      install_requires=['Cython'],
      ext_modules=[Extension('lame.hip',
                             ['lame/hip.pyx'],
                             libraries=['mp3lame'],
                             include_dirs=[setup_dir, setup_dir+"/lame"])], # Use setup_dir for robustness
      classifiers=["Programming Language :: Python :: 3",
                   "Operating System :: OS Independent"])
