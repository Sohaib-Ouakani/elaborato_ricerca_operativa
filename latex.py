def tikz_graph(G, highlight_path=None, flows=None):
    """
    Genera codice LaTeX/TikZ per disegnare il grafo con flussi e capacità.

    Questa funzione crea una rappresentazione grafica del grafo usando TikZ,
    una libreria LaTeX per disegnare grafici. Il risultato può essere incluso
    in un documento LaTeX per visualizzare il grafo.

    CARATTERISTICHE DELLA VISUALIZZAZIONE:
    - Ogni nodo è disegnato con la sua etichetta (numero)
    - Ogni arco mostra "flusso/capacità" (es. "3/5" = 3 unità di flusso su 5 di capacità)
    - Gli archi del cammino aumentante corrente sono evidenziati in rosso
    - Solo gli archi con capacità > 0 sono disegnati

    Parametri:
    - G: oggetto Graph con capacità (cap) e flussi (flow)
    - highlight_path: lista di nodi che formano un cammino da evidenziare in rosso
                      (opzionale, usato per mostrare il cammino aumentante)
    - flows: dizionario alternativo di flussi da usare al posto di G.flow
             (opzionale, utile per mostrare flussi di iterazioni precedenti)

    Ritorna:
    - s: stringa contenente il codice LaTeX/TikZ completo per disegnare il grafo
    """
    highlight = set()
    if highlight_path:
        highlight = set(zip(highlight_path[:-1], highlight_path[1:]))

    # positions = {
    #     2: (2, 2),
    #     4: (2, -2),
    #     5: (4, -2),
    #     3: (4, 2),
    #     6: (6, 0),
    #     8: (6, 2),
    #     7: (6, -2),
    #     9: (8, 0),
    # }

    positions = {
        1: (0, 0),
        2: (1.5, 2),
        3: (1.5, -2),
        4: (3, 0),
        5: (4.5, 2),
        6: (4.5, -2),
        7: (6, 0),
        8: (7.5, 2),
        9: (7.5, -2),
        10: (9, 0),
    }

    # per esercizio esame 2
    # positions = {
    #     1: (0, 0),
    #     2: (1.5, 2),
    #     3: (1.5, -2),
    #     4: (3, 0),
    #     5: (4.5, 2),
    #     6: (4.5, -2),
    #     7: (6, 0),
    # }

    s = "\\begin{tikzpicture}[>=Stealth]\n"

    for node, (x, y) in positions.items():
        s += f"\\node ({node}) at ({x},{y}) {{{node}}};\n"

    # usa flows se fornito, altrimenti G.flow
    flow_dict = flows if flows else G.flow

    for i in G.cap:
        for j in G.cap[i]:
            if G.cap[i][j] > 0:
                style = "red, thick" if (i, j) in highlight else ""
                s += (
                    f"\\draw[->,{style}] ({i}) -- ({j}) "
                    f"node[midway, above] {{{flow_dict[i][j]}/{G.cap[i][j]}}};\n"
                )

    s += "\\end{tikzpicture}\n"
    return s


def tikz_graph_labels(G, labels=None, flows=None):
    """
    Genera codice LaTeX/TikZ per disegnare il grafo con etichettamento dei nodi.

    Questa funzione è simile a tikz_graph, ma può mostrare informazioni aggiuntive
    sui nodi quando viene usato il metodo dell'etichettamento.

    DUE MODALITÀ DI VISUALIZZAZIONE:

    1. Se labels è None (modalità classica):
       - Mostra solo i numeri dei nodi
       - Mostra "flusso/capacità" sugli archi
       - Usato per visualizzare il grafo senza informazioni di etichettamento

    2. Se labels è fornito (modalità etichettamento):
       - Mostra il numero del nodo
       - Sotto ogni nodo mostra (pred, delta) dove:
         * pred = predecessore del nodo nel cammino aumentante
         * delta = capacità residua dal sorgente a questo nodo
       - Usato per visualizzare lo stato dell'algoritmo di etichettamento

    Parametri:
    - G: oggetto Graph con capacità e flussi
    - labels: dizionario con informazioni di etichettamento per ogni nodo
              labels[nodo] = {"pred": predecessore, "delta": capacità_residua}
              None per visualizzazione classica
    - flows: dizionario alternativo di flussi (opzionale)

    Ritorna:
    - s: stringa contenente il codice LaTeX/TikZ
    """

    # positions = {
    #     2: (2, 2),
    #     4: (2, -2),
    #     5: (4, -2),
    #     3: (4, 2),
    #     6: (6, 0),
    #     8: (6, 2),
    #     7: (6, -2),
    #     9: (8, 0),
    # }

    positions = {
        1: (0, 0),
        2: (1.5, 2),
        3: (1.5, -2),
        4: (3, 0),
        5: (4.5, 2),
        6: (4.5, -2),
        7: (6, 0),
        8: (7.5, 2),
        9: (7.5, -2),
        10: (9, 0),
    }

    # per esercizio esame 2
    # positions = {
    #     1: (0, 0),
    #     2: (1.5, 2),
    #     3: (1.5, -2),
    #     4: (3, 0),
    #     5: (4.5, 2),
    #     6: (4.5, -2),
    #     7: (6, 0),
    # }

    s = "\\begin{tikzpicture}[>=Stealth]\n"

    # nodi
    for node, (x, y) in positions.items():
        if labels and node in labels:
            pred = labels[node]["pred"]
            delta = labels[node]["delta"]
            s += f"\\node ({node}) at ({x},{y}) {{{node}\\\\{{\\small ({pred},{delta})}}}};\n"
        else:
            s += f"\\node ({node}) at ({x},{y}) {{{node}}};\n"

    flow_dict = flows if flows else G.flow

    # archi con etichette f/c
    for i in G.cap:
        for j in G.cap[i]:
            if G.cap[i][j] > 0:
                s += (
                    f"\\draw[->] ({i}) -- ({j}) "
                    f"node[midway, above] {{{flow_dict[i][j]}/{G.cap[i][j]}}};\n"
                )

    s += "\\end{tikzpicture}\n"
    return s
