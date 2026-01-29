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
        """
        Aggiunge un arco diretto dal nodo i al nodo j con una data capacità.

        Parametri:
        - i: nodo sorgente dell'arco
        - j: nodo destinazione dell'arco
        - capacity: capacità massima dell'arco (u_ij)

        Questa funzione:
        1. Crea l'arco diretto (i,j) con la capacità specificata
        2. Inizializza il flusso a 0 (nessun flusso all'inizio)
        3. Crea automaticamente l'arco inverso (j,i) se non esiste,
           con capacità 0 (necessario per l'algoritmo di Ford-Fulkerson)
        4. Aggiunge i nodi i e j al set dei nodi del grafo
        """
        self.cap[i][j] = capacity
        self.flow[i][j] = 0

        # arco inverso
        if i not in self.cap[j]:
            self.cap[j][i] = 0
            self.flow[j][i] = 0

        self.nodes.add(i)
        self.nodes.add(j)
