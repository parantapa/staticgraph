"""
Exception classes for staticgraph.
"""
class StaticGraphException(Exception):
    """
    Base exception class for StaticGraphs
    """

class StaticGraphNotEqNodesException(StaticGraphException):
    """
    Subclass of StaticGraphException class to check equality
    between node sets of two graphs
    """
