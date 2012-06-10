from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from numpy import get_include

ext_modules = [
    Extension("staticgraph.make_digraph", ["staticgraph/make_digraph.pyx"],
              include_dirs=[get_include()]),
    Extension("staticgraph.merge_digraph", ["staticgraph/merge_digraph.pyx"],
              include_dirs=[get_include()]),
    Extension("staticgraph.sub_digraph", ["staticgraph/sub_digraph.pyx"],
              include_dirs=[get_include()]),
    ]

packages = ["staticgraph", "staticgraph.algorithms"]

setup(name = "StaticGraph",
      version = "0.54a",
      packages = packages,
      ext_modules = ext_modules,
      cmdclass = {'build_ext': build_ext}
      )
