# MIPS nRisc de 8 bits

**Autores:** Kayky Moreira Praxedes, Carlos Ernesto Cardoso dos Reis
**Data:** Março 2026

## 1. Objetivo do projeto

Construção e simulação de um processador **MIPS nRisc monociclo**, projetado integralmente em Verilog HDL, com arquitetura simplificada de 8 bits para dados, instruções e memória [01].

### Programa embarcado

Foi embarcado na memória de instruções um programa que executa a **Cifra de César** sobre uma mensagem armazenada na memória de dados (ver Apêndice C). O algoritmo:

1. Lê um caractere da memória.
2. Soma o deslocamento (chave, sendo número entre -15 e 15).
3. Ajusta o valor caso ultrapasse o intervalo alfabético.
4. Armazena o novo caractere na memória.

O limite da mensagem é de **128 caracteres**, imposto pelo espaço de endereçamento (o mesmo vale para o tamanho do programa).

## 2. Diagrama

> O diagrama de blocos original (datapath completo) está disponível no PDF do projeto.

### Caminho dos dados

Os dados seguem uma ordem fixa:

1. PC acessa memória de instruções.
2. Instrução é decodificada pela unidade de controle.
3. Registradores são lidos.
4. ULA executa operação.
5. Resultado é escrito no banco ou na memória.

## 3. Arquitetura

Principais componentes e seu funcionamento (ver Apêndice B):

### 3.1 Unidade de controle

Geração dos sinais de controle a partir do OpCode e do campo `funct` (determinam o fluxo do caminho de dados e a operação realizada em cada ciclo).

**Flags de controle (binário):**

| OpCode/funct | Instrução |
|---|---|
| `0000` | add |
| `0001` | sub |
| `001X` | addi |
| `0100` | mult |
| `0101` | null |
| `0110` | ld |
| `0111` | st |
| `1000` | jr |
| `1001` | null |
| `1010` | beq |
| `1011` | slt |
| `1100` | result |
| `1101` | null |
| `1110` | nop |
| `1111` | hlt |

**Tabela de sinais de controle por instrução:**

| Instrução | ALUSrc | MemToReg | RegWrite | MemRead | MemWrite | Branch | Jump | NextOp | End | ALUOp |
|---|---|---|---|---|---|---|---|---|---|---|
| add | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 00 |
| sub | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 00 |
| addi | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 01 |
| mult | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| null | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| ld | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 01 |
| st | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 01 |
| jr | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 01 |
| null | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 01 |
| beq | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 11 |
| slt | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 11 |
| result | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 00 |
| null | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 00 |
| nop | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 01 |
| hlt | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 01 |

**Descrição dos sinais:**

- ``ALUSrc``: indica se o segundo operando vem de um registrador (0), ou se é um imediato (1).
- ``MemToReg``: indica se o resultado a ser escrito no registrador vem da ULA (0) ou da memória (1).
- ``RegWrite``: indica se haverá escrita no registrador (1) ou não (0).
- ``MemRead``: indica se haverá leitura de memória (1) ou não (0).
- ``MemWrite``: indica se haverá escrita na memória (1) ou não (0).
- ``Branch``: indica se haverá um desvio condicional (1), ou não (0).
- ``Jump``: indica se haverá um desvio incondicional (1), ou não (0).
- ``NextOp``: ignora a linha de instrução.
- ``End``: encerra o programa.
- ``ALUOp``: 2 bits que indicam o tipo de operação a ser realizada pela ULA [02]:
  - `00`: add, sub ou result
  - `01`: addi
  - `10`: mult
  - `11`: beq ou slt

### 3.2 PC (Program Counter)

Registrador responsável por armazenar o endereço da próxima instrução.

### 3.3 Memória

A memória é dividida em duas regiões, ambas com endereços de 7 bits (128 posições) e armazenando dados de 8 bits:

- **Memória de dados**: responsável por armazenar os dados variáveis (nesse caso, a mensagem a ser codificada).
- **Memória de instruções**: responsável por armazenar o código do programa.

