# Lane Detector

C implementation that processes optical sensor readings (values 0, 128, 255) to detect lane markings, classify curves (left/right), and identify obstacles — using linked lists with grouping of consecutive equal values and classification by order of appearance.

**Developers:** Kayky Moreira Praxedes, Carlos Ernesto Cardoso dos Reis

---

## What is Lane Detection?

Line follower systems use optical sensors that return reflectance values: **0** (black/shadow), **128** (gray/edge), and **255** (white/lane). Each sensor row scans a cross-section of the lane. The program groups consecutive equal values, classifies each group into one of 3 types (1/2/3) by order of first appearance, and searches for the pattern **(1, 3, 2, 3, 1)** — which respectively represents left edge, left shoulder, lane center, right shoulder, right edge.

### Fundamental properties

- The pattern (1, 3, 2, 3, 1) is the signature of a valid lane marking
- The position of type 2 group (center) defines the lane midpoint
- Curves are detected by the variation of the midpoint between rows
- Obstacles are anomalous patterns that interrupt the expected sequence

---

## Features

- **Sensor data classification** — groups consecutive equal values into linked list nodes and assigns types (1, 2, 3) by order of appearance
- **Lane detection** — locates the pattern (1, 3, 2, 3, 1) in the classified list and calculates the lane midpoint
- **Curve classification** — compares the first with the last valid midpoint to decide between straight, left curve, or right curve
- **Obstacle detection** — recognizes post-lane patterns that indicate obstacles (currently inoperative — see Issues #14)

---

## Project Structure

```
Code/
├── Makefile                 # Compilation and test execution
├── detectarPista.c          # Main program
└── casos-teste/
    ├── detectarPista-casoTeste-1.txt  # Straight lane
    ├── detectarPista-casoTeste-2.txt  # Straight lane
    ├── detectarPista-casoTeste-3.txt  # Left curve
    └── detectarPista-casoTeste-4.txt  # Straight lane
```

| Constant | Value | Meaning |
|---|---|---|
| `LANE_PATTERN` | `(1, 3, 2, 3, 1)` | Type sequence that identifies the lane |
| `VALIDITY_THRESHOLD` | `70%` | Minimum % of rows with valid midpoint |
| `STRAIGHT_TOLERANCE_UP` | `+14` | Maximum variation above average for straight |
| `STRAIGHT_TOLERANCE_LOW` | `-30` | Maximum variation below average for straight |
| `CURVE_TOLERANCE` | `±15` | Variation for classifying curve |

---

## Modules

### Classification Module (`novo` / `inserir`)

Receives raw sensor keys and organizes them into a linked list by grouping consecutive equal values. On each new value, it checks whether it has appeared before in the same row: if so, it reuses the previous type; if not, it creates a new node with type 1 and reclassifies the types of existing nodes to maintain ordering (1, 2, 3) by ascending key order.

### Lane Detection Module (`testa`)

Traverses the classified list searching for the pattern (1, 3, 2, 3, 1). When found, it calculates the midpoint by accumulating partial `NumElementos` values:

1. Accumulates type 1 elements (left edge)
2. Adds type 3 elements (left shoulder)
3. Adds half of type 2 elements (lane center)
4. Ignores type 3 (right shoulder) and type 1 (right edge)

**Returns:** lane midpoint, or `-1` if the pattern is not found.

### Obstacle Detection Module (`TestaObstaculo`)

Detects pattern variations that indicate obstacles on the lane:

1. Searches for the base pattern (1, 3, 2, 3, 1)
2. If there is a direct closing (3, 1), returns 10
3. If there is a second pattern (3, 1) after the closing, returns 1
4. Returns `-1` if there is no obstacle

**Note:** This function is **never called** in the current `main()` (see Issue #14).

### Utilities

- **`contaObs(vector, size)`** — counts how many rows have an obstacle (values `== 1` in the vector)
- **`freePtr(list)`** — traverses the list freeing each node from memory

### Main Function (`main`)

1. Reads the number `L` of sensor rows
2. For each row, reads `quantity` values, classifies into a linked list, calculates the midpoint, and frees the list
3. If ≥70% of rows have a valid midpoint, calculates the average and decides:
   - **Straight line** — midpoints within tolerance
   - **Right curve** — last midpoint less than the first
   - **Left curve** — last midpoint greater than the first
4. Reports whether there are obstacles on the lane

---

## Safety / Limitations / Robustness

- **Classification by order of appearance**: types 1, 2, 3 depend on the sequence in which sensor values are processed — if the expected order (e.g., 0 → 255 → 128) is not respected, the classification may produce false positives or negatives.
- **Minimum of 70% valid rows**: below this threshold, the program returns "Lane shape not estimated." without additional details.
- **Inoperative obstacle detection**: the `TestaObstaculo()` function is not called anywhere in `main()` (see `PENDENCIAS.md #14`).
- **Curve decided by only 2 points** (first and last row) — insufficient for real curve patterns (see `PENDENCIAS.md #15`).
- **Dynamic allocation without failure handling**: `malloc` return value is never checked.
- **Educational project**: not recommended for production use without the fixes listed in `PENDENCIAS.md`.

---

## Tests

Four test cases located in `Codigo/casos-teste/`. Each contains 15 sensor rows with 950 values per row (values 0, 128, 255).

1. **casoTeste-1** — Symmetric straight lane, no obstacle
2. **casoTeste-2** — Straight lane with slight lateral shift, no obstacle
3. **casoTeste-3** — Left curve (pattern shifts progressively to the left between rows), no obstacle
4. **casoTeste-4** — Straight lane, no obstacle

---

## Usage / Setup

Compile and run with `make`:

```bash
cd Code
make             # compiles detectarPista
make run-all     # runs all 4 test cases
make run-teste1  # runs only case 1
```

Manual execution with a specific test case:

```bash
gcc -o detectarPista detectarPista.c
./detectarPista < casos-teste/detectarPista-casoTeste-3.txt
```

Input format:

```
L                       # number of sensor rows
Q1                      # number of values in row 1
v1 v2 ... vQ1           # sensor values (0, 128, 255)
Q2                      # number of values in row 2
v1 v2 ... vQ2
...
```

Expected output:

```
Pista em linha reta e sem impedimento.
Curva a esquerda e com impedimento.
Formato da pista nao estimado.
```
