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

PACKAGE_SOURCE = {
    module: ['src/' + module.replace('.', '/') + '.pyx']
    for module in CYTHON_MODULES
}

PACKAGE_DATA = {
    module: [module.split('.')[-1] + '.pyx']
    for module in CYTHON_MODULES
}

NP_INCLUDES = np.get_include()

CYTHON_EXTENSIONS = [
    Extension(
        module,
        PACKAGE_SOURCE[module],
        include_dirs=[NP_INCLUDES],
        define_macros=[('NPY_NO_DEPRECATED_API', 1)],
        extra_compile_args=['-Wno-unreachable-code'],
    )
    for module in CYTHON_MODULES
]

setup(
    ext_modules=cythonize(CYTHON_EXTENSIONS),
    package_data=PACKAGE_DATA,
    include_package_data=True,
    quiet=True,
)
