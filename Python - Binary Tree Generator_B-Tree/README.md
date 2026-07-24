# B-Tree — Binary Tree Generator

Implementation of a **B-Tree** of degree `t` in Python, with complete insertion, deletion, and search operations. Despite the directory name, the structure is a **B-Tree**, not a simple binary tree.

**Developer:** Kayky Moreira Praxedes

---

## What is a B-Tree?

A B-Tree is a balanced data structure where each node can store **multiple keys** and have **multiple children**. Unlike a binary tree (which has at most 2 children per node), the B-Tree is optimized for systems that work with large volumes of data, such as databases and file systems.

**Fundamental properties:**
- Each node contains between `t - 1` and `2t - 1` keys (except the root, which can have 1 to `2t - 1` keys)
- Each non-leaf node with `n` keys has exactly `n + 1` children
- All leaves are at the **same depth**
- Keys within each node are kept **sorted**

---

## Features

- **Insertion** — Inserts keys while maintaining tree balance, splitting full nodes when necessary.
- **Deletion** — Removes keys covering all literature cases (leaf, internal node, borrowing between siblings, node merging).
- **Search** — Locates a key by traversing the tree from the root.
- **Visualization** — Displays the tree formatted by levels, indicating root and leaves.

---

## Code Structure

| Constant | Value | Meaning |
|---|---|---|
| `LEFT_SIBLING` | `-1` | Indicates operation with the left sibling |
| `RIGHT_SIBLING` | `0` | Indicates operation with the right sibling |
| `MAX_DEPTH` | `100` | Safety limit against infinite recursion |

**Class `bNode`:** `leaf` (bool, whether it is a leaf), `keys` (stored keys), `children` (references to children).

**Class `bTree`:** `root` (root node), `t` (minimum degree).

---

## Modules

### Insertion

Insertion (`insert(k)`) navigates to the appropriate leaf via `goLeaf`. If the leaf has space (`len(keys) < 2t - 1`), it inserts `k` while maintaining order. If it is full, it splits the node and retries.

`split(node)` divides a full node into two siblings, promoting the median key to the parent — creating a new root if necessary, and cascading recursively if the parent is also full.

### Deletion

Deletion (`remove(k)`) covers all classic cases:

**Leaf deletion:**
1. **1a** — leaf above minimum: remove directly
2. **1b** — leaf at minimum, but a sibling has extra keys: borrow via `passKey`
3. **1c** — leaf and siblings at minimum: merge via `merge`, then try to remove again

**Internal node deletion:**
1. **2a** — some child has more than minimum: replace with predecessor/successor key
2. **2b** — both children at minimum: merge the two children via `merge`

`merge(node, sibling, parent, index, pm)` merges two sibling nodes when both are at minimum keys; if the parent also runs out of extra keys, the merge may cascade up to the grandparent. `passKey` does the reverse: transfers a key from parent to the node, compensating with a key from the sibling. `findParent` locates the parent of a node recursively.

### Search

`search(k, node)` recursively descends through the tree: returns the node if `k` is found in it, `None` if it reaches a leaf without finding it, or descends to the appropriate child.

---

## Safety Against Infinite Loops

All recursive functions (`goLeaf`, `findParent`, `split`, `insert`, `search`, `merge`, `remove`) have the `_call_depth` parameter, incremented on each call. If `MAX_DEPTH` (100) is exceeded, a `RecursionError` is raised, preventing infinite loops caused by bugs in the reorganization logic.

---

## Tests

The `main()` function runs a battery of manual tests:

1. **Insertions** — 20 keys, alternating between nodes with space and full nodes (triggering splits)
2. **Deletions** — 13 keys, covering cases 1a, 1b, 1c, 2a, 2b, and recursive deletion
3. **Searches** — existing key (28) and non-existing key (51)

---

## Usage

```python
btree = bTree(2)  # minimum degree = 2
```

With `t = 2`, each node can have between 1 and 3 keys, and each non-leaf node has between 2 and 4 children.
