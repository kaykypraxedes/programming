# Pendências e Melhorias

Análise detalhada de todos os problemas identificados no código `aeroporto.c`, organizados do mais leve ao mais estrutural.

---

## 1. Erros de Digitação e Formatação

| # | Local | Problema | Gravidade |
|---|-------|----------|-----------|
| 1 | Linhas 244, 354, 503, 551 | `"Indentificador"` — erro de digitação, o correto é `"Identificador"` | Muito Baixa |
| 2 | Linha 536 | `"RS%.2lf\n"` — símbolo da moeda errado, deveria ser `"R$%.2lf\n"` | Muito Baixa |
| 3 | Linha 107 | Comentário `//Add passageiro 1` repetido para o passageiro 2 (deveria ser `"passageiro 2"`) | Muito Baixa |
| 4 | Linhas 95, 107, 119 | Comentários inconsistentes — alguns sem espaço após `//` (`//Add` vs `// Add`) | Muito Baixa |
| 5 | Linha 67 | Comentário em inglês `"Adiciona elementos de teste"` — inconsistência com o resto do código em português | Muito Baixa |

---

## 2. Organização e Redundância

| # | Local | Problema | Gravidade |
|---|-------|----------|-----------|
| 6 | Linha 241-242 | Variável `prevptr` declarada em `adicionar` voo mas **nunca utilizada** | Baixa |
| 7 | Linha 302, 331 | Variável `prevptr` declarada em `adicionar` passagem mas **nunca utilizada** | Baixa |
| 8 | Linha 351, 377 | Variável `prevptr` declarada em `adicionar` passageiro mas **nunca utilizada** | Baixa |
| 9 | Linha 242, 276 | Variável `atualptr` declarada duas vezes em escopos diferentes dentro de `adicionar` voo — redundante e confuso | Baixa |
| 10 | Linha 55-60 | Protótipos com nomes de parâmetros divergentes das definições — `acao(VOOSPTR *, ...)` vs `acao(VOOSPTR *vooptr, ...)` | Baixa |
| 11 | Linhas 53-54 | `quantidade_total_voos` é atualizado, mas `quantidade_total_passageiros` nunca é atualizado nas funções CRUD (só na `main`) | Média |
| 12 | Linha 21, 45 | Campos `qvoos` e `qpassageiros` dentro das structs atuam como contadores globais, mas estão acoplados ao primeiro nó da lista — conceitualmente errado | Média |
| 13 | Geral | Indentação inconsistente — mistura estilos de alinhamento em todo o arquivo | Baixa |
| 14 | Linha 190-210 | `menu()` e `menuinterno()` são virtualmente idênticas — poderiam ser unificadas com parâmetro para o título | Baixa |
| 15 | Linha 163-185 | Bloco `switch` em `main()` com repetição de `acao(&voo, &passagem, &passageiro, escolha, escint)` — poderia ser simplificado | Baixa |

---

## 3. Bugs de Alocação e Memória

| # | Local | Problema | Gravidade |
|---|-------|----------|-----------|
| 16 | Linhas 70-157 | Dados de teste alocados com `malloc` mas **nunca liberados** — vazamento ao encerrar o programa | Média |
| 17 | Linha 243 (e todas as outras alocações) | Nenhuma chamada de `malloc` verifica retorno NULL — se a alocação falhar, ocorre **crash** | Alta |
| 18 | Linha 187 | `main()` retorna sem percorrer as listas para liberar a memória com `free()` | Média |

---

## 4. Bugs de Lógica (Críticos)

