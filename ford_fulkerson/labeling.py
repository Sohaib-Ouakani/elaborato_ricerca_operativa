from collections import defaultdict

def min_cut_from_residual(G, s):
    """
    Calcola il taglio minimo (S,T) a partire dal grafo G e dal suo flusso corrente.

    Questa funzione è simile a quella in residual.py, ma costruisce il grafo
    residuo internamente invece di riceverlo come parametro.

    Il TAGLIO MINIMO divide i nodi in due insiemi:
    - S: nodi raggiungibili dalla sorgente s nel grafo residuo
    - T: nodi non raggiungibili da s nel grafo residuo

    Alla fine dell'algoritmo di Ford-Fulkerson, questo taglio ha capacità
    uguale al flusso massimo (teorema del taglio minimo - flusso massimo).

    Parametri:
    - G: oggetto Graph con capacità e flussi
    - s: nodo sorgente

    Ritorna:
    - S: set di nodi raggiungibili da s
    - T: set di nodi non raggiungibili da s
    """

    # costruisco il grafo residuo
    R = defaultdict(dict)
    for i in G.cap:
        for j in G.cap[i]:
            u = G.cap[i][j]
            x = G.flow[i][j]
            # arco diretto
            if u - x > 0:
                R[i][j] = u - x
            # arco inverso
            if x > 0:
                R[j][i] = x

    # DFS per trovare nodi raggiungibili da s
    visited = set()
    stack = [s]
    while stack:
        node = stack.pop()
        visited.add(node)
        for nxt in R[node]:
            if nxt not in visited and R[node][nxt] > 0:
                stack.append(nxt)

    S = visited
    T = set(G.cap.keys()) - S
    return S, T

def ford_fulkerson_labeling(G, s, t):
    """
    Algoritmo di Ford-Fulkerson per il FLUSSO MASSIMO usando il metodo dell'ETICHETTAMENTO.

    Questa è una variante dell'algoritmo di Ford-Fulkerson che usa una tecnica
    chiamata "etichettamento" (labeling) invece di costruire esplicitamente
    il grafo residuo ad ogni iterazione.

    METODO DELL'ETICHETTAMENTO:
    Invece di costruire il grafo residuo, questa versione etichetta i nodi
    durante la ricerca del cammino aumentante con due informazioni:

    1. PRED (predecessore):
       - pred[j] = i se j è raggiunto tramite l'arco diretto i→j
       - pred[j] = -i se j è raggiunto tramite l'arco inverso j→i
       - Il segno indica la direzione dell'arco utilizzato

    2. DELTA (capacità residua):
       - delta[j] = capacità residua minima dal nodo sorgente s al nodo j
       - Questo è il massimo flusso che può attraversare il cammino fino a j

    Questa tecnica permette di:
    - Ricostruire il cammino aumentante risalendo i predecessori
    - Conoscere subito quanto flusso possiamo inviare (il delta al pozzo t)
    - Evitare di costruire esplicitamente il grafo residuo

    Parametri:
    - G: oggetto Graph con capacità e flussi
    - s: nodo sorgente
    - t: nodo pozzo

    Ritorna:
    - value: valore del flusso massimo
    - iterations: lista di dettagli per ogni iterazione
    - S, T: taglio minimo
    """
    value = 0
    iterations = []
    S = None
    T = None

    while True:
        pred = {}
        delta = {s: float("inf")}
        expanded = set()
        queue = [s]

        # fase di etichettamento
        while queue and t not in pred:
            i = queue.pop(0)
            expanded.add(i)

            # archi diretti
            for j in G.cap[i]:
                if j not in pred and G.flow[i][j] < G.cap[i][j]:
                    pred[j] = i
                    delta[j] = min(delta[i], G.cap[i][j] - G.flow[i][j])
                    queue.append(j)

            # archi inversi
            for j in G.cap:
                if i in G.cap[j] and j not in pred and G.flow[j][i] > 0:
                    pred[j] = -i
                    delta[j] = min(delta[i], G.flow[j][i])
                    queue.append(j)

        if t not in pred:
            break

        d = delta[t]
        value += d

        # ricostruzione cammino
        path = [t]
        j = t
        while j != s:
            j = abs(pred[j])
            path.append(j)
        path.reverse()

        # aggiornamento flussi
        j = t
        while j != s:
            p = pred[j]
            i = abs(p)
            if p > 0:
                G.flow[i][j] += d
            else:
                G.flow[j][i] -= d
            j = i


        iterations.append({
            "labels": {
                v: {
                    "pred": pred[v],
                    "delta": delta[v]
                }
                for v in pred
            },
            "path": path,
            "delta": d,
            "flow": {i: dict(G.flow[i]) for i in G.flow}
        })
    # calcolo taglio minimo residuo
    S, T = min_cut_from_residual(G, s)

    return value, iterations, S, T
