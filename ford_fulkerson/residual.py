from collections import defaultdict

def build_residual_graph(G):
    """
    Costruisce il grafo residuo G(x) a partire dal grafo G e dal suo flusso corrente.

    Il GRAFO RESIDUO è un concetto fondamentale nell'algoritmo di Ford-Fulkerson:
    rappresenta la "capacità residua" disponibile su ogni arco, considerando
    il flusso già presente.

    Per ogni arco (i,j) del grafo originale, il grafo residuo può contenere:

    1. ARCO DIRETTO (i→j) con capacità residua = u_ij - x_ij
       - Rappresenta quanto flusso AGGIUNTIVO possiamo ancora inviare
       - Esiste solo se u_ij - x_ij > 0 (c'è ancora capacità disponibile)

    2. ARCO INVERSO (j→i) con capacità residua = x_ij
       - Rappresenta quanto flusso possiamo "annullare" riducendo il flusso su (i,j)
       - Esiste solo se x_ij > 0 (c'è flusso da poter ridurre)

    Parametri:
    - G: oggetto Graph contenente cap (capacità) e flow (flusso corrente)

    Ritorna:
    - R: dizionario di dizionari rappresentante il grafo residuo
         R[i][j] = capacità residua dell'arco i→j
    """

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

    return R


def find_augmenting_path(R, s, t):
    """
    Trova un cammino aumentante nel grafo residuo usando Depth-First Search (DFS).

    Un CAMMINO AUMENTANTE è un cammino dalla sorgente s al pozzo t nel grafo
    residuo R, lungo il quale possiamo inviare flusso aggiuntivo.

    L'algoritmo usa DFS per esplorare il grafo:
    - Parte dalla sorgente s
    - Esplora in profondità fino a raggiungere t o esaurire le possibilità
    - Tiene traccia del DELTA, cioè la capacità residua minima lungo il cammino
      (questo determina quanto flusso possiamo inviare)

    Parametri:
    - R: grafo residuo (dizionario di dizionari)
    - s: nodo sorgente
    - t: nodo pozzo (destinazione)

    Ritorna:
    - path: lista di nodi che formano il cammino da s a t
            None se non esiste un cammino
    - delta: capacità residua minima lungo il cammino
             (quanto flusso possiamo inviare lungo questo cammino)
             0 se non esiste un cammino
    """
    stack = [(s, [s], float("inf"))]
    visited = set()

    while stack:
        node, path, delta = stack.pop()

        if node == t:
            return path, delta

        visited.add(node)

        for nxt in R[node]:
            if nxt not in visited and R[node][nxt] > 0:
                stack.append((
                    nxt,
                    path + [nxt],
                    min(delta, R[node][nxt])
                ))

    return None, 0

def min_cut_from_residual(R, s):
    """
    Calcola il taglio minimo (S,T) a partire dal grafo residuo R.

    Il TEOREMA DEL TAGLIO MINIMO - FLUSSO MASSIMO afferma che:
    "Il valore del flusso massimo è uguale alla capacità del taglio minimo"

    Un TAGLIO (S,T) è una partizione dei nodi in due insiemi:
    - S contiene la sorgente s
    - T contiene il pozzo t
    - Nessun nodo appartiene sia a S che a T
    - S ∪ T = insieme di tutti i nodi

    La CAPACITÀ DI UN TAGLIO è la somma delle capacità degli archi che vanno da S a T.

    Alla fine dell'algoritmo di Ford-Fulkerson:
    - S = nodi raggiungibili da s nel grafo residuo
    - T = nodi NON raggiungibili da s nel grafo residuo
    - Questo taglio è il taglio minimo e ha capacità uguale al flusso massimo

    Parametri:
    - R: grafo residuo finale (quando non esistono più cammini aumentanti)
    - s: nodo sorgente

    Ritorna:
    - S: set di nodi raggiungibili da s (contiene s)
    - T: set di nodi non raggiungibili da s (contiene t)
    """
    visited = set()
    stack = [s]

    while stack:
        node = stack.pop()
        visited.add(node)
        for nxt in R[node]:
            if nxt not in visited and R[node][nxt] > 0:
                stack.append(nxt)

    S = visited
    T = set(R.keys()) - S
    return S, T


def ford_fulkerson_residual(G, s, t):
    """
    Algoritmo di Ford-Fulkerson per il problema del FLUSSO MASSIMO.
    Versione che costruisce esplicitamente il grafo residuo.

    PROBLEMA DEL FLUSSO MASSIMO:
    Dato un grafo diretto con capacità sugli archi, una sorgente s e un pozzo t,
    trovare il massimo flusso che può essere inviato da s a t rispettando:
    1. Vincoli di capacità: 0 ≤ x_ij ≤ u_ij per ogni arco (i,j)
    2. Conservazione del flusso: per ogni nodo (eccetto s e t),
       il flusso in entrata = flusso in uscita

    ALGORITMO DI FORD-FULKERSON:
    1. Inizia con flusso zero su tutti gli archi
    2. Finché esiste un cammino aumentante da s a t nel grafo residuo:
       a. Trova un cammino aumentante e calcola il suo delta (capacità minima)
       b. Aumenta il flusso di delta lungo il cammino
       c. Aggiorna il grafo residuo
    3. Quando non esistono più cammini aumentanti, il flusso è massimo

    Parametri:
    - G: oggetto Graph con capacità e flussi
    - s: nodo sorgente (da cui parte il flusso)
    - t: nodo pozzo (dove arriva il flusso)

    Ritorna:
    - value: valore del flusso massimo (quanto flusso totale passa da s a t)
    - iterations: lista di dizionari, uno per ogni iterazione, contenente:
        * path: cammino aumentante trovato
        * delta: quanto flusso è stato aggiunto in questa iterazione
        * flow: stato del flusso dopo questa iterazione
    - S: insieme di nodi nel taglio minimo (lato sorgente)
    - T: insieme di nodi nel taglio minimo (lato pozzo)
    """
    value = 0
    iterations = []
    S = None
    T = None

    while True:
        R = build_residual_graph(G)
        path, delta = find_augmenting_path(R, s, t)

        if path is None:
            break

        # aggiorna flusso
        for i, j in zip(path[:-1], path[1:]):
            if j in G.cap[i]:
                G.flow[i][j] += delta
            else:
                G.flow[j][i] -= delta

        value += delta


        iterations.append({
            "path": path,
            "delta": delta,
            "flow": {i: dict(G.flow[i]) for i in G.flow}
        })

    # calcola taglio minimo residuo
    R_after = build_residual_graph(G)
    S, T = min_cut_from_residual(R_after, s)

    return value, iterations, S, T
