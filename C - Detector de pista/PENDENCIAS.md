# Pendências — Detector de Pista

Catálogo de problemas identificados no código, organizados por severidade
(do menos ao mais crítico).

---

## 🟡 Estilo e Legibilidade

### 1. Mistura pt-BR / inglês em nomes

A `struct lista` mistura `Chave`, `Tipo`, `NumElementos`, `PontoMedio` (português)
com `nextPtr` (inglês). Escolher um idioma e manter consistência facilita
a leitura.

**Localização:** `Código/detectarPista.c:11-16`

---

### 2. Typedef que esconde ponteiro (`LISTAPTR`)

`typedef LISTA *LISTAPTR;` obscurece o fato de que `LISTAPTR` é um ponteiro.
Em revisões de código é fácil confundir passagem por valor vs. referência.
A prática recomendada é manter o `*` visível.

**Localização:** `Código/detectarPista.c:22`

---

### 3. Capitalização inconsistente de parâmetros

`Chave` (maiúsculo) vs. `quantidade`, `lista`, `tamanho` (minúsculos) —
parâmetros da mesma função deveriam seguir a mesma regra.

**Localização:** espalhado por todas as funções

---

### 4. Nomes pouco descritivos

`testa()`, `auxRepetido`, `auxLista`, `validf`, `cont` — nomes que não
revelam a intenção ou o conteúdo da variável/função sem ler a implementação.

**Localização:** `Código/detectarPista.c:33-136`

---

### 5. Estilo de nomenclatura inconsistente

- `camelCase`: `PontoMedio`, `NumElementos`
- `snake_case`: `freePtr`, `contaObs`
- `PascalCase`: `TestaObstaculo` (única função com inicial maiúscula)

**Localização:** geral

---

### 6. Formatação irregular

`for(int i = 0;i<tamanho; i++){` — falta espaçamento após `;` e antes de `{`.
Dificulta a varredura visual rápida do código.

**Localização:** `Código/detectarPista.c:130`

---

## 🟠 Complexidade Desnecessária

### 7. Lista encadeada: estrutura superdimensionada para o problema

O agrupamento de valores consecutivos poderia ser feito com um simples array
de structs durante a leitura. A lista encadeada com alocação dinâmica adiciona
complexidade (gerenciamento manual de memória, percorrimento repetido, lógica
de inserção) sem benefício mensurável para o cenário — o número de valores
por linha é conhecido antes da leitura (`quantidade`).

**Envolve:** `novo()`, `inserir()`, `freePtr()`

---

### 8. Aninhamento excessivo em `testa()` e `TestaObstaculo()`

Cinco níveis de `if` aninhados (linhas 71-87 e 99-119) prejudicam a legibilidade
e aumentam a chance de erros de lógica. Refatorar com early returns ou
extrair subfunções resolveria.

**Localização:** `Código/detectarPista.c:71-87`, `95-126`

---

### 9. `inserir()` sobrecarregada

