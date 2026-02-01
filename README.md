# ELABORATO RICERCA OPERATIVA

## PANORAMICA GENERALE

Questo progetto implementa in Python l'algoritmo di Ford-Fulkerson per risolvere il problema
del FLUSSO MASSIMO su grafi orientati con capacità.

### PROBLEMA DEL FLUSSO MASSIMO

Dato:
- Un grafo orientato G = (V, A)
- Capacità u_ij su ogni arco (i,j)
- Un nodo sorgente s
- Un nodo pozzo t

Trovare:
- Il massimo flusso che può essere inviato da s a t

Rispettando:
1. **Vincolo di capacità**: 0 ≤ x_ij ≤ u_ij per ogni arco (i,j)
2. **Conservazione del flusso**: per ogni nodo v ≠ s,t:
   Σ x_iv = Σ x_vj (flusso entrante = flusso uscente)

---

## STRUTTURA DEL PROGETTO

```
.
├── graph.py           - Struttura dati del grafo
├── residual.py        - Ford-Fulkerson con grafo residuo esplicito
├── labeling.py        - Ford-Fulkerson con metodo etichettamento
├── latex.py           - Funzioni per visualizzazione in LateX
└── main.py            - Programma principale
```

---

## 1. GRAPH.PY - Struttura Dati del Grafo

### Classe Graph

Rappresenta un grafo diretto con capacità e flussi.

**Attributi:**
- `cap[i][j]`: capacità dell'arco da i a j
- `flow[i][j]`: flusso corrente sull'arco da i a j
- `nodes`: set di tutti i nodi del grafo

**Invariante importante:**
Se esiste l'arco (i,j), deve esistere anche l'arco (j,i) (eventualmente con capacità 0).
Questo è necessario per l'algoritmo di Ford-Fulkerson.

**Metodo principale:**
```python
add_edge(i, j, capacity)
```
- Aggiunge l'arco i→j con la capacità specificata
- Inizializza il flusso a 0
- Crea automaticamente l'arco inverso j→i con capacità 0 (se non esiste)

---

## 2. RESIDUAL.PY - Versione con Grafo Residuo

### Concetto di Grafo Residuo

Il **grafo residuo** G(x) rappresenta la capacità disponibile considerando
il flusso corrente x:

Per ogni arco (i,j) del grafo originale:
1. **Arco diretto** i→j con capacità residua = u_ij - x_ij
   - Indica quanto flusso aggiuntivo possiamo inviare
   - Esiste solo se u_ij - x_ij > 0

2. **Arco inverso** j→i con capacità residua = x_ij
   - Indica quanto flusso possiamo "annullare"
   - Esiste solo se x_ij > 0

### Funzioni Principali

#### `build_residual_graph(G)`
Costruisce il grafo residuo a partire da G e dal suo flusso corrente.

**Ritorna:** Dizionario R dove R[i][j] = capacità residua dell'arco i→j

#### `find_augmenting_path(R, s, t)`
Trova un cammino aumentante nel grafo residuo usando DFS.

**Un cammino aumentante** è un cammino da s a t nel grafo residuo lungo
il quale possiamo inviare flusso aggiuntivo.

**Ritorna:**
- `path`: lista di nodi che formano il cammino (o None)
- `delta`: capacità residua minima lungo il cammino (il "collo di bottiglia")

#### `ford_fulkerson_residual(G, s, t)`
Algoritmo principale di Ford-Fulkerson.

**Pseudocodice:**
```
1. Inizializza flusso x = 0
2. WHILE esiste un cammino aumentante P da s a t in G(x):
   a. Trova P e calcola delta = min{capacità residua su P}
   b. Aumenta il flusso di delta lungo P
   c. Aggiorna il grafo residuo
3. RETURN flusso massimo
```

---

## 3. LABELING.PY - Versione con Etichettamento

### Metodo dell'Etichettamento

Invece di costruire esplicitamente il grafo residuo ad ogni iterazione,
questo metodo **etichetta** i nodi durante la ricerca del cammino.

### Etichette dei Nodi

Ogni nodo j raggiunto viene etichettato con:

1. **pred[j]** (predecessore):
   - `pred[j] = i` (positivo): j raggiunto tramite arco diretto i→j
   - `pred[j] = -i` (negativo): j raggiunto tramite arco inverso j→i nel residuo
   
2. **delta[j]** (capacità residua):
   - Capacità residua minima dal sorgente s al nodo j
   - Quanto flusso può attraversare il cammino da s a j

### Vantaggi del Metodo

- Non serve costruire esplicitamente il grafo residuo
- Le etichette permettono di ricostruire il cammino
- Il delta al pozzo t indica direttamente quanto flusso inviare

### Funzione Principale

