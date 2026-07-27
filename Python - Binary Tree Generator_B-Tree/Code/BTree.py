# B-Tree.py
# Desenvolvedor:
#     Kayky Moreira Praxedes

# Direção do irmão para operações de empréstimo/mesclagem
LEFT_SIBLING = -1
RIGHT_SIBLING = 0
# Limite de segurança contra recursão infinita
MAX_DEPTH = 100


class BNode:
    # Nó da B-Tree: folha, lista de chaves e lista de filhos
    def __init__(self, leaf):
        self.leaf = leaf
        self.keys = []
        self.children = []


class BTree:
    # Árvore B com grau mínimo t (cada nó tem entre t-1 e 2t-1 chaves)
    def __init__(self, t):
        self.root = None
        self.t = t

    # Percorre a árvore da raiz até a folha onde a chave k deve ser inserida
    # Input:  BNode, int, int
    # Output: BNode
    def GoLeaf(self, node, k, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em GoLeaf")
        if node.leaf is True:
            return node
        else:
            i = 0
            for i in range(len(node.keys)):
                if k < node.keys[i]:
                    return self.GoLeaf(node.children[i], k, _call_depth + 1)
            return self.GoLeaf(node.children[i + 1], k, _call_depth + 1)

    # Encontra recursivamente o nó pai de um nó filho na árvore
    # Input:  BNode, BNode, int
    # Output: BNode | None
    def FindParent(self, current, child, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em FindParent")
        if current.leaf is True:
            return None
        for i in range(len(current.keys) + 1):
            if current.children[i] == child:
                return current
            else:
                parent = self.FindParent(current.children[i], child, _call_depth + 1)
                if parent is not None:
                    return parent
        return None

    # Divide um nó cheio, promovendo a chave mediana ao pai.
    # Se o nó for raiz, cria uma nova raiz. Se o pai também estiver cheio, divide-o recursivamente antes de prosseguir.
    # Input:  BNode, int
    # Output: None
    def Split(self, node, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em Split")
        parent = self.FindParent(self.root, node)
        if parent is None:
            new_root = BNode(False)
            new_root.children.append(node)
            self.root = new_root
            parent = new_root
        new_node = BNode(node.leaf)
        if len(parent.keys) == 2 * self.t - 1:
            self.Split(parent, _call_depth + 1)
            parent = self.FindParent(self.root, node)
        i = 0
        while i < len(parent.keys) and parent.children[i] != node:
            i += 1
        mediana_index = self.t - 1
        mediana = node.keys[mediana_index]
        new_node.keys = node.keys[mediana_index + 1 :]
        if not node.leaf:
            new_node.children = node.children[mediana_index + 1 :]
        node.keys = node.keys[:mediana_index]
        if not node.leaf:
            node.children = node.children[: mediana_index + 1]
        parent.keys.insert(i, mediana)
        parent.children.insert(i + 1, new_node)

    # Insere uma chave k na B-Tree. Localiza a folha alvo via GoLeaf.
    # Se a folha tiver espaço, insere ordenadamente; senão, divide o nó (Split) e tenta novamente.
    # Input:  int, int
    # Output: None
    def Insert(self, k, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em Insert")
        if self.root is None:
            self.root = BNode(True)
            self.root.keys.append(k)
        else:
            leaf = self.GoLeaf(self.root, k)
            if len(leaf.keys) < 2 * self.t - 1:
                i = 0
                while i < len(leaf.keys) and k > leaf.keys[i]:
                    i += 1
                leaf.keys.insert(i, k)
            else:
                self.Split(leaf)
                self.Insert(k, _call_depth + 1)

    # Busca recursivamente uma chave k na subárvore enraizada em node.
    # Retorna o nó que contém a chave ou None se não encontrada.
    # Input:  int, BNode, int
    # Output: BNode | None
    def Search(self, k, node, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em Search")
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
                return self.Search(k, node.children[i], _call_depth + 1)
        else:
            if node.leaf:
                return None
            else:
                return self.Search(k, node.children[i], _call_depth + 1)

    # Transfere uma chave do nó pai para node, pegando uma chave do nó irmão (esquerdo ou direito) como reposição.
    # Usado no rebalanceamento durante remoção (caso 1b).
    # Input:  BNode, BNode, BNode, int, int
    # Output: None
    def PassKey(self, node, sibling, parent, index, pm):
        if pm == LEFT_SIBLING:
            node.keys.insert(0, parent.keys[index])
        else:
            node.keys.append(parent.keys[index])
        parent.keys[index] = sibling.keys.pop(
            -1 if pm == LEFT_SIBLING else RIGHT_SIBLING
        )
        if not sibling.leaf:
            if pm == LEFT_SIBLING:
                node.children.insert(0, sibling.children.pop(-1))
            else:
                node.children.append(sibling.children.pop(RIGHT_SIBLING))

    # Mescla dois nós irmãos quando ambos estão no mínimo de chaves.
    # Se o pai também ficar abaixo do mínimo, pode cascatear a mesclagem recursivamente para cima (com empréstimo do avô ou fusão de níveis).
    # Input:  BNode, BNode, BNode, int, int, int
    # Output: None
    def Merge(self, node, sibling, parent, index, pm, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em Merge")
        grand_parent = self.FindParent(self.root, parent)
        if len(parent.keys) > self.t - 1 or grand_parent is None:
            if pm == LEFT_SIBLING:
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
                    if pm == LEFT_SIBLING:
                        self.root = sibling
                    else:
                        self.root = node
        else:
            index_parent = grand_parent.children.index(parent)
            if (
                index_parent > 0
                and len(grand_parent.children[index_parent - 1].keys) > self.t - 1
            ):
                self.PassKey(
                    parent,
                    grand_parent.children[index_parent - 1],
                    grand_parent,
                    index_parent - 1,
                    LEFT_SIBLING,
                )
                self.Merge(node, sibling, parent, index, pm, _call_depth + 1)
            elif (
                index_parent < len(grand_parent.keys)
                and len(grand_parent.children[index_parent + 1].keys) > self.t - 1
            ):
                self.PassKey(
                    parent,
                    grand_parent.children[index_parent + 1],
                    grand_parent,
                    index_parent,
                    RIGHT_SIBLING,
                )
                self.Merge(node, sibling, parent, index, pm, _call_depth + 1)
            else:
                if index_parent > 0:
                    self.Merge(
                        parent,
                        grand_parent.children[index_parent - 1],
                        grand_parent,
                        index_parent - 1,
                        LEFT_SIBLING,
                        _call_depth + 1,
                    )
                else:
                    self.Merge(
                        parent,
                        grand_parent.children[index_parent + 1],
                        grand_parent,
                        index_parent,
                        RIGHT_SIBLING,
                        _call_depth + 1,
                    )

    # Remove uma chave k da B-Tree tratando todos os casos clássicos:
    # - Caso 1: remoção em folha (1a: chaves suficientes; 1b: empréstimo
    #   do irmão via PassKey; 1c: mesclagem com irmão via Merge)
    # - Caso 2: remoção em nó interno (2a: substituir por antecessor/sucessor;
    #   2b: mesclar filhos e tentar novamente)
    # Suporta cascateamento recursivo quando a mesclagem reduz o pai.
    # Input:  int, int
    # Output: None
    def Remove(self, k, _call_depth=0):
        if _call_depth > MAX_DEPTH:
            raise RecursionError("Máxima profundidade excedida em Remove")
        node = self.Search(k, self.root)
        if node is None:
            print("Chave não encontrada")
            return
        elif node == self.root and node.leaf is True:
            node.keys.remove(k)
        else:
            if node.leaf is True:
                # Caso 1: remoção em folha
                if len(node.keys) > self.t - 1:
                    # Caso 1a: folha tem chaves suficientes, remove diretamente
                    node.keys.remove(k)
                else:
                    parent = self.FindParent(self.root, node)
                    index = parent.children.index(node)
                    if index > 0 and len(parent.children[index - 1].keys) > self.t - 1:
                        # Caso 1b: empréstimo do irmão esquerdo
                        self.PassKey(
                            node,
                            parent.children[index - 1],
                            parent,
                            index - 1,
                            LEFT_SIBLING,
                        )
                        node.keys.remove(k)
                        return
                    elif (
                        index < len(parent.keys)
                        and len(parent.children[index + 1].keys) > self.t - 1
                    ):
                        # Caso 1b: empréstimo do irmão direito
                        self.PassKey(
                            node,
                            parent.children[index + 1],
                            parent,
                            index,
                            RIGHT_SIBLING,
                        )
                        node.keys.remove(k)
                        return
                    # Caso 1c: mesclar com irmão
                    if index > 0:
                        self.Merge(
                            node,
                            parent.children[index - 1],
                            parent,
                            index - 1,
                            LEFT_SIBLING,
                        )
                        self.Remove(k, _call_depth + 1)
                    else:
                        self.Merge(
                            node,
                            parent.children[index + 1],
                            parent,
                            index,
                            RIGHT_SIBLING,
                        )
                        self.Remove(k, _call_depth + 1)
            else:
                # Caso 2: remoção em nó interno
                index = node.keys.index(k)
                if len(node.children[index].keys) > self.t - 1:
                    # Caso 2a: substituir pelo antecessor (maior chave da subárvore esquerda)
                    predessor = node.children[index].keys[
                        len(node.children[index].keys) - 1
                    ]
                    node.keys[index] = predessor
                    node.children[index].keys.pop(-1)
                    return
                elif len(node.children[index + 1].keys) > self.t - 1:
                    # Caso 2a: substituir pelo sucessor (menor chave da subárvore direita)
                    sucessor = node.children[index + 1].keys[0]
                    node.keys[index] = sucessor
                    node.children[index + 1].keys.pop(0)
                    return
                # Caso 2b: mesclar os dois filhos e tentar remover novamente
                self.Merge(
                    node.children[index],
                    node.children[index + 1],
                    node,
                    index,
                    RIGHT_SIBLING,
                )
                self.Remove(k, _call_depth + 1)

    # Imprime a árvore nível a nível de forma indentada,
    # marcando raiz e folhas para visualização da estrutura.
    # Input:  BNode | None, int
    # Output: None
    def PrintTree(self, node=None, level=0):
        if node is None:
            node = self.root
        print(
            "  " * level
            + f"Level {level}: {node.keys} {'(raiz)' if level == 0 else ''} {'(folha)' if node.leaf else ''}"
        )
        if not node.leaf:
            for child in node.children:
                self.PrintTree(child, level + 1)


def main():
    btree = BTree(2)
    print("======================")
    print("        B-TREE:       ")
    print("======================\n")
    print("t = 2\n")
    print("======================")
    print("       INSERÇÃO       ")
    print("======================\n")
    print("10, 20 e 5 (caso 1):")
    btree.Insert(10)
    btree.Insert(20)
    btree.Insert(5)
    btree.PrintTree()
    print("\n15 (caso 2):")
    btree.Insert(15)
    btree.PrintTree()
    print("\n25, 3 e 7 (caso 1):")
    btree.Insert(25)
    btree.Insert(3)
    btree.Insert(7)
    btree.PrintTree()
    print("\n12 (caso 2):")
    btree.Insert(12)
    btree.PrintTree()
    print("\n17, 22 e 27 (caso 1):")
    btree.Insert(17)
    btree.Insert(22)
    btree.Insert(27)
    btree.PrintTree()
    print("\n2 (caso 2):")
    btree.Insert(2)
    btree.PrintTree()
    print("\n4, 6 e 8 (caso 1):")
    btree.Insert(4)
    btree.Insert(6)
    btree.Insert(8)
    btree.PrintTree()
    print("\n11 (caso recursivo):")
    btree.Insert(11)
    btree.PrintTree()
    print("\n13, 16, 18 e 21 (caso 1):")
    btree.Insert(13)
    btree.Insert(16)
    btree.Insert(18)
    btree.Insert(21)
    btree.PrintTree()
    print("\n23 (caso 2):")
    btree.Insert(23)
    btree.PrintTree()
    print("\n26 e 28 (caso 1):")
    btree.Insert(26)
    btree.Insert(28)
    btree.PrintTree()
    print("\n======================")
    print("       REMOÇÃO       ")
    print("======================\n")
    print("2 e 4 (casos 1a):")
    btree.Remove(2)
    btree.Remove(4)
    btree.PrintTree()
    print("\n3 (caso 1b):")
    btree.Remove(3)
    btree.PrintTree()
    print("\n8, 11, 12, 16 e 17 (casos 1a):")
    btree.Remove(8)
    btree.Remove(11)
    btree.Remove(12)
    btree.Remove(16)
    btree.Remove(17)
    btree.PrintTree()
    print("\n13 (caso 1c):")
    btree.Remove(13)
    btree.PrintTree()
    print("\n20 (caso 2a):")
    btree.Remove(20)
    btree.PrintTree()
    print("\n22 e 23(casos 1a):")
    btree.Remove(22)
    btree.Remove(23)
    btree.PrintTree()
    print("\n18 (caso 2b):")
    btree.Remove(18)
    btree.PrintTree()
    print("\n6 (Caso recursivo):")
    btree.Remove(6)
    btree.PrintTree()

    print("\n======================")
    print("       PESQUISA      ")
    print("======================\n")
    if btree.Search(28, btree.root) is not None:
        print("Número 28 encontrado!")
    else:
        print("Número 28 não foi encontrado!")
    if btree.Search(51, btree.root) is not None:
        print("Número 51 encontrado!")
    else:
        print("Número 51 não foi encontrado!")


if __name__ == "__main__":
    main()
