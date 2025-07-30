# setup.py
#
# Usage:
#    python setup.py build_ext --inplace

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension
from setuptools import setup

CYTHON_MODULES = [
    'ck.circuit.circuit',
    'ck.pgm_compiler.support.circuit_table.circuit_table',
    'ck.circuit_compiler.cython_vm_compiler._compiler'
]

NP_INCLUDES = np.get_include()

CYTHON_EXTENSIONS = [
    Extension(
        module,
        ['src/' + module.replace('.', '/') + '.pyx'],
        include_dirs=[NP_INCLUDES],
    )
    for module in CYTHON_MODULES
]

setup(ext_modules=cythonize(CYTHON_EXTENSIONS))
