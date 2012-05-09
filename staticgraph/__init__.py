from staticgraph.digraph import load

try:
    from staticgraph.cDigraph import make
except ImportError:
    print "Failed to import fast version"

    from staticgraph.digraph import make
