"""
Basic data types for the graph structures
"""

__author__  = "Parantapa Bhattacharya <pb@parantapa.net>"

__all__ = ["NTYPE", "ATYPE", "ETYPE"]

import numpy as np

NTYPE = np.uint32       # Type for node ids
ATYPE = np.uint64       # Type for arc ids
ETYPE = np.uint64       # Type for edgelists

