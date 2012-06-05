from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from numpy import get_include

ext_modules = [
    Extension("staticgraph.make_digraph", ["staticgraph/make_digraph.pyx"],
              include_dirs=[get_include()]),
    Extension("staticgraph.cGraph", ["staticgraph/cGraph.pyx"],
              include_dirs=[get_include()])
    ]

packages = ["staticgraph", "staticgraph.algorithms"]

setup(name = "StaticGraph",
      version = "0.53a",
      packages = packages,
      ext_modules = ext_modules,
      cmdclass = {'build_ext': build_ext}
      )
