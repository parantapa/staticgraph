"""
Ctypes for storing numpy arrays

Corresponds directly with types.py
"""

cimport numpy as np

ctypedef np.uint32_t NTYPE_t
ctypedef np.uint64_t ATYPE_t
ctypedef np.uint64_t ETYPE_t

