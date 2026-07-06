# B-Tree — Gerador de Árvore Binária

Implementação de uma **Árvore B** (B-Tree) de grau `t` em Python, com operações completas de inserção, remoção e busca. Apesar do nome do diretório, a estrutura é uma **B-Tree**, e não uma árvore binária simples.

**Desenvolvedor:** Kayky Moreira Praxedes

---

## O que é uma B-Tree?

Uma B-Tree é uma estrutura de dados balanceada onde cada nó pode armazenar **múltiplas chaves** e ter **múltiplos filhos**. Diferente de uma árvore binária (que tem no máximo 2 filhos por nó), a B-Tree é otimizada para sistemas que trabalham com grandes volumes de dados, como bancos de dados e sistemas de arquivos.

**Propriedades fundamentais:**
- Cada nó contém entre `t - 1` e `2t - 1` chaves (exceto a raiz, que pode ter de 1 a `2t - 1`)
- Cada nó não-folha com `n` chaves tem exatamente `n + 1` filhos
- Todas as folhas estão na **mesma profundidade**
- As chaves dentro de cada nó são mantidas **ordenadas**

---

## Funcionalidades

- **Inserção** — Insere chaves mantendo o balanceamento da árvore, dividindo nós cheios (`split`) quando necessário.
- **Remoção** — Remove chaves cobrindo todos os casos da literatura (folha, nó interno, empréstimo entre irmãos, fusão de nós).
- **Busca** — Localiza uma chave percorrendo a árvore a partir da raiz.
- **Visualização** — Exibe a árvore formatada por níveis, indicando raiz e folhas.

---

## Estrutura do código

| Constante | Valor | Significado |
|---|---|---|
| `IRMAO_ESQUERDO` | `-1` | Indica operação com o irmão esquerdo |
| `IRMAO_DIREITO` | `0` | Indica operação com o irmão direito |
| `MAX_DEPTH` | `100` | Limite de segurança contra recursão infinita |

**Classe `bNode` (nó):** `leaf` (bool, se é folha), `keys` (chaves armazenadas), `children` (referências aos filhos).

**Classe `bTree` (árvore):** `root` (nó raiz), `t` (grau mínimo).

---

## Módulos

### Inserção

A inserção (`insert(k)`) navega até a folha apropriada via `goLeaf`. Se a folha tem espaço (`len(keys) < 2t - 1`), insere `k` mantendo a ordem. Se está cheia, divide o nó (`split`) e tenta novamente.

O `split(node)` divide um nó cheio em dois irmãos, promovendo a chave mediana para o pai — criando uma nova raiz se necessário, e cascateando recursivamente se o pai também estiver cheio.

### Remoção

A remoção (`remove(k)`) cobre todos os casos clássicos:

**Remoção em folha:**
1. **1a** — folha acima do mínimo: remove diretamente
2. **1b** — folha no mínimo, mas um irmão tem chaves extras: empréstimo via `passKey`
3. **1c** — folha e irmãos no mínimo: fusão via `merge`, depois tenta remover novamente

**Remoção em nó interno:**
1. **2a** — algum filho tem mais que o mínimo: substitui pela chave predecessora/sucessora
2. **2b** — ambos os filhos no mínimo: funde os dois filhos via `merge`

O `merge(node, sibling, parent, index, pm)` funde dois nós irmãos quando ambos estão no mínimo de chaves; se o pai também ficar sem chaves extras, a fusão pode cascatear até o avô. `passKey` faz o inverso: transfere uma chave do pai para o nó, compensando com uma chave do irmão. `findParent` localiza o pai de um nó recursivamente.

### Busca

`search(k, node)` desce recursivamente pela árvore: retorna o nó se `k` estiver nele, `None` se chegar numa folha sem encontrar, ou desce para o filho apropriado.

---

## Segurança contra loops infinitos

Todas as funções recursivas (`goLeaf`, `findParent`, `split`, `insert`, `search`, `merge`, `remove`) possuem o parâmetro `_call_depth`, incrementado a cada chamada. Se `MAX_DEPTH` (100) for excedido, um `RecursionError` é levantado, prevenindo loops infinitos causados por bugs na lógica de reorganização.

---

## Testes

A função `main()` executa uma bateria de testes manuais:

1. **Inserções** — 20 chaves, alternando nós com espaço e nós cheios (disparando splits)
2. **Remoções** — 13 chaves, cobrindo os casos 1a, 1b, 1c, 2a, 2b e remoção recursiva
3. **Buscas** — chave existente (28) e inexistente (51)

---

## Uso

```python
btree = bTree(2)  # grau mínimo = 2
```

Com `t = 2`, cada nó pode ter entre 1 e 3 chaves, e cada nó não-folha tem entre 2 e 4 filhos.
