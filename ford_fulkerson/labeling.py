def min_cut_from_residual(G, s):
    """
    Calcola il taglio minimo (S,T) a partire dal grafo residuo costruito da G
    S = nodi raggiungibili dalla sorgente
    T = nodi non raggiungibili
    """
    from collections import defaultdict

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
    Algoritmo di Ford–Fulkerson con etichettamento
    """
    value = 0
    iterations = []

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

        # calcolo taglio minimo residuo
        S, T = min_cut_from_residual(G, s)

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

    return value, iterations, S, T
