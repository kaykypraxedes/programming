# B-Tree.py
# Desenvolvedor:
#     Kayky Moreira Praxedes

IRMAO_ESQUERDO = -1
IRMAO_DIREITO = 0
MAX_DEPTH = 100


class bNode:
    def __init__(self, leaf):
        self.leaf = leaf
        self.keys = []
        self.children = []


class bTree:
    def __init__(self, t):
        self.root = None
        self.t = t

    def goLeaf(self, node, k, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em goLeaf")
        if node.leaf is True:
            return node
        else:
            i = 0
            for i in range(len(node.keys)):
                if k < node.keys[i]:
                    return self.goLeaf(node.children[i], k, _call_depth + 1)
            return self.goLeaf(node.children[i + 1], k, _call_depth + 1)

    def findParent(self, current, child, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em findParent")
        if current.leaf is True:
            return None
        for i in range(len(current.keys) + 1):
            if current.children[i] == child:
                return current
            else:
                parent = self.findParent(current.children[i], child, _call_depth + 1)
                if parent is not None:
                    return parent
        return None

    def split(self, node, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em split")
        parent = self.findParent(self.root, node)
        if parent is None:
            newRoot = bNode(False)
            newRoot.children.append(node)
            self.root = newRoot
            parent = newRoot
        newNode = bNode(node.leaf)
        if len(parent.keys) == 2 * self.t - 1:
            self.split(parent, _call_depth + 1)
            parent = self.findParent(self.root, node)
        i = 0
        while i < len(parent.keys) and parent.children[i] != node:
            i += 1
        mediana_index = self.t - 1
        mediana = node.keys[mediana_index]
        newNode.keys = node.keys[mediana_index + 1 :]
        if not node.leaf:
            newNode.children = node.children[mediana_index + 1 :]
        node.keys = node.keys[:mediana_index]
        if not node.leaf:
            node.children = node.children[: mediana_index + 1]
        parent.keys.insert(i, mediana)
        parent.children.insert(i + 1, newNode)

    def insert(self, k, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em insert")
        if self.root is None:
            self.root = bNode(True)
            self.root.keys.append(k)
        else:
            leaf = self.goLeaf(self.root, k)
            if len(leaf.keys) < 2 * self.t - 1:
                i = 0
                while i < len(leaf.keys) and k > leaf.keys[i]:
                    i += 1
                leaf.keys.insert(i, k)
            else:
                self.split(leaf)
                self.insert(k, _call_depth + 1)

    def search(self, k, node, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em search")
        if node is None:
            return None
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys):
            if k == node.keys[i]:
                return node
            elif node.leaf:
                return None
            else:
                return self.search(k, node.children[i], _call_depth + 1)
        else:
            if node.leaf:
                return None
            else:
                return self.search(k, node.children[i], _call_depth + 1)

    def passKey(self, node, sibling, parent, index, pm):
        if pm == IRMAO_ESQUERDO:
            node.keys.insert(0, parent.keys[index])
        else:
            node.keys.append(parent.keys[index])
        parent.keys[index] = sibling.keys.pop(
            -1 if pm == IRMAO_ESQUERDO else IRMAO_DIREITO
        )
        if not sibling.leaf:
            if pm == IRMAO_ESQUERDO:
                node.children.insert(0, sibling.children.pop(-1))
            else:
                node.children.append(sibling.children.pop(IRMAO_DIREITO))

    def merge(self, node, sibling, parent, index, pm, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em merge")
        grandParent = self.findParent(self.root, parent)
        if len(parent.keys) > self.t - 1 or grandParent is None:
            if pm == IRMAO_ESQUERDO:
                sibling.keys.append(parent.keys[index])
                parent.keys.pop(index)
                parent.children.pop(index)
                sibling.keys.extend(node.keys)
                if not node.leaf:
                    sibling.children.extend(node.children)
            else:
                node.keys.append(parent.keys[index])
                parent.keys.pop(index)
                parent.children.pop(index + 1)
                node.keys.extend(sibling.keys)
                if not sibling.leaf:
                    node.children.extend(sibling.children)
                if parent == self.root and len(parent.keys) == 0:
                    if pm == IRMAO_ESQUERDO:
                        self.root = sibling
                    else:
                        self.root = node
        else:
            indexParent = grandParent.children.index(parent)
            if (
                indexParent > 0
                and len(grandParent.children[indexParent - 1].keys) > self.t - 1
            ):
                self.passKey(
                    parent,
                    grandParent.children[indexParent - 1],
                    grandParent,
                    indexParent - 1,
                    IRMAO_ESQUERDO,
                )
                self.merge(node, sibling, parent, index, pm, _call_depth + 1)
            elif (
                indexParent < len(grandParent.keys)
                and len(grandParent.children[indexParent + 1].keys) > self.t - 1
            ):
                self.passKey(
                    parent,
                    grandParent.children[indexParent + 1],
                    grandParent,
                    indexParent,
                    IRMAO_DIREITO,
                )
                self.merge(node, sibling, parent, index, pm, _call_depth + 1)
            else:
                if indexParent > 0:
                    self.merge(
                        parent,
                        grandParent.children[indexParent - 1],
                        grandParent,
                        indexParent - 1,
                        IRMAO_ESQUERDO,
                        _call_depth + 1,
                    )
                else:
                    self.merge(
                        parent,
                        grandParent.children[indexParent + 1],
                        grandParent,
                        indexParent,
                        IRMAO_DIREITO,
                        _call_depth + 1,
                    )

    def remove(self, k, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em remove")
        node = self.search(k, self.root)
        if node is None:
            print("Chave não encontrada")
            return
        elif node == self.root and node.leaf is True:
            node.keys.remove(k)
        else:
            if node.leaf is True:
                if len(node.keys) > self.t - 1:
                    node.keys.remove(k)
                else:
                    parent = self.findParent(self.root, node)
                    index = parent.children.index(node)
                    if index > 0 and len(parent.children[index - 1].keys) > self.t - 1:
                        self.passKey(
                            node,
                            parent.children[index - 1],
                            parent,
                            index - 1,
                            IRMAO_ESQUERDO,
                        )
                        node.keys.remove(k)
                        return
                    elif (
                        index < len(parent.keys)
                        and len(parent.children[index + 1].keys) > self.t - 1
                    ):
                        self.passKey(
                            node,
                            parent.children[index + 1],
                            parent,
                            index,
                            IRMAO_DIREITO,
                        )
                        node.keys.remove(k)
                        return
                    if index > 0:
                        self.merge(
                            node,
                            parent.children[index - 1],
                            parent,
                            index - 1,
                            IRMAO_ESQUERDO,
                        )
                        self.remove(k, _call_depth + 1)
                    else:
                        self.merge(
                            node,
                            parent.children[index + 1],
                            parent,
                            index,
                            IRMAO_DIREITO,
                        )
                        self.remove(k, _call_depth + 1)
            else:
                index = node.keys.index(k)
                if len(node.children[index].keys) > self.t - 1:
                    predessor = node.children[index].keys[
                        len(node.children[index].keys) - 1
                    ]
                    node.keys[index] = predessor
                    node.children[index].keys.pop(-1)
                    return
                elif len(node.children[index + 1].keys) > self.t - 1:
                    sucessor = node.children[index + 1].keys[0]
                    node.keys[index] = sucessor
                    node.children[index + 1].keys.pop(0)
                    return
                self.merge(
                    node.children[index],
                    node.children[index + 1],
                    node,
                    index,
                    IRMAO_DIREITO,
                )
                self.remove(k, _call_depth + 1)

    def printTree(self, node=None, level=0):
        if node is None:
            node = self.root
        print(
            "  " * level
            + f"Level {level}: {node.keys} {'(raiz)' if level == 0 else ''} {'(folha)' if node.leaf else ''}"
        )
        if not node.leaf:
            for child in node.children:
                self.printTree(child, level + 1)


def main():
    btree = bTree(2)
    print("======================")
    print("        B-TREE:       ")
    print("======================\n")
    print("t = 2\n")
    print("======================")
    print("       INSERÇÃO       ")
    print("======================\n")
    print("10, 20 e 5 (caso 1):")
    btree.insert(10)
    btree.insert(20)
    btree.insert(5)
    btree.printTree()
    print("\n15 (caso 2):")
    btree.insert(15)
    btree.printTree()
    print("\n25, 3 e 7 (caso 1):")
    btree.insert(25)
    btree.insert(3)
    btree.insert(7)
    btree.printTree()
    print("\n12 (caso 2):")
    btree.insert(12)
    btree.printTree()
    print("\n17, 22 e 27 (caso 1):")
    btree.insert(17)
    btree.insert(22)
    btree.insert(27)
    btree.printTree()
    print("\n2 (caso 2):")
    btree.insert(2)
    btree.printTree()
    print("\n4, 6 e 8 (caso 1):")
    btree.insert(4)
    btree.insert(6)
    btree.insert(8)
    btree.printTree()
    print("\n11 (caso recursivo):")
    btree.insert(11)
    btree.printTree()
    print("\n13, 16, 18 e 21 (caso 1):")
    btree.insert(13)
    btree.insert(16)
    btree.insert(18)
    btree.insert(21)
    btree.printTree()
    print("\n23 (caso 2):")
    btree.insert(23)
    btree.printTree()
    print("\n26 e 28 (caso 1):")
    btree.insert(26)
    btree.insert(28)
    btree.printTree()
    print("\n======================")
    print("       REMOÇÃO       ")
    print("======================\n")
    print("2 e 4 (casos 1a):")
    btree.remove(2)
    btree.remove(4)
    btree.printTree()
    print("\n3 (caso 1b):")
    btree.remove(3)
    btree.printTree()
    print("\n8, 11, 12, 16 e 17 (casos 1a):")
    btree.remove(8)
    btree.remove(11)
    btree.remove(12)
    btree.remove(16)
    btree.remove(17)
    btree.printTree()
    print("\n13 (caso 1c):")
    btree.remove(13)
    btree.printTree()
    print("\n20 (caso 2a):")
    btree.remove(20)
    btree.printTree()
    print("\n22 e 23(casos 1a):")
    btree.remove(22)
    btree.remove(23)
    btree.printTree()
    print("\n18 (caso 2b):")
    btree.remove(18)
    btree.printTree()
    print("\n6 (Caso recursivo):")
    btree.remove(6)
    btree.printTree()

    print("\n======================")
    print("       PESQUISA      ")
    print("======================\n")
    if btree.search(28, btree.root) is not None:
        print("Número 28 encontrado!")
    else:
        print("Número 28 não foi encontrado!")
    if btree.search(51, btree.root) is not None:
        print("Número 51 encontrado!")
    else:
        print("Número 51 não foi encontrado!")


if __name__ == "__main__":
    main()
