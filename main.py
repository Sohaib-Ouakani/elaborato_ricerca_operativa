from graph import Graph
from ford_fulkerson.residual import ford_fulkerson_residual
from ford_fulkerson.labeling import ford_fulkerson_labeling
from latex import tikz_graph, tikz_graph_labels


def build_example_graph():
    """
    Esempio semplice dal PDF
    """
    G = Graph()
    # Example 1
    # G.add_edge(1, 2, 2)
    # G.add_edge(1, 3, 4)
    # G.add_edge(2, 3, 3)
    # G.add_edge(2, 4, 1)
    # G.add_edge(3, 4, 5)

    # G.add_edge(1, 2, 14)
    # G.add_edge(1, 4, 23)
    # G.add_edge(2, 4, 9)
    # G.add_edge(4, 5, 26)
    # G.add_edge(5, 2, 11)
    # G.add_edge(2, 3, 10)
    # G.add_edge(3, 5, 12)
    # G.add_edge(5, 7, 4)
    # G.add_edge(5, 6, 25)
    # G.add_edge(3, 8, 18)
    # G.add_edge(6, 8, 8)
    # G.add_edge(6, 7, 7)
    # G.add_edge(8, 9, 20)
    # G.add_edge(7, 9, 15)

    #esempio esame
    G.add_edge(1, 2,5)
    G.add_edge(1, 3,9)
    G.add_edge(3, 2,5)
    G.add_edge(3, 4,2)
    G.add_edge(3, 6,4)
    G.add_edge(2, 4,2)
    G.add_edge(2, 5,5)
    G.add_edge(4, 5,2)
    G.add_edge(4, 6,2)
    G.add_edge(5, 6,3)
    G.add_edge(5, 7,2)
    G.add_edge(5, 8,5)
    G.add_edge(6, 7,2)
    G.add_edge(6, 9,4)
    G.add_edge(7, 8,3)
    G.add_edge(7, 9,3)
    G.add_edge(8, 10,7)
    G.add_edge(9, 8,6)
    G.add_edge(9, 10,7)
    return G

def latex_boilerplate():
    print("""\\documentclass{article}
    \\usepackage{graphicx} % Required for inserting images
    \\usepackage{tikz}
    \\usetikzlibrary{arrows.meta, positioning}

    \\tikzset{every picture/.style={>=Stealth, x=1.6cm, y=1.2cm}}

    \\title{ricerca_operativa}
    \\author{}
    \\date{January 2026}

    \\begin{document}\n""")


if __name__ == "__main__":

    print("=== FORD–FULKERSON (GRAFO RESIDUO) ===")
    G1 = build_example_graph()
    value, iters, S, T = ford_fulkerson_residual(G1, 1, 10)

    print("Flusso massimo:", value, "\nS: ", S, "T: ", T)
    latex_boilerplate()
    for k, it in enumerate(iters, 1):
        print(f"\nIterazione {k}")
        print("Cammino:", it["path"])
        print("Delta:", it["delta"])
        print("\\\\")
        print(tikz_graph(G1, it["path"], it["flow"]))
    print("\\end{document}\n")

    print("\n=== FORD–FULKERSON (ETICHETTAMENTO) ===")
    G2 = build_example_graph()
    value, iters, S, T = ford_fulkerson_labeling(G2, 1, 10)

    print("Flusso massimo:", value, "\nS: ", S, "T: ", T)
    latex_boilerplate()
    for k, it in enumerate(iters, 1):
        print(f"\nIterazione {k}")
        print("Cammino:", it["path"])
        print("Delta:", it["delta"])
        print("\\\\")
        print(tikz_graph_labels(G2, it["labels"], it["flow"]))
    print("\\end{document}\n")