A função acumula três responsabilidades: (a) percorrer a lista para verificar
se a chave já existe, (b) inserir novo nó, (c) reclassificar os tipos de nós
existentes quando um novo valor aparece. Separar em funções menores
(aumentaria testabilidade e clareza.

**Localização:** `Código/detectarPista.c:33-63`

---

### 10. Algoritmo de classificação de tipos (1/2/3) frágil

A lógica que atribui tipos 1, 2, 3 baseada em ordem de primeira aparição
e depois reclassifica nós existentes é difícil de validar mentalmente. Uma
mudança na ordem de entrada dos valores do sensor pode produzir
classificações inesperadas sem que isso seja óbvio para o leitor.

**Localização:** `Código/detectarPista.c:49-62`

---

## 🔴 Gerenciamento de Memória

### 11. Vazamento se `scanf` falhar

O primeiro nó é alocado em `novo()` na linha 158 antes do `scanf` da
`Chave`. Se o `scanf` falhar, o nó alocado não é liberado — não há
`freePtr` em nenhum caminho de erro.

**Localização:** `Código/detectarPista.c:157-158`

---

### 12. Campo `PontoMedio` na struct aponta para variável da pilha

Todos os nós compartilham o mesmo ponteiro `&PontoMedio` (variável local
de `main`). O campo nunca é efetivamente usado para nada — é um resquício
de versão anterior ou confusão conceitual. Gera ruído e pode enganar
quem mantém o código.

**Localização:** `Código/detectarPista.c:15,29,47`

---

### 13. `freePtr` com `prevPtr` não inicializado na primeira iteração

`prevPtr = *lista` na linha 141 escreve em `prevPtr` antes de qualquer
leitura, então tecnicamente não é um bug de UB, mas a declaração sem
inicializador (`LISTAPTR prevPtr;`) seguida de atribuição imediata
pode levantar alertas em analysers estáticos.

**Localização:** `Código/detectarPista.c:138-145`

---

## 🔴🔴 Erros Lógicos

### 14. `TestaObstaculo()` jamais é invocada (CRÍTICO)

Na linha 164: `obstaculos[i] = obstaculo;` — a variável `obstaculo` NUNCA
recebe o retorno de `TestaObstaculo()`; ela é usada sem inicialização, o
que é **comportamento indefinido** em C. Consequência: a detecção de
impedimentos é **completamente inoperante**, e o valor armazenado em
`obstaculos[]` é imprevisível.

**Localização:** `Código/detectarPista.c:152,164`

---

### 15. Classificação de curva usa apenas 2 pontos

As condições das linhas 183-186 comparam `PontosMedios[0]` (primeira linha)
com `PontosMedios[validf]` (última linha válida) para decidir direção da
curva. Duas amostras são insuficientes — ignoram oscilações intermediárias
e podem classificar erroneamente ruído como curva. O correto seria analisar
a tendência em todas as linhas.

**Localização:** `Código/detectarPista.c:183-186`

---

### 16. Threshold assimétrico para linha reta

Comentário na linha 180 indica `media ± 14`, mas a condição real na linha 181
usa `media + 14` e `media - 30`. Provável erro de digitação (`30` no lugar
de `14`). Isso torna a detecção muito mais permissiva para variações negativas
do que para positivas.

**Localização:** `Código/detectarPista.c:181`

---

### 17. `return 10` vs. `return 1` em `TestaObstaculo`

A função retorna `10` na linha 108 (obstáculo "completo") e `1` na linha 115
(obstáculo "parcial"). `contaObs()` só conta valores `== 1`, então mesmo
que `TestaObstaculo` fosse chamada, os obstáculos do tipo `10` seriam
silenciosamente ignorados.

**Localização:** `Código/detectarPista.c:108,115,131`

---

### 18. Saída pode ficar corrompida

Se a última linha válida não se encaixar em nenhuma das três condições
(L181-186), o bloco `if(numObs > 0)` ainda executa, imprimindo algo como
`" com impedimento.\n"` sem o prefixo de pista/curva.

**Localização:** `Código/detectarPista.c:181-192`

---

### 19. `previousPtr` pode ser `NULL` em `inserir()`

Se a lista estiver vazia (nó cabeça `NULL`), `previousPtr` nunca é
atribuído, e o acesso `previousPtr->PontoMedio` na linha 47 causa
falha de segmentação. O fluxo atual do `main()` sempre cria o primeiro
nó antes de chamar `inserir()`, mas a função não é segura para uso
genérico.

**Localização:** `Código/detectarPista.c:44,47`

---

## ⚪ Portabilidade e Boas Práticas

### 20. VLA (`Variable Length Array`)

`int PontosMedios[L]` — VLA é opcional no C11 e foi removido no C23.
Compiladores podem não suportar ou emitir avisos. Alternativa: alocação
dinâmica com `malloc`.

**Localização:** `Código/detectarPista.c:151`

---

### 21. `scanf` sem validação de retorno

Nenhuma chamada de `scanf` verifica se a leitura foi bem-sucedida. Se a
entrada estiver mal formatada, o programa opera com valores indefinidos.

**Localização:** `Código/detectarPista.c:150,154,157`

---

### 22. Acento faltando em mensagem

`"nao"` sem o acento circunflexo — `"não"`.

**Localização:** `Código/detectarPista.c:193`
