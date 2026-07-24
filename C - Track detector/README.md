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
- **Obstacle detection** — recognizes post-lane patterns that indicate obstacles

---

## Project Structure

```
Code/
├── Makefile                # Compilation and test execution
├── detectarPista.c         # Main program
└── test-cases/
    ├── test-case_1.txt     # Straight lane
    ├── test-case_2.txt     # Straight lane
    ├── test-case_3.txt     # Left curve
    ├── test-case_4.txt     # Straight lane
    ├── test-case_5.txt     # Right curve
    └── test-case_6.txt     # Straight lane
```

| Constant | Value | Meaning |
|---|---|---|
| `LANE_PATTERN` | `(1, 3, 2, 3, 1)` | Type sequence that identifies the lane |
| `VALIDITY_THRESHOLD` | `70%` | Minimum % of rows with valid midpoint |
| `STRAIGHT_TOLERANCE` | `±14` | Maximum variation from the mean for straight |
| `CURVE_TOLERANCE` | `±15` | Variation threshold for classifying curve |

---

## Modules

### Classification Module (`CreateNode` / `InsertKey`)

Receives raw sensor keys and organizes them into a linked list by grouping consecutive equal values. On each new value, it checks whether it has appeared before in the same row: if so, it reuses the previous type; if not, it creates a new node with type 1 and reclassifies the types of existing nodes to maintain ordering (1, 2, 3) by ascending key order.

The insertion logic is split into three internal helpers:
- `FindKeyType` — traverses the list searching for the key and returns the last node
- `AppendNode` — creates a new node and appends it to the end of the list
- `ReclassifyByKey` — adjusts the types of all nodes when a new distinct key is inserted

### Lane Detection Module (`FindLane`)

Traverses the classified list searching for the pattern (1, 3, 2, 3, 1). When found, it calculates the midpoint by accumulating partial `element_count` values:

1. Accumulates type 1 elements (left edge)
2. Adds type 3 elements (left shoulder)
3. Adds half of type 2 elements (lane center)
4. Ignores type 3 (right shoulder) and type 1 (right edge)

**Returns:** lane midpoint, or `-1` if the pattern is not found.

The pattern matching uses two shared helpers:
- `MatchPattern5` — matches 5 consecutive types and computes midpoint contribution
- `FindSubPattern` — matches a subsequence of any length

### Obstacle Detection Module (`CheckObstacle`)

Detects pattern variations that indicate obstacles on the lane:

1. Searches for the base pattern (1, 3, 2, 3, 1) — if found, returns 0 (clean lane)
2. Otherwise, searches for prefix (1, 3, 2) followed by a (3, 1) closing later — if found, returns 1 (obstacle)
3. Returns `-1` if no lane pattern is detected

### Utilities

- **`CountObstacles(array, size)`** — counts how many rows have an obstacle (values `== 1` in the vector)
- **`FreeList(list)`** — traverses the list freeing each node from memory

### Main Function (`main`)

1. Reads the number `L` of sensor rows
2. Dynamically allocates arrays for midpoints and obstacles (with null-check on allocation)
3. For each row, reads `quantity` values, classifies into a linked list, calculates the midpoint and obstacle status, and frees the list
4. If ≥70% of rows have a valid midpoint, calculates the average and decides:
   - **Straight line** — last midpoint within ±14 of the mean
   - **Right curve** — last midpoint less than the first
   - **Left curve** — last midpoint greater than the first
5. Reports whether there are obstacles on the lane

---

## Design Decisions

This project was developed under specific academic guidelines. Some design choices reflect the professor's pedagogical constraints rather than optimal engineering:

- **Classification by order of appearance**: types 1, 2, 3 depend on the sequence sensor values are processed — a deliberate simplification to teach list traversal and reclassification. An alternative based on absolute ordering by key value was designed but not applied per project requirements.
- **Curve decided by only 2 points** (first and last valid row) — professor's requirement to keep the decision logic simple. A more robust solution using linear regression on all valid midpoints was considered.
- **Linked list data structure** — maintained over a plain array despite the fixed key space (3 values), keeping the door open for variable-length sensor data in future expansions.
- **Minimum of 70% valid rows**: below this threshold, the program returns "Formato da pista nao estimado." without additional details.

---

## Tests

Six test cases located in `Code/casos-teste/`. Each contains 15 sensor rows with 950 values per row (values 0, 128, 255).

1. **test-case_1** — Symmetric straight lane, no obstacle
2. **test-case_2** — Straight lane with slight lateral shift, no obstacle
3. **test-case_3** — Left curve (pattern shifts progressively to the left between rows), no obstacle
4. **test-case_4** — Straight lane, no obstacle
5. **test-case_5** — Right curve with obstacle
6. **test-case_6** — Straight lane with obstacle

---

## Usage / Setup

Compile and run with `make`:

```bash
cd Code
make                # compiles and runs all test cases
make test-case_1    # runs only case 1
make test-case_3    # runs only case 3
```

Manual execution with a specific test case:

```bash
gcc -o detectarPista detectarPista.c
./detectarPista < casos-teste/test-case_3.txt
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