### 3.4 Banco de registradores

Conjunto de 4 registradores de uso geral com 8 bits cada, acessados pelas instruções por uma ordenação numérica:

- `00`: $c0
- `01`: $c1
- `10`: $c2
- `11`: $c3

Existe ainda o registrador especial **$re**, responsável por armazenar o resultado das instruções de comparação (`beq` e `slt`). Os valores assumidos podem ser 0 (comparação falsa) ou 1 (verdadeira), assumindo por padrão o valor **-4 (11111100)**, evitando desvios não intencionais.

### 3.5 ULA (Unidade Lógica e Aritmética)

Responsável pelas operações aritméticas, lógicas e de comparação [03].

O projeto não utiliza descrição comportamental (operadores aritméticos de alto nível da linguagem, como `+`, `-`, `*` ou operadores relacionais) para as operações. Em vez disso, a ULA foi construída de forma hierárquica, a partir de componentes básicos (somador de 1 bit, somador de 8 e 16 bits), explicitando o fluxo de carry e a propagação de sinais, o que permite observar diretamente a implementação física do circuito.

**Extensor de sinal**: mini módulo responsável por converter os imediatos de 3 bits das instruções para 8 bits (possibilitando as operações na ULA).

## 4. Instruções (binário e Assembly)

As instruções possuem 8 bits e são divididas em três formatos, a depender da quantidade de registradores utilizados na operação [04].

### Tipo 2R — Operações entre dois registradores

```
| OpCode (3 bits) | Reg1 (2 bits) | Reg2 (2 bits) | funct (1 bit) |
```

**Aritméticas:**
- `000 00-11 00-11 0` → `add $ci $cj` → $ci = $ci + $cj
- `000 00-11 00-11 1` → `sub $ci $cj` → $ci = $ci − $cj
- `010 00-11 00-11 0` → `mult $ci $cj` → $ci = $ci × $cj

**Memória:**
- `011 00-11 00-11 0` → `ld $ci $cj` → $ci = memória de dados[$cj]
- `011 00-11 00-11 1` → `st $ci $cj` → memória de dados[$cj] = $ci

**Comparação:**
- `101 00-11 00-11 0` → `beq $ci $cj` → $re = ($ci == $cj) ? 1 : 0
- `101 00-11 00-11 1` → `slt $ci $cj` → $re = ($ci < $cj) ? 1 : 0

### Tipo 1R — Operações com apenas um registrador

```
| OpCode (3 bits) | Reg (2 bits) | Imediato (3 bits) |
```

**Aritméticos:**
- `001 00-11 000-111` → `addi $ci imediato` → $ci = $ci + imediato

**Desvio:**
- `100 00-11 000-111` → `jr $ci` → PC = $ci
- `110 00-11 000-111` → `result $ci imediato` → PC = ($re == imediato) ? $ci : PC + 1

O imediato possui sinal e varia de -3 a 3 (`101` a `011`).

### Tipo 0R — Operações sem uso de registradores

```
| OpCode (3 bits) | don't care (4 bits) | funct (1 bit) |
```

**Controle:**
- `111 0000 0` → `nop` (não executa nenhuma ação)
- `111 0000 1` → `hlt` (encerra o programa)

## Apêndice A — Características adicionais do processador

**Objetivo do projeto:**

[01] Todas as operações são realizadas em um ciclo de clock, com a duração do ciclo sendo arbitrariamente definida em 10ns (como a simulação não tem um limite físico, qualquer valor seria aceito).

**Arquitetura:**

[02] O ALUOp `01` foi definido em muitas operações pois evita o acesso a múltiplos registradores (poderia acabar causando bugs por conta dos flags de controle).

[03] A ULA gera um sinal que indica quando ocorreu um overflow aritmético. Todavia, devido ao intuito do projeto e do programa embarcado, esse sinal não altera em nada o funcionamento do projeto.

**Instruções (binário e Assembly):**

