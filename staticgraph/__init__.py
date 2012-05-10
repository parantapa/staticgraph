from staticgraph.digraph import load

try:
    from staticgraph.cDigraph import make
except ImportError:
    from warnings import warn

    warn("using slower version of make ...")
    from staticgraph.digraph import make
