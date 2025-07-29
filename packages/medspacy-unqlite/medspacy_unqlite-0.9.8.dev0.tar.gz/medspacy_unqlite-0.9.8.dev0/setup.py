
import sys
import warnings

from setuptools import setup
from setuptools.extension import Extension
try:
    from Cython.Build import cythonize
except ImportError:
    cython_installed = False
    warnings.warn('Cython not installed, using pre-generated C source file.')
else:
    cython_installed = True


if cython_installed:
    python_source = 'unqlite.pyx'
else:
    python_source = 'unqlite.c'
    cythonize = lambda obj: obj

if sys.platform.find('win') < 0:
    libs = ['pthread']
else:
    libs = []

library_source = ['src/unqlite.c']
unqlite_extension = Extension(
    'unqlite',
    define_macros=[('UNQLITE_ENABLE_THREADS', '1')],
    libraries=libs,
    sources=[python_source] + library_source)

setup(
    ext_modules=cythonize([unqlite_extension])
)