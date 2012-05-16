from warnings import warn

from staticgraph.digraph import load as load_digraph
from staticgraph.graph import load as load_graph

try:
    from staticgraph.cDigraph import make as make_digraph
except ImportError:
    warn("using slower version of make for digraph ...")
    from staticgraph.digraph import make as make_digraph

try:
    from staticgraph.cGraph import make as make_graph
except ImportError:
    warn("using slower version of make for graph ...")
    from staticgraph.graph import make as make_graph

