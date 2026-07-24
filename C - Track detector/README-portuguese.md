# Detector de Pista

Implementação em C que processa leituras de sensores ópticos (valores 0, 128, 255) para detectar faixas de pista, classificar curvas (esquerda/direita) e identificar impedimentos — usando listas encadeadas com agrupamento de valores consecutivos iguais e classificação por ordem de aparição.

**Desenvolvedores:** Kayky Moreira Praxedes, Carlos Ernesto Cardoso dos Reis

---

## O que é Detecção de Pista?

Sistemas seguidores de linha (line followers) usam sensores ópticos que retornam valores de refletância: **0** (preto/sombra), **128** (cinza/borda) e **255** (branco/pista). Cada linha do sensor escaneia uma seção transversal da pista. O programa agrupa valores consecutivos iguais, classifica cada grupo em um dos 3 tipos (1/2/3) por ordem de primeira aparição, e busca o padrão **(1, 3, 2, 3, 1)** — que representa respectivamente borda esquerda, ombro esquerdo, centro da pista, ombro direito, borda direita.

### Propriedades fundamentais

- O padrão (1, 3, 2, 3, 1) é a assinatura de uma faixa de pista válida
- A posição do grupo tipo 2 (centro) define o ponto médio da pista
- Curvas são detectadas pela variação do ponto médio entre linhas
- Obstáculos são padrões anômalos que interrompem a sequência esperada

---

## Funcionalidades

- **Classificação de dados do sensor** — agrupa valores consecutivos iguais em nós de lista encadeada e atribui tipos (1, 2, 3) por ordem de aparição
- **Detecção de pista** — localiza o padrão (1, 3, 2, 3, 1) na lista classificada e calcula o ponto médio da faixa
- **Classificação de curva** — compara o primeiro com o último ponto médio válido para decidir entre reta, curva à esquerda ou curva à direita
- **Detecção de impedimentos** — reconhece padrões pós-pista que indicam obstáculos

---

## Estrutura do Projeto

```
Code/
├── Makefile                # Compilação e execução dos testes
├── detectarPista.c         # Programa principal
└── test-cases/
    ├── test-case_1.txt     # Pista em linha reta
    ├── test-case_2.txt     # Pista em linha reta
    ├── test-case_3.txt     # Curva à esquerda
    ├── test-case_4.txt     # Pista em linha reta
    ├── test-case_5.txt     # Curva à direita
    └── test-case_6.txt     # Pista em linha reta
```

| Constante | Valor | Significado |
|---|---|---|
| `PADRAO_PISTA` | `(1, 3, 2, 3, 1)` | Sequência de tipos que identifica a pista |
| `LIMIAR_VALIDADE` | `70%` | % mínima de linhas com ponto médio válido |
| `TOLERANCIA_RETA` | `±14` | Variação máxima da média para reta |
| `TOLERANCIA_CURVA` | `±15` | Limiar de variação para classificar curva |

---

## Módulos

### Módulo de Classificação (`CreateNode` / `InsertKey`)

Recebe as chaves brutas do sensor e as organiza em uma lista encadeada agrupando valores consecutivos iguais. A cada novo valor, verifica se ele já apareceu antes na mesma linha: se sim, reutiliza o tipo anterior; se não, cria um novo nó com tipo 1 e reclassifica os tipos dos nós existentes para manter a ordenação (1, 2, 3) por ordem crescente de chave.

A lógica de inserção é dividida em três funções auxiliares internas:
- `FindKeyType` — percorre a lista buscando a chave e retorna o último nó
- `AppendNode` — cria um novo nó e o anexa ao final da lista
- `ReclassifyByKey` — ajusta os tipos de todos os nós quando uma nova chave distinta é inserida

### Módulo de Detecção de Pista (`FindLane`)

Percorre a lista classificada em busca do padrão (1, 3, 2, 3, 1). Quando encontra, calcula o ponto médio acumulando os `element_count` parciais:

1. Acumula elementos do tipo 1 (borda esquerda)
2. Soma elementos do tipo 3 (ombro esquerdo)
3. Adiciona metade dos elementos do tipo 2 (centro da pista)
4. Ignora tipo 3 (ombro direito) e tipo 1 (borda direita)

