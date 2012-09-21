from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from numpy import get_include

ext_modules = [
    Extension("staticgraph._edgelist", ["staticgraph/_edgelist.pyx"],
              include_dirs=[get_include()]),
]

packages = ["staticgraph"]

setup(name = "StaticGraph",
      version = "0.1a",
      packages = packages,
      ext_modules = ext_modules,
      cmdclass = {'build_ext': build_ext}
)
