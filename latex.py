def tikz_graph(G, highlight_path=None):
    """
    Restituisce una stringa LaTeX/TikZ del grafo
    """
    highlight = set()
    if highlight_path:
        highlight = set(zip(highlight_path[:-1], highlight_path[1:]))

    s = "\\begin{tikzpicture}[>=stealth, node distance=2cm]\n"

    for i, node in enumerate(sorted(G.nodes)):
        s += f"\\node ({node}) at ({i*2},0) {{{node}}};\n"

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
