from collections import defaultdict

def min_cut_from_residual(G, s):
    """
    Calcola il taglio minimo (S, T) a partire dal grafo G e dal suo flusso corrente.

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

    # Costruisco il grafo residuo
    R = defaultdict(dict)

    # Itera su tutti gli archi del grafo
    for i in G.cap:
        for j in G.cap[i]:
            u = G.cap[i][j]     # Capacità dell'arco i→j
            x = G.flow[i][j]    # Flusso corrente sull'arco i→j

            # Arco diretto i→j nel grafo residuo
            # Esiste se c'è ancora capacità disponibile
            if u - x > 0:
                R[i][j] = u - x

            # Arco inverso j→i nel grafo residuo
            # Esiste se c'è flusso da poter ridurre
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
    il grafo residuo a ogni iterazione.

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
    # Inizializza il valore del flusso massimo a 0
    value = 0

    # Lista per memorizzare i dettagli di ogni iterazione
    iterations = []

    while True:
        # Dizionario dei predecessori: pred[nodo] = predecessore di 'nodo'
        # Se pred[j] > 0: arco diretto pred[j]→j
        # Se pred[j] < 0: arco inverso j→|pred[j]|
        pred = {}

        # delta[j] = indica il massimo aumento consentito nel cammino da s fino a j
        delta = {s: float("inf")}

        # fisso il predecessore della sorgente a se stesso
        pred[s] = s

        # Coda per la BFS (Breadth-First Search)
        # BFS invece di DFS per trovare cammini più "corti"
        # Questa coda rappresenta tutti i nodi etichettati non espansi
        queue = [s]

        # Fase di etichettamento
        while queue and t not in pred:
            i = queue.pop(0)

            # ESPLORAZIONE ARCHI DIRETTI i→j
            # Corrispondono ad archi nel grafo originale con capacità residua
            for j in G.cap[i]:
                # Considera l'arco i→j solo se:
                # 1. j non è stato ancora etichettato (j not in pred)
                # 2. C'è capacità residua disponibile (flow[i][j] < cap[i][j])
                if j not in pred and G.flow[i][j] < G.cap[i][j]:
                    pred[j] = i
                    delta[j] = min(delta[i], G.cap[i][j] - G.flow[i][j])
                    queue.append(j)

            # ESPLORAZIONE ARCHI INVERSI j→i
            # Corrispondono a flusso che può essere ridotto
            for j in G.cap:
                # Verifica se esiste l'arco j→i nel grafo originale
                # e se ha flusso positivo (che può essere ridotto)
                if i in G.cap[j] and j not in pred and G.flow[j][i] > 0:
                    pred[j] = -i
                    delta[j] = min(delta[i], G.flow[j][i])
                    queue.append(j)

        # CONDIZIONE DI TERMINAZIONE:
        # Se t non è stato etichettato, non esiste un cammino aumentante
        if t not in pred:
            # Per ottenere anche una rappresentazione del labeling che "fallisce"
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
                # Copia del flusso corrente (per visualizzazione)
                "flow": {i: dict(G.flow[i]) for i in G.flow}
            })
            break

        # CALCOLO DEL FLUSSO DA INVIARE:
        d = delta[t]

        # Aggiorna il valore totale del flusso
        value += d

        # RICOSTRUZIONE DEL CAMMINO AUMENTANTE:
        # Risale dal pozzo t alla sorgente s seguendo i predecessori
        path = [t]
        j = t
        while j != s:
            j = abs(pred[j])
            path.append(j)

        # Inverti il cammino per averlo da s a t
        path.reverse()

        # AGGIORNAMENTO DEI FLUSSI:
        # Risale di nuovo dal pozzo alla sorgente per aggiornare i fluss
        j = t
        while j != s:
            # Ottieni il predecessore (con il segno)
            p = pred[j]
            i = abs(p)
            if p > 0:
                # ARCO DIRETTO i→j: aumenta il flusso di d
                G.flow[i][j] += d
            else:
                # ARCO INVERSO j→i: riduci il flusso di d
                # (equivalente a "annullare" parte del flusso)
                G.flow[j][i] -= d
            j = i

        # Salva i dettagli di questa iterazione:
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
            # Copia del flusso corrente (per visualizzazione)
            "flow": {i: dict(G.flow[i]) for i in G.flow}
        })
    # CALCOLO DEL TAGLIO MINIMO
    S, T = min_cut_from_residual(G, s)

    return value, iterations, S, T