#### `ford_fulkerson_labeling(G, s, t)`

**Fase di etichettamento (BFS):**
```
1. Inizializza: pred = {}, delta[s] = ∞
2. Coda = [s]
3. WHILE coda non vuota AND t non etichettato:
   a. Estrai nodo i dalla coda
   
   b. Per ogni arco diretto i→j con capacità residua:
      - pred[j] = i
      - delta[j] = min(delta[i], capacità residua i→j)
      - Aggiungi j alla coda
   
   c. Per ogni arco inverso j→i con flusso > 0:
      - pred[j] = -i
      - delta[j] = min(delta[i], flusso j→i)
      - Aggiungi j alla coda

4. Se t non etichettato → STOP (flusso massimo raggiunto)
5. Altrimenti → ricostruisci cammino e aggiorna flusso
```

---

## 4. LATEX.PY - Visualizzazione dei Grafi

### `tikz_graph(G, highlight_path, flows)`

Genera codice LaTeX/TikZ per disegnare il grafo.

**Caratteristiche:**
- Nodi posizionati secondo coordinate predefinite
- Archi etichettati con "flusso/capacità" (es: "3/5")
- Cammino aumentante evidenziato in rosso e spesso
- Solo archi con capacità > 0 vengono disegnati

**Parametri:**
- `highlight_path`: cammino da evidenziare (opzionale)
- `flows`: flussi alternativi da mostrare (opzionale)

### `tikz_graph_labels(G, labels, flows)`

Come `tikz_graph`, ma può mostrare etichette sui nodi.

**Con labels:**
Ogni nodo mostra:
```
    j
  (i,δ)
```
dove i = predecessore, δ = delta

**Senza labels:**
Comportamento identico a `tikz_graph` (senza evidenziazione)

---

## 5. MAIN.PY - Programma Principale

### Funzioni

#### `build_example_graph()`
Costruisce un grafo di esempio.

#### `latex_boilerplate()`
Genera il preambolo del documento LaTeX con tutti i pacchetti necessari.

### Esecuzione del Programma

Il programma esegue **due versioni** dell'algoritmo:

1. **Ford-Fulkerson con grafo residuo:**
   - Usa `ford_fulkerson_residual`
   - Visualizza con `tikz_graph` (cammino evidenziato in rosso)

2. **Ford-Fulkerson con etichettamento:**
   - Usa `ford_fulkerson_labeling`
   - Visualizza con `tikz_graph_labels` (etichette sui nodi)

### Output

Per ogni versione, il programma stampa:
```
=== FORD–FULKERSON (METODO) ===
Flusso massimo: 14
S: {1, 2, 3, 4, 5}
T: {6, 7, 8, 9, 10}

\documentclass{article}
...
\begin{document}

Iterazione 1
Cammino: [1, 2, 5, 8, 10]
Delta: 5
\\
\begin{tikzpicture}
...
\end{tikzpicture}

Iterazione 2
...

\end{document}
```

### Utilizzo dell'Output

```bash
# Esegui il programma e salva l'output
python main.py > output.tex

# Compila con LaTeX
pdflatex output.tex

# Visualizza il PDF
open output.pdf  # macOS
xdg-open output.pdf  # Linux
```

---

## TEOREMI FONDAMENTALI

### Teorema del Taglio Minimo - Flusso Massimo

**Enunciato:**
Il valore del flusso massimo da s a t è uguale alla capacità del taglio minimo.

**Taglio (S,T):**
- Partizione dei nodi: S ∪ T = V, S ∩ T = ∅
- s ∈ S, t ∈ T
- Capacità del taglio = Σ u_ij per tutti gli archi da S a T

**Alla fine dell'algoritmo:**
- S = nodi raggiungibili da s nel grafo residuo
- T = nodi non raggiungibili da s
- (S,T) è il taglio minimo
- Tutti gli archi da S a T sono saturi (x_ij = u_ij)
- Tutti gli archi da T a S hanno flusso 0

### Correttezza dell'Algoritmo

**L'algoritmo termina quando:**
Non esiste più un cammino aumentante da s a t nel grafo residuo.

**Questo implica:**
1. Il flusso corrente è il flusso massimo
2. Il taglio (S,T) è il taglio di capacità minima
3. Capacità(S,T) = Flusso(s,t)

---

## APPLICAZIONI PRATICHE

1. **Reti di trasporto:** massimizzare il flusso di merci/veicoli
2. **Reti di comunicazione:** massimizzare la banda disponibile
3. **Network reliability:** trovare i collegamenti critici

---

## CONCLUSIONI

Questo progetto fornisce un'implementazione completa e commentata dell'algoritmo
di Ford-Fulkerson in due varianti, con visualizzazione LaTeX/TikZ integrata.