**Retorna:** ponto médio da pista, ou `-1` se o padrão não for encontrado.

A correspondência de padrões usa duas funções auxiliares compartilhadas:
- `MatchPattern5` — casa 5 tipos consecutivos e calcula a contribuição ao ponto médio
- `FindSubPattern` — casa uma subsequência de qualquer comprimento

### Módulo de Detecção de Obstáculos (`CheckObstacle`)

Detecta variações do padrão que indicam impedimentos na pista:

1. Busca o padrão base (1, 3, 2, 3, 1) — se encontrado, retorna 0 (pista limpa)
2. Caso contrário, busca o prefixo (1, 3, 2) seguido por um fechamento (3, 1) mais adiante — se encontrado, retorna 1 (impedimento)
3. Retorna `-1` se nenhum padrão de pista for detectado

### Utilitários

- **`CountObstacles(vetor, tamanho)`** — conta quantas linhas têm obstáculo (valores `== 1` no vetor)
- **`FreeList(lista)`** — percorre a lista liberando cada nó da memória

### Função Principal (`main`)

1. Lê o número `L` de linhas de sensor
2. Aloca dinamicamente arrays para pontos médios e obstáculos (com verificação de nulidade na alocação)
3. Para cada linha, lê `quantidade` valores, classifica em lista encadeada, calcula o ponto médio e status de obstáculo, e libera a lista
4. Se ≥70% das linhas tiverem ponto médio válido, calcula a média e decide:
   - **Linha reta** — último ponto médio dentro de ±14 da média
   - **Curva à direita** — último ponto médio menor que o primeiro
   - **Curva à esquerda** — último ponto médio maior que o primeiro
5. Informa se há impedimentos na pista

---

## Decisões de Projeto

Este projeto foi desenvolvido sob diretrizes acadêmicas específicas. Algumas escolhas de design refletem restrições pedagógicas da professora em vez de otimização puramente técnica:

- **Classificação por ordem de aparição**: os tipos 1, 2, 3 dependem da sequência em que os valores do sensor são processados — uma simplificação deliberada para ensinar travessia de lista e reclassificação. Uma alternativa baseada em ordenação absoluta por chave foi projetada mas não aplicada por requisito do projeto.
- **Curva decidida por apenas 2 pontos** (primeira e última linha válida) — requisito da professora para manter a lógica de decisão simples. Uma solução mais robusta usando regressão linear em todos os pontos médios válidos foi considerada.
- **Estrutura de dados de lista encadeada** — mantida em vez de um array simples apesar do espaço fixo de chaves (3 valores), mantendo a porta aberta para dados de sensor de comprimento variável em expansões futuras.
- **Mínimo de 70% de linhas válidas**: abaixo desse limiar, o programa retorna "Formato da pista nao estimado." sem detalhamento adicional.

---

## Testes

Seis casos de teste localizados em `Code/casos-teste/`. Cada um contém 15 linhas de sensor com 950 valores por linha (valores 0, 128, 255).

1. **test-case_1** — Pista em linha reta simétrica, sem impedimento
2. **test-case_2** — Pista em linha reta com leve deslocamento lateral, sem impedimento
3. **test-case_3** — Curva à esquerda (padrão desloca-se progressivamente para a esquerda entre as linhas), sem impedimento
4. **test-case_4** — Pista em linha reta, sem impedimento
5. **test-case_5** — Curva à direita com impedimento
6. **test-case_6** — Pista em linha reta com impedimento

---

## Uso / Configuração

Compilar e executar com `make`:

```bash
cd Code
make                # compila e executa todos os casos de teste
make test-case_1    # executa apenas o caso 1
make test-case_3    # executa apenas o caso 3
```

Execução manual com um caso específico:

```bash
gcc -o detectarPista detectarPista.c
./detectarPista < casos-teste/test-case_3.txt
```

Formato da entrada:

```
L                       # número de linhas de sensor
Q1                      # quantidade de valores na linha 1
v1 v2 ... vQ1           # valores do sensor (0, 128, 255)
Q2                      # quantidade de valores na linha 2
v1 v2 ... vQ2
...
```

Saída esperada:

```
Pista em linha reta e sem impedimento.
Curva a esquerda e com impedimento.
Formato da pista nao estimado.
```
