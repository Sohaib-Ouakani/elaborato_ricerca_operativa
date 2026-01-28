from graph import Graph
from ford_fulkerson.residual import ford_fulkerson_residual
from ford_fulkerson.labeling import ford_fulkerson_labeling
from latex import tikz_graph


def build_example_graph():
    """
    Esempio semplice dal PDF
    """
    G = Graph()
    G.add_edge(1, 2, 3)
    G.add_edge(1, 3, 4)
    G.add_edge(2, 3, 1)
    G.add_edge(2, 4, 2)
    G.add_edge(3, 4, 5)
    return G


if __name__ == "__main__":

    print("=== FORD–FULKERSON (GRAFO RESIDUO) ===")
    G1 = build_example_graph()
    value, iters = ford_fulkerson_residual(G1, 1, 4)

    print("Flusso massimo:", value)
    for k, it in enumerate(iters, 1):
        print(f"\nIterazione {k}")
        print("Cammino:", it["path"])
        print("Delta:", it["delta"])
        print(tikz_graph(G1, it["path"]))

    print("\n=== FORD–FULKERSON (ETICHETTAMENTO) ===")
    G2 = build_example_graph()
    value, iters = ford_fulkerson_labeling(G2, 1, 4)

    print("Flusso massimo:", value)
