from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from numpy import get_include

ext_modules = [
    Extension("staticgraph.graph_edgelist",
              ["staticgraph/graph_edgelist.pyx"],
              include_dirs=[get_include()]),
    Extension("staticgraph.links",
              ["staticgraph/links.pyx"],
              include_dirs=[get_include()]),
    Extension("staticgraph.components",
              ["staticgraph/components.pyx"],
              include_dirs=[get_include()]),
]

packages = ["staticgraph"]

setup(
    name        = "StaticGraph",
    version     = "0.1",
    packages    = packages,
    ext_modules = ext_modules,
    cmdclass    = {'build_ext': build_ext}
)
