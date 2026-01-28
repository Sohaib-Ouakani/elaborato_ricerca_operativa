from collections import defaultdict

def build_residual_graph(G):
    """
    Costruisce il grafo residuo G(x)
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
    Trova un cammino aumentante nel grafo residuo (DFS)
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
    Restituisce i nodi nel taglio minimo secondo il grafo residuo R
    S = nodi raggiungibili da s
    T = nodi non raggiungibili da s
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
    Algoritmo di Ford–Fulkerson (versione con grafo residuo)
    """
    value = 0
    iterations = []

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

        # calcola taglio minimo residuo
        R_after = build_residual_graph(G)
        S, T = min_cut_from_residual(R_after, s)

        iterations.append({
            "path": path,
            "delta": delta,
            "flow": {i: dict(G.flow[i]) for i in G.flow}
        })

    return value, iterations, S, T