[04] Os bits don't care recebem o valor 0 por padrão nas instruções em binário (evita conflitos nos flags de controle, acesso indevido a registradores, etc).

## Apêndice B — Resultado dos testbenches

Os testbenches foram realizados no site [edaplayground.com](https://www.edaplayground.com/) (Testbench/Design: SystemVerilog/Verilog, Compilador/Simulador: Icarus Verilog 12.0).

### Módulos individuais

#### Controle

| Op2 | Op1 | Op0 | funct | reset | ALUSrc | MemToReg | RegWrite | MemRead | MemWrite | Branch | Jump | NextOp | End |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |

> Nota: a tabela original também inclui a coluna ALUOp (2 bits) ao final de cada linha; consulte o PDF original para os valores completos por linha caso necessário para depuração detalhada.

#### PC (Program Counter)

| Time | Clock | Reset | End | endereco | enderecoSaida |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 5 | 0 |
| 5 | 1 | 1 | 0 | 5 | 0 |
| 10 | 0 | 0 | 0 | 5 | 0 |
| 15 | 1 | 0 | 0 | 5 | 5 |
| 20 | 0 | 0 | 0 | 10 | 5 |
| 25 | 1 | 0 | 0 | 10 | 10 |
| 30 | 0 | 0 | 0 | 20 | 10 |
| 35 | 1 | 0 | 0 | 20 | 20 |
| 40 | 0 | 0 | 1 | 30 | 20 |
| 45 | 1 | 0 | 1 | 30 | 20 |
| 50 | 0 | 0 | 1 | 40 | 20 |
| 55 | 1 | 0 | 1 | 40 | 20 |
| 60 | 0 | 1 | 1 | 40 | 0 |
| 65 | 1 | 1 | 1 | 40 | 0 |
| 70 | 0 | 0 | 0 | 40 | 0 |
| 75 | 1 | 0 | 0 | 40 | 40 |
| 80 | 0 | 0 | 0 | 40 | 40 |

#### Memória de dados (leitura isolada)

| Endereço | Dado lido (bin) | Caractere |
|---|---|---|
| 0 | 01001000 | H |
| 1 | 01000101 | E |
| 2 | 01001100 | L |
| 3 | 01001100 | L |
| 4 | 01001111 | O |
| 5 | 00000000 | (vazio) |
| 6 | 01010111 | W |
| 7 | 01001111 | O |
| 8 | 01010010 | R |
| 9 | 01001100 | L |
| 10 | 01000100 | D |

(Sequência repetida e estendida para verificação de múltiplas leituras, incluindo a palavra "WORLD" e endereços extras de teste, ex.: posição 20 com valores `xxxxxxxx` e `01011010` (Z) em diferentes execuções.)

#### Memória de instruções (amostra)

| Endereço | OpCode | Reg1 | Reg2 | Funct | Imediato |
|---|---|---|---|---|---|
| 0 | 000 | 10 | 10 | 1 | 101 |
| 4 | 001 | 00 | 01 | 1 | 011 |
| 10 | 011 | 01 | 10 | 0 | 100 |
| 19 | 110 | 11 | 00 | 1 | 001 |
| 54 | 001 | 00 | 01 | 1 | 011 |
| 77 | 111 | 00 | 00 | 0 | 000 |
| 81 | 100 | 00 | 00 | 0 | 000 |
| 83 | 111 | 00 | 00 | 1 | 001 |

#### Banco de registradores (amostra)

| Time | Clock | Reset | RegWrite | Reg1 | Reg2 | DadoW | Dado Reg1 | Dado Reg2 | ReIn | ReOut |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 00 | 00 | 00 | 00 | 00 | 00 | fc |
| 5 | 1 | 1 | 0 | 00 | 00 | 00 | 00 | 00 | 00 | fc |
| 10 | 0 | 0 | 1 | 00 | 00 | aa | 00 | 00 | 11 | fc |
| 15 | 1 | 0 | 1 | 00 | 00 | aa | aa | aa | 11 | 11 |
| 20 | 0 | 0 | 1 | 01 | 00 | bb | 00 | aa | 22 | 11 |
| 25 | 1 | 0 | 1 | 01 | 00 | bb | bb | aa | 22 | 22 |
| 30 | 0 | 0 | 1 | 10 | 00 | cc | 00 | aa | 33 | 22 |
| 35 | 1 | 0 | 1 | 10 | 00 | cc | cc | aa | 33 | 33 |
| 40 | 0 | 0 | 1 | 11 | 00 | dd | 00 | aa | 44 | 33 |
| 45 | 1 | 0 | 1 | 11 | 00 | dd | dd | aa | 44 | 44 |
| 50 | 0 | 0 | 0 | 00 | 01 | dd | aa | bb | 55 | 44 |
| 55 | 1 | 0 | 0 | 00 | 01 | dd | aa | bb | 55 | 55 |
| 60 | 0 | 0 | 0 | 10 | 11 | dd | cc | dd | 55 | 55 |
| 65 | 1 | 0 | 0 | 10 | 11 | dd | cc | dd | 55 | 55 |
| 70 | 0 | 0 | 0 | 00 | 00 | ff | aa | aa | 66 | 55 |
| 75 | 1 | 0 | 0 | 00 | 00 | ff | aa | aa | 66 | 66 |
| 80 | 0 | 0 | 0 | 00 | 00 | ff | aa | aa | 66 | 66 |
| 85 | 1 | 0 | 0 | 00 | 00 | ff | aa | aa | 66 | 66 |
| 90 | 0 | 0 | 1 | 00 | 00 | ff | aa | aa | 66 | 66 |
| 95 | 1 | 0 | 1 | 00 | 00 | ff | ff | ff | 66 | 66 |
| 100 | 0 | 0 | 1 | 00 | 00 | ff | ff | ff | 77 | 66 |
| 105 | 1 | 0 | 1 | 00 | 00 | ff | ff | ff | 77 | 77 |
| 110 | 0 | 0 | 1 | 00 | 00 | ff | ff | ff | 88 | 77 |
| 115 | 1 | 0 | 1 | 00 | 00 | ff | ff | ff | 88 | 88 |
| 120 | 0 | 1 | 1 | 00 | 00 | ff | 00 | 00 | 88 | fc |
| 125 | 1 | 1 | 1 | 00 | 00 | ff | 00 | 00 | 88 | fc |
| 130 | 0 | 0 | 1 | 00 | 00 | ff | 00 | 00 | 88 | fc |
| 135 | 1 | 0 | 1 | 00 | 00 | ff | ff | ff | 88 | 88 |
| 140 | 0 | 0 | 1 | 00 | 00 | ff | ff | ff | 88 | 88 |

#### ULA

| A | B | S | overflow | reEntrada | reSaida | zero |
|---|---|---|---|---|---|---|
| 10 | 20 | 30 | 0 | aa | aa | 0 |
| 255 | 1 | 0 | 1 | 55 | 55 | 0 |
| 30 | 15 | 15 | 1 | bb | bb | 0 |
| 50 | 25 | 75 | 0 | ee | ee | 0 |
| 10 | 5 | 50 | 0 | ff | ff | 0 |
| 128 | 2 | 0 | 1 | 66 | 66 | 0 |
| 40 | 40 | 0 | 1 | 11 | 01 | 0 |
| 40 | 41 | 0 | 0 | 22 | 00 | 0 |
| 10 | 20 | 0 | 0 | 33 | 01 | 0 |
| 30 | 20 | 0 | 1 | 44 | 00 | 0 |
| 25 | 204 | 0 | 1 | cc | fc | 1 |
| 30 | 25 | 0 | 0 | dd | fc | 0 |

### Processador completo com programa embarcado

#### Exemplo: mensagem "HELLO", cifra 5

**Memória de dados antes [0:6]:**

| Endereço | Valor | Decimal | Caractere |
|---|---|---|---|
| 0 | 01001000 | 72 | H |
| 1 | 01000101 | 69 | E |
| 2 | 01001100 | 76 | L |
| 3 | 01001100 | 76 | L |
| 4 | 01001111 | 79 | O |
| 5 | 00000000 | 0 | (vazio) |
| 6 | xxxxxxxx | x | — |

**Memória de dados depois (resultado da cifra):**

| Endereço | Valor | Decimal | Caractere |
|---|---|---|---|
| 0 | 01001101 | 77 | M |
| 1 | 01001010 | 74 | J |
| 2 | 01010001 | 81 | Q |
| 3 | 01010001 | 81 | Q |
| 4 | 01010100 | 84 | T |
| 5 | 00000000 | 0 | (vazio) |
| 6 | xxxxxxxx | x | — |

> O trace completo de execução ciclo a ciclo (registrador `$c0`–`$c3`, `$re`, PC e instrução decodificada) está documentado no PDF original.

#### Outros testes de cifra

**Mensagem "BATATA", cifra 15:**

| Endereço | Original | Cifrado |
|---|---|---|
| 0 | B (66) | Q (81) |
| 1 | A (65) | P (80) |
| 2 | T (84) | I (73) |
| 3 | A (65) | P (80) |
| 4 | T (84) | I (73) |
| 5 | A (65) | P (80) |
| 6 | (fim, 0) | (fim, 0) |

**Mensagem "GALOFRITO", cifra -15:**

| Endereço | Original | Cifrado |
|---|---|---|
| 0 | G (71) | R (82) |
| 1 | A (65) | L (76) |
| 2 | L (76) | W (87) |
| 3 | O (79) | Z (90) |
| 4 | F (70) | Q (81) |
| 5 | R (82) | C (67) |
| 6 | I (73) | T (84) |
| 7 | T (84) | E (69) |
| 8 | O (79) | Z (90) |
| 9 | (fim, 0) | (fim, 0) |

**Mensagem "GALO FRITO" (com espaço), cifra -15** — demonstra que o algoritmo trata corretamente um caractere após o espaço (EOF lógico só ocorre no byte `0x00` real, não em espaços intermediários):

| Endereço | Original | Cifrado |
|---|---|---|
| 0 | G (71) | R (82) |
| 1 | A (65) | L (76) |
| 2 | L (76) | W (87) |
| 3 | O (79) | Z (90) |
| 4 | (espaço, 0) | (espaço, 0) |
| 5 | F (70) | F (70) |
| 6 | R (82) | R (82) |
| 7 | I (73) | I (73) |
| 8 | T (84) | T (84) |
| 9 | O (79) | O (79) |
| 10 | (fim, 0) | (fim, 0) |

> Observação: nesse caso de teste com espaço em posição intermediária (valor 0x00, que é o mesmo código usado como marcador de fim de mensagem), a memória de dados é tratada como `(0, 11)` no testbench resumido — ou seja, o `0` interno funciona como terminador, então apenas "GALO" é processado antes de a simulação ser encerrada nesse trecho de teste.

## Apêndice C — Programa embarcado (binário e Assembly)

> Para tornar o código programável, sem que a mudança de cifra alterasse a quantidade de linhas (já que as somas com imediato só podem ser feitas de 3 em 3 e os jumps são para uma linha específica), faz-se uma soma de 5 linhas sempre (que vai de -15 até 15, cobrindo todo o range).

```assembly
0-  00010101  // sub $c2, $c2      (zera os registradores)
1-  00000001  // sub $c0, $c0
2-  00011111  // sub $c3, $c3
3-  11100000  // nop
4-  00100011  // addi $c0, 3        (incrementa o valor da cifra)
5-  00100010  // addi $c0, 2        (como o resto é 0, a cifra é 5)
6-  00100000  // addi $c0, 0
7-  00100000  // addi $c0, 0
8-  00100000  // addi $c0, 0
9-  11100000  // nop
10- 01101100  // ld $c1, $c2        (recebe o valor armazenado na posição indicada por $c2 e copia em $c1)
11- 00001000  // add $c1, $c0       (adiciona a cifra ao valor)
12- 10101000  // beq $c1, $c0       (testa se chegou ao EOF (0))
13- 00000001  // sub $c0, $c0
14- 11100000  // nop
15- 00111011  // addi $c3, 3
16- 01011110  // mult $c3, $c3
17- 01011110  // mult $c3, $c3
18- 00111001  // addi $c3, 1        ($c3 == 82)
19- 11011001  // result $c3, 1      (se chegou ao EOF, vai para o fim do código)
20- 00000001  // sub $c0, $c0
21- 00011111  // sub $c3, $c3
22- 11100000  // nop
23- 00100011  // addi $c0, 3
24- 00100011  // addi $c0, 3
25- 00100011  // addi $c0, 3
26- 00100001  // addi $c0, 1
27- 00111011  // addi $c3, 3
28- 00111011  // addi $c3, 3
29- 00111011  // addi $c3, 3
30- 01000110  // mult $c0, $c3
31- 00100001  // addi $c0, 1        ($c0 == 91)
32- 00011111  // sub $c3, $c3
33- 10101001  // slt $c1, $c0       (verifica se $c1 < 91 ('Z') ? $re = 1 : $re = 0)
34- 00000001  // sub $c0, $c0
35- 00011111  // sub $c3, $c3
36- 00111011  // addi $c3, 3
37- 00000110  // add $c0, $c3
38- 01011000  // mult $c3, $c0
39- 01011000  // mult $c3, $c0
40- 00011110  // add $c3, $c3
41- 00111101  // addi $c3, -3       ($c3 == 51)
42- 11011001  // result $c3, 1      (se a letra está no range, pula a operação de correção)
43- 00011111  // sub $c3, $c3
44- 00000001  // sub $c0, $c0
45- 00100011  // addi $c0, 3
46- 00111011  // addi $c3, 3
47- 01000110  // mult $c0, $c3
48- 01000110  // mult $c0, $c3
49- 00100111  // addi $c0, -1       ($c0 == 26)
50- 00001001  // sub $c1, $c0       (o valor é decrementado para caber no range)
51- 11100000  // nop
52- 00000001  // sub $c0, $c0
53- 00011111  // sub $c3, $c3
54- 00100011  // addi $c0, 3
55- 00100001  // addi $c0, 1
56- 00011000  // add $c3, $c0
57- 01000110  // mult $c0, $c3
58- 01000110  // mult $c0, $c3
59- 00100001  // addi $c0, 1        ($c0 == 65)
60- 00011111  // sub $c3, $c3
61- 10101001  // slt $c1, $c0       (verifica se $c1 < 65 ('A') ? $re = 1 : $re = 0)
62- 00000001  // sub $c0, $c0
63- 00111011  // addi $c3, 3
64- 01011110  // mult $c3, $c3
65- 01011110  // mult $c3, $c3
66- 00111101  // addi $c3, -3       ($c3 == 78)
67- 11011000  // result $c3, 0      (se a letra está no range, pula a operação de correção)
68- 00011111  // sub $c3, $c3
69- 00000001  // sub $c0, $c0
70- 00100011  // addi $c0, 3
71- 00111011  // addi $c3, 3
72- 01000110  // mult $c0, $c3
73- 01000110  // mult $c0, $c3
74- 00100111  // addi $c0, -1       ($c0 == 26)
75- 00001000  // add $c1, $c0       (o valor é incrementado para caber no range)
76- 00000001  // sub $c0, $c0
77- 11100000  // nop
78- 01101101  // st $c1, $c2        (armazena o valor de $c1 no endereço indicado por $c2)
79- 00110001  // addi $c2, 1        (passa para o próximo caractere)
80- 00100001  // addi $c0, 1
81- 10000000  // jr $c0             (volta para o início do código)
82- 11100000  // nop
83- 11100001  // hlt                (encerra o programa)
```
