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

| Entidade      | Atributos principais                                  |
|---------------|-------------------------------------------------------|
| **Voo**       | identificador, numero_aeronave, empresa, origem, destino, data/horario_partida |
| **Passagem**  | numero, id_passageiro, id_voo, valor, data_venda      |
| **Passageiro**| identificador, nome, identidade, endereco, telefone, sexo |

---

## Regras de Negócio

- **Limites:** máximo de 50 voos e 100 passageiros por execução
- **Identificadores únicos:** voos e passageiros não podem ter IDs duplicados
- **Integridade referencial:**
  - Ao remover um voo, todas as passagens e passageiros associados são removidos automaticamente
  - Ao remover um passageiro, suas passagens são removidas automaticamente
- **Validação:** ao criar uma passagem, o sistema verifica se o passageiro e o voo informados existem
- **Dados de teste:** 2 voos, 3 passageiros e 3 passagens são pré-carregados na inicialização

---

## Tecnologias

- **Linguagem:** C (padrão C99)
- **Bibliotecas:** `stdio.h`, `stdlib.h`, `string.h`
- **Compilador:** GCC (ou qualquer compilador C padrão)

> Não há dependências externas — apenas a biblioteca padrão C é utilizada.

---

## Limitações Conhecidas

- **Sem persistência de dados** — todas as informações são perdidas ao encerrar o programa
- **Código monolítico** — todo o sistema está em um único arquivo `.c`
- **Validação de entrada frágil** — uso de `scanf` sem tratamento de entradas inválidas
- **Vazamentos de memória** — nem toda memória alocada é liberada adequadamente
- **Contagem de limites inconsistente** — os campos `qvoos` e `qpassageiros` apresentam falhas de atualização
- **Bug conhecido:** verificação do limite de passagens na função `adicionar` percorre a lista até o final e tenta acessar um nó nulo

---

## Melhorias Futuras Possíveis

- [ ] Persistência em arquivo (binário ou texto)
- [ ] Modularização do código em múltiplos arquivos (.h / .c)
- [ ] Interface gráfica ou versão web
- [ ] Validação robusta de entrada do usuário
- [ ] Correção de vazamentos de memória
- [ ] Testes automatizados
- [ ] Suporte a cadastro de aeronaves e empresas
