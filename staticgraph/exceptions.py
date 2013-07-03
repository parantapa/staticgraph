"""
Exception classes for staticgraph.
"""
class StaticGraphException(Exception):
    """
    Base exception class for StaticGraphs
    """

class StaticGraphNotEqNodesException(StaticGraphException):
    """
    Subclass of StaticGraphException for
    inequality between node sets of two graphs
    """

class StaticGraphNodeAbsentException(StaticGraphException):
    """
    Subclass of StaticGraphException class for
    absence of a specific node.
    """

class StaticGraphDisconnectedGraphException(StaticGraphException):
    """
    Subclass of StaticGraphException class for
    handling unexpected disconnected graphs.
    """
