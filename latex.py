def tikz_graph(G, highlight_path=None):
    highlight = set()
    if highlight_path:
        highlight = set(zip(highlight_path[:-1], highlight_path[1:]))

    # layout manuale (puoi adattarlo a ogni esempio)
    positions = {
        1: (0, 0),
        2: (2, -1),
        4: (2, 1),
        5: (3, 1),
        3: (3, -1),
        6: (4, 0),
        8: (4, -1),
        7: (4, 1),
        9: (5, 0),
    }

    s = "\\begin{tikzpicture}[>=Stealth]\n"

    for node, (x, y) in positions.items():
        s += f"\\node ({node}) at ({x},{y}) {{{node}}};\n"

    for i in G.cap:
        for j in G.cap[i]:
            if G.cap[i][j] > 0:
                style = "red, thick" if (i, j) in highlight else ""
                s += (
                    f"\\draw[->,{style}] ({i}) -- ({j}) "
                    f"node[midway, above] {{{G.flow[i][j]}/{G.cap[i][j]}}};\n"
                )

    s += "\\end{tikzpicture}\n"
    return s