| # | Local | Problema | Gravidade |
|---|-------|----------|-----------|
| 19 | **Linhas 291-296** | **ACESSO A PONTEIRO NULO (CRASH).** O loop `while(teste != NULL) teste = teste->next;` percorre até o fim. Depois `teste->numero >= 100` desreferencia `teste` que é **sempre NULL**. Além disso, se a lista estiver vazia (`*psptr == NULL`), a verificação de limite é **pulada inteiramente**, permitindo criar a primeira passagem sem validação de limite. | **Crítica** |
| 20 | **Linhas 356-364** | **ACESSO A PONTEIRO NULO (CRASH).** Se houver apenas 1 passageiro na lista e o ID do novo for diferente, o loop `while(atualptr != NULL && ...)` termina com `atualptr == NULL`. A linha 360 então faz `atualptr->identificador`, causando **crash**. | **Crítica** |
| 21 | Linha 281 | `(*vptr)->qvoos++` — ao adicionar um voo no final, incrementa o campo `qvoos` **do primeiro voo**, corrompendo seu dado. | Alta |
| 22 | Linha 387 | `(*paptr)->qpassageiros++` — mesmo problema do item 21: incrementa o contador **do primeiro passageiro**, não de um contador global. | Alta |
| 23 | **Linhas 600-601** | Ao remover passageiro via remoção de voo, `(*paptr)->qpassageiros--` decrementa o contador **do (novo) primeiro nó**, não do nó correto. Se o passageiro removido for o primeiro, `*paptr` já foi atualizado e o decremento afeta o nó errado. | Alta |
| 24 | **Linhas 634-637** | Se o voo removido for o único (lista fica vazia), `*vptr` será NULL, o `if` falha, e `quantidade_total_voos` **não é decrementado**, ficando incorreto. | Alta |
| 25 | **Linhas 752-766** | Relatório "voos por empresa" imprime **linhas repetidas**. Para cada voo, o loop interno percorre a lista inteira contando todos os voos daquela empresa e imprime. Se a empresa X tem 3 voos, a linha aparece **3 vezes**. | Alta |
| 26 | Linha 342 | `newptr->numero = prevptr->numero + 1` — numeração sequencial frágil. Se passagens intermediárias forem removidas, uma nova passagem pode receber um número já existente, causando duplicata. | Média |
| 27 | Linha 20 | Campo `quantidade_passageiros` em `VOOS` é declarado mas **nunca atualizado** — o sistema recalcula dinamicamente na consulta | Média |

---

## 5. Problemas de Validação e Input

| # | Local | Problema | Gravidade |
|---|-------|----------|-----------|
| 28 | Geral | `scanf` sem validação de retorno — entrada não-numérica em `%d` causa **loop infinito** ou comportamento indefinido | Alta |
| 29 | Linhas 259, 261, 263, 266, 268 | `scanf(" %[^\n]", ...)` sem limite de caracteres — **buffer overflow** se o usuário digitar mais que o tamanho do campo (ex: `char empresa[20]` pode receber 50 caracteres) | Alta |

---

## 6. Melhorias Arquiteturais (Grande Porte)

| # | Problema | Gravidade |
|---|----------|-----------|
| 30 | **Código monolítico** — ~790 linhas em um único `.c`. Sem headers, sem separação de responsabilidades (CRUD, relatórios, listas, UI tudo misturado). | Alta |
| 31 | **Zero funções auxiliares** — o padrão de busca `while(atualptr != NULL && atualptr->campo != valor)` se repete ~10 vezes. Faltam funções como `buscarVooPorId()`, `buscarPassageiroPorId()`, etc. | Alta |
| 32 | **Responsabilidade única violada** — `remover` faz remoção em cascata (voo → passagens + passageiros) dentro de uma única função de ~70 linhas. | Alta |
| 33 | **Dados de teste fixos** — carga na `main()` sem flag de compilação ou possibilidade de pular. | Média |
| 34 | **Sem persistência** — nenhum dado é salvo em arquivo ou banco de dados. Tudo perdido ao encerrar. | Alta |
| 35 | **Duas estruturas acumulam a mesma informação** — `qvoos`/`qpassageiros` nas structs e `quantidade_total_voos`/`quantidade_total_passageiros` globais coexistem sem sincronia. | Média |
| 36 | **Função `alterar` não valida IDs alterados** — permite alterar `identificador_voo` ou `identificador_passageiro` para valores que não existem nas listas correspondentes. | Média |

---

## Resumo por Prioridade

| Prioridade | Qtd | Itens |
|------------|-----|-------|
| **Crítica** (crash) | 2 | #19, #20 |
| **Alta** (lógica incorreta) | 8 | #17, #21, #22, #23, #24, #25, #28, #29 |
| **Média** (comportamento errado) | 7 | #11, #12, #16, #18, #26, #27, #36 |
| **Baixa** (organização/estilo) | 8 | #6, #7, #8, #9, #10, #13, #14, #15 |
| **Muito Baixa** (cosmético) | 5 | #1, #2, #3, #4, #5 |
| **Arquitetural** | 7 | #30, #31, #32, #33, #34, #35, #36 |
