"""
Ctypes for storing numpy arrays

Corresponds directly with types.py
"""

cimport numpy as np

ctypedef np.uint32_t NODE_t  # Node type
ctypedef np.uint64_t NODE2_t # Two nodes in one
ctypedef np.uint64_t INDEX_t # Index type

