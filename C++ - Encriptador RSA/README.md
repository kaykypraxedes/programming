# Encriptador RSA

Implementação educacional do algoritmo RSA em C++, com utilitários para geração de números primos e fatoração.

## Funcionalidades

- **Fatoração de números** — Decompõe um valor em seus fatores primos, exibindo o tempo de processamento e a quantidade de primos calculados.
- **Cálculo do menor primo com n dígitos** — Encontra o menor número primo com uma quantidade específica de dígitos usando a Conjectura de Legendre.
- **Criptografia/Descriptografia RSA** — Geração de chaves (pública e privada), codificação e decodificação de mensagens.

## Estrutura do Projeto

```
Código/
├── main.cpp           # Interface principal (menu interativo)
├── cripto.cpp/.h      # Implementação do RSA
├── fatora.cpp/.h      # Decomposição em fatores primos
├── primos.cpp/.h      # Geração de primos (Crivo de Eratóstenes)
└── tempo.cpp/.h       # Formatação de tempo (us → ms → s → min)
```

## Módulos

### primos

Gera números primos até um limite utilizando o **Crivo de Eratóstenes**. A função `calculaPrimos()` constrói o crivo até `sqrt(n) + 1` e armazena os primos em um vetor. `primoMin()` usa a Conjectura de Legendre para encontrar o menor primo acima de `10^(n-1)`.

### fatora

Recebe um vetor de primos do módulo `primos` e realiza divisões sucessivas para obter a decomposição em fatores primos. Retorna uma string formatada (ex: `"84 = 2² * 3 * 7"`).

### cripto

Implementa o RSA com as seguintes operações:

- **Multiplicação modular** (`modMul`) — Evita overflow de `unsigned long long` com subtrações condicionais.
- **Exponenciação modular** (`modPow`) — Algoritmo binário para `b^e mod n`.
- **Inverso modular** (`modInverse`) — Algoritmo estendido de Euclides.
- **Codificação** — Converte a mensagem para números ASCII, divide em blocos menores que `n` e aplica `C(b) = b^e mod n`.
- **Decodificação** — Recebe os blocos codificados, aplica `D(a) = a^d mod n` e reconverte para texto.

### tempo

Converte microssegundos para milissegundos, segundos ou minutos + segundos para exibição amigável.

## Observação sobre Segurança

O Crivo de Eratóstenes implementado neste projeto só é capaz de fatorar números cujo maior fator primo esteja dentro do limite viável de memória (~4 GB para `sqrt(2^64)`, ou 2³² bits). Para um número RSA real (tipicamente 2048 bits ou mais), a raiz quadrada já teria 1024 bits — inviabilizando completamente o crivo. Este projeto ilustra justamente que algoritmos ingênuos, mesmo otimizados, não conseguem quebrar o RSA na prática, servindo apenas como demonstração educacional do funcionamento matemático do algoritmo.
