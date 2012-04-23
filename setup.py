from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from numpy import get_include

ext_modules = [
    Extension("largegraph.cDigraph", ["largegraph/cDigraph.pyx"],
              include_dirs=[get_include()])
    ]

packages = ["largegraph"]

setup(name = "LargeGraph",
      version = "0.1a",
      packages = packages,
      ext_modules = ext_modules,
      cmdclass = {'build_ext': build_ext}
      )
