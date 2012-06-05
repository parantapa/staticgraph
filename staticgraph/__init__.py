from warnings import warn

from staticgraph.digraph import load as load_digraph
from staticgraph.make_digraph import make as make_digraph
from staticgraph.manip_digraph import merge as merge_digraph
from staticgraph.manip_digraph import subgraph as sub_digraph

from staticgraph.link_analysis import hits

# The following is really curft code that I havent had chance to update
try:
    from staticgraph.cGraph import make as make_graph
except ImportError:
    warn("using slower version of make for graph ...")
    from staticgraph.graph import make as make_graph
from staticgraph.graph import load as load_graph

