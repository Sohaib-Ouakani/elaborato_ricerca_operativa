from collections import defaultdict

class Graph:
    """
    Grafo diretto con capacità e flussi.
    Rispetta l'assunzione:
    se (i,j) ∈ A allora anche (j,i) ∈ A (con capacità eventualmente nulla)
    """

    def __init__(self):
        self.cap = defaultdict(dict)   # capacità u_ij
        self.flow = defaultdict(dict)  # flusso x_ij
        self.nodes = set()

    def add_edge(self, i, j, capacity):
        self.cap[i][j] = capacity
        self.flow[i][j] = 0

        # arco inverso
        if i not in self.cap[j]:
            self.cap[j][i] = 0
            self.flow[j][i] = 0

        self.nodes.add(i)
        self.nodes.add(j)
