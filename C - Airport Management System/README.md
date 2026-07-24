# Airport Management System

CRUD system in **C** for managing flights, tickets, and passengers at airports, with data stored in memory via linked lists.

**Developers:** Kayky Moreira Praxedes, Carlos Ernesto Cardoso dos Reis

---

## Features

### Main Menu
1. **Voos** — Manage flights
2. **Passagens** — Manage tickets
3. **Passageiros** — Manage passengers
4. **Relatórios** — Display management reports
5. **Sair**

### Submenu (CRUD)
Each module offers: **Adicionar** (Add), **Alterar** (Edit), **Excluir** (Delete), **Consultar** (Search), **Sair** (Exit).

### Reports
- Number of tickets per flight
- Number of flights per airline
- List of passengers per flight

---

## Data Structures

The system uses **singly linked lists** with dynamic allocation for three entities:

| Entity         | Main attributes                                          |
|----------------|----------------------------------------------------------|
| **Voo**        | id, aircraft_number, airline, origin, destination, departure_date/time |
| **Passagem**   | number, passenger_id, flight_id, value, sale_date        |
| **Passageiro** | id, name, identity, address, phone, gender               |

---

## Business Rules

- **Limits:** maximum of 50 flights and 100 passengers per execution
- **Unique identifiers:** flights and passengers cannot have duplicate IDs
- **Referential integrity:**
  - When a flight is removed, all associated tickets and passengers are automatically removed
  - When a passenger is removed, their tickets are automatically removed
- **Validation:** when creating a ticket, the system checks that the specified passenger and flight exist
- **Test data:** 2 flights, 3 passengers, and 3 tickets are pre-loaded at initialization

---

## Technologies

- **Language:** C (C99 standard)
- **Libraries:** `stdio.h`, `stdlib.h`, `string.h`
- **Compiler:** GCC (or any standard C compiler)

> No external dependencies — only the standard C library is used.

---

## Known Limitations

- **No data persistence** — all information is lost when the program ends
- **Monolithic code** — the entire system is in a single `.c` file
- **Fragile input validation** — uses `scanf` without handling invalid inputs
- **Memory leaks** — not all allocated memory is properly freed
- **Inconsistent limit counting** — the `qvoos` and `qpassageiros` fields have update flaws
- **Known bug:** ticket limit check in the `adicionar` function traverses the list to the end and tries to access a null node

---

## Possible Future Improvements

- [ ] File persistence (binary or text)
- [ ] Code modularization into multiple files (.h / .c)
- [ ] Graphical interface or web version
- [ ] Robust user input validation
- [ ] Fix memory leaks
- [ ] Automated tests
- [ ] Support for aircraft and airline registration
