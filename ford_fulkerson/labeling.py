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

        iterations.append({
            "path": path,
            "delta": d,
            "flow": {i: dict(G.flow[i]) for i in G.flow}
        })

    return value, iterations
