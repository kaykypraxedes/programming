# Detector de Pista

Implementação em C que processa leituras de sensores ópticos (valores 0,
128, 255) para detectar faixas de pista, classificar curvas (esquerda/direita)
e identificar impedimentos — usando listas encadeadas com agrupamento de
valores consecutivos iguais e classificação por ordem de aparição.

**Desenvolvedores:** Kayky Moreira Praxedes, Carlos Ernesto Cardoso dos Reis

---

## O que é Detecção de Pista?

Sistemas seguidores de linha (line followers) usam sensores ópticos que
retornam valores de refletância: **0** (preto/sombra), **128** (cinza/borda)
e **255** (branco/pista). Cada linha do sensor escaneia uma seção transversal
da pista. O programa agrupa valores consecutivos iguais, classifica cada
grupo em um dos 3 tipos (1/2/3) por ordem de primeira aparição, e busca o
padrão **(1, 3, 2, 3, 1)** — que representa respectivamente borda esquerda,
ombro esquerdo, centro da pista, ombro direito, borda direita.

### Propriedades fundamentais

- O padrão (1, 3, 2, 3, 1) é a assinatura de uma faixa de pista válida
- A posição do grupo tipo 2 (centro) define o ponto médio da pista
- Curvas são detectadas pela variação do ponto médio entre linhas
- Obstáculos são padrões anômalos que interrompem a sequência esperada

---

## Funcionalidades

- **Classificação de dados do sensor** — agrupa valores consecutivos iguais
  em nós de lista encadeada e atribui tipos (1, 2, 3) por ordem de aparição
- **Detecção de pista** — localiza o padrão (1, 3, 2, 3, 1) na lista
  classificada e calcula o ponto médio da faixa
- **Classificação de curva** — compara o primeiro com o último ponto médio
  válido para decidir entre reta, curva à esquerda ou curva à direita
- **Detecção de impedimentos** — reconhece padrões pós-pista que indicam
  obstáculos (atualmente inoperante — ver Pendências #14)

---

## Estrutura do Projeto

```
C - Detector de pista/
├── README.md                    # Documentação do projeto
├── TEMPLATE_README.md           # Template usado para o README
├── PENDENCIAS.md                # Catálogo de bugs e melhorias
├── Resumo do projeto.txt        # Descrição textual resumida
└── Código/
    ├── Makefile                 # Compilação e execução dos testes
    ├── detectarPista.c          # Programa principal (~195 linhas)
    └── casos-teste/
        ├── detectarPista-casoTeste-1.txt  # Pista em linha reta
        ├── detectarPista-casoTeste-2.txt  # Pista em linha reta
        ├── detectarPista-casoTeste-3.txt  # Curva à esquerda
        └── detectarPista-casoTeste-4.txt  # Pista em linha reta
```

| Constante | Valor | Significado |
|---|---|---|
| `PADRAO_PISTA` | `(1, 3, 2, 3, 1)` | Sequência de tipos que identifica a pista |
| `LIMIAR_VALIDADE` | `70%` | % mínima de linhas com ponto médio válido |
| `TOLERANCIA_RETA_SUP` | `+14` | Variação máxima acima da média para reta |
| `TOLERANCIA_RETA_INF` | `-30` | Variação máxima abaixo da média para reta |
| `TOLERANCIA_CURVA` | `±15` | Variação para classificar curva |

---

## Módulos

### Módulo de Classificação (`novo` / `inserir`)

Recebe as chaves brutas do sensor e as organiza em uma lista encadeada
agrupando valores consecutivos iguais. A cada novo valor, verifica se ele
já apareceu antes na mesma linha: se sim, reutiliza o tipo anterior; se
não, cria um novo nó com tipo 1 e reclassifica os tipos dos nós existentes
para manter a ordenação (1, 2, 3) por ordem crescente de chave.

### Módulo de Detecção de Pista (`testa`)

Percorre a lista classificada em busca do padrão (1, 3, 2, 3, 1).
Quando encontra, calcula o ponto médio acumulando os `NumElementos` parciais:

1. Acumula elementos do tipo 1 (borda esquerda)
2. Soma elementos do tipo 3 (ombro esquerdo)
3. Adiciona metade dos elementos do tipo 2 (centro da pista)
4. Ignora tipo 3 (ombro direito) e tipo 1 (borda direita)

**Retorna:** ponto médio da pista, ou `-1` se o padrão não for encontrado.

### Módulo de Detecção de Obstáculos (`TestaObstaculo`)

Detecta variações do padrão que indicam impedimentos na pista:

1. Busca o padrão base (1, 3, 2, 3, 1)
2. Se houver um fechamento direto (3, 1), retorna 10
3. Se houver um segundo padrão (3, 1) após o fechamento, retorna 1
4. Retorna `-1` se não houver impedimento

**Nota:** Esta função **nunca é chamada** no `main()` atual (veja Pendência #14).

### Utilitários

- **`contaObs(vetor, tamanho)`** — conta quantas linhas têm obstáculo
  (valores `== 1` no vetor)
- **`freePtr(lista)`** — percorre a lista liberando cada nó da memória

### Função Principal (`main`)

1. Lê o número `L` de linhas de sensor
2. Para cada linha, lê `quantidade` valores, classifica em lista encadeada,
   calcula o ponto médio e libera a lista
3. Se ≥70% das linhas tiverem ponto médio válido, calcula a média e decide:
   - **Linha reta** — pontos médios dentro da tolerância
   - **Curva à direita** — último ponto médio menor que o primeiro
   - **Curva à esquerda** — último ponto médio maior que o primeiro
4. Informa se há impedimentos na pista

---

## Segurança / Limitações / Robustez

- **Classificação por ordem de aparição**: os tipos 1, 2, 3 dependem da
  sequência em que os valores do sensor são processados — se a ordem
  esperada (ex: 0 → 255 → 128) não for respeitada, a classificação pode
  produzir falsos positivos ou negativos.
- **Mínimo de 70% de linhas válidas**: abaixo desse limiar, o programa
  retorna "Formato da pista nao estimado." sem detalhamento adicional.
- **Detecção de obstáculos inoperante**: a função `TestaObstaculo()` não é
  chamada em nenhum ponto do `main()` (veja `PENDENCIAS.md #14`).
- **Curva decidida por apenas 2 pontos** (primeira e última linha) —
  insuficiente para padrões de curva reais (veja `PENDENCIAS.md #15`).
- **Alocação dinâmica sem tratamento de falha**: `malloc` nunca tem seu
  retorno verificado.
- **Projeto educacional**: não recomendado para uso em produção sem as
  correções listadas em `PENDENCIAS.md`.

---

## Testes

Quatro casos de teste localizados em `Código/casos-teste/`. Cada um contém
15 linhas de sensor com 950 valores por linha (valores 0, 128, 255).

1. **casoTeste-1** — Pista em linha reta simétrica, sem impedimento
2. **casoTeste-2** — Pista em linha reta com leve deslocamento lateral,
   sem impedimento
3. **casoTeste-3** — Curva à esquerda (padrão desloca-se progressivamente
   para a esquerda entre as linhas), sem impedimento
4. **casoTeste-4** — Pista em linha reta, sem impedimento

---

## Uso / Configuração

Compilar e executar com `make`:

```bash
cd Codigo
make             # compila detectarPista
make run-all     # executa os 4 casos de teste
make run-teste1  # executa apenas o caso 1
```

Execução manual com um caso específico:

```bash
gcc -o detectarPista detectarPista.c
./detectarPista < casos-teste/detectarPista-casoTeste-3.txt
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
