# Sistema de Gerenciamento de Aeroporto

Sistema CRUD em **C** para gerenciamento de voos, passagens e passageiros em aeroportos, com dados armazenados em memória via listas encadeadas.

**Desenvolvedores:** Kayky Moreira Praxedes, Carlos Ernesto Cardoso dos Reis

---

## Funcionalidades

### Menu Principal
1. **Voos** — Gerenciar voos
2. **Passagens** — Gerenciar passagens
3. **Passageiros** — Gerenciar passageiros
4. **Relatórios** — Exibir relatórios gerenciais
5. **Sair**

### Submenu (CRUD)
Cada módulo oferece: **Adicionar**, **Alterar**, **Excluir**, **Consultar**, **Sair**.

### Relatórios
- Quantidade de passagens por voo
- Quantidade de voos por empresa
- Lista de passageiros por voo

---

## Estruturas de Dados

O sistema utiliza **listas encadeadas simples** com alocação dinâmica para três entidades:

| Entidade      | Atributos principais (nomes em inglês no código)                        |
|---------------|-------------------------------------------------------------------------|
| **Voo**       | id, aircraft_number, airline, origin, destination, departure_date, departure_time |
| **Passagem**  | number, passenger_id, flight_id, price, sale_date                       |
| **Passageiro**| id, name, identity, address, phone, gender                              |

---

## Regras de Negócio

- **Limites:** máximo de 50 voos, 100 passageiros e 100 passagens por execução
- **Identificadores únicos:** voos e passageiros não podem ter IDs duplicados
- **Integridade referencial:**
  - Ao remover um voo, todas as passagens e passageiros associados são removidos automaticamente
  - Ao remover um passageiro, suas passagens são removidas automaticamente
- **Validação:** ao criar uma passagem, o sistema verifica se o passageiro e o voo informados existem
- **Dados de teste:** 2 voos, 3 passageiros e 3 passagens são pré-carregados na inicialização

---

## Compilação e Testes

```bash
cd Code && make                    # compilar o programa
cd Code && make test               # executar testes automatizados (12 testbenchs)
cd Code && make clean              # remover artefatos de compilação
cd Code && ./airport_manager       # executar o programa
```

### Testes Automatizados

O diretório `Code/testbenchs/` contém 12 scripts de teste cobrindo:

- Integridade do relatório inicial
- Adição e rejeição de duplicatas para voos, passageiros e passagens
- Remoção em cascata (voo e passageiro)
- Remoção de passagem e consistência dos contadores
- Alteração de dados de voo
- Estado do sistema vazio

---

## Tecnologias

- **Linguagem:** C (padrão C99)
- **Bibliotecas:** `stdio.h`, `stdlib.h`, `string.h`
- **Compilador:** GCC (ou qualquer compilador C padrão)

> Não há dependências externas — apenas a biblioteca padrão C é utilizada.

---

## Escolhas de Implementação

Estas são decisões deliberadas de projeto para manter o código simples e focado:

- **Limites arbitrários** — os tetos de 50 voos, 100 passageiros e 100 passagens
  não são requisitos de negócio; existem para evitar crescimento ilimitado de
  memória neste projeto acadêmico.
- **Código monolítico** — todo o sistema está em um único arquivo `.c` por
  escolha, para compilação simples sem dependências externas.
- **Armazenamento em memória** — todos os dados estão em listas encadeadas e
  são perdidos ao encerrar o programa. Nenhuma persistência em arquivo ou banco
  de dados foi implementada.
