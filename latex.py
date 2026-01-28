def tikz_graph(G, highlight_path=None, flows=None):
    """
    Disegna il grafo con TikZ.
    - flows: opzionale, dizionario dei flussi da usare al posto di G.flow
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
    Disegna il grafo con TikZ mostrando:
    - se labels è None: f/c sugli archi (versione classica)
    - se labels è fornito: etichettamento dei nodi (pred, delta)
    - flows: opzionale, dizionario dei flussi da usare al posto di G.flow
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
