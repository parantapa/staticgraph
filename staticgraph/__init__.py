from warnings import warn

from staticgraph.make_digraph import make as make_digraph
from staticgraph.digraph import load as load_digraph

try:
    from staticgraph.cGraph import make as make_graph
except ImportError:
    warn("using slower version of make for graph ...")
    from staticgraph.graph import make as make_graph
from staticgraph.graph import load as load_graph

