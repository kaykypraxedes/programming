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

| Entity       | Main attributes                                                       |
|--------------|-----------------------------------------------------------------------|
| **Flight**   | id, aircraft_number, airline, origin, destination, departure_date, departure_time |
| **Ticket**   | number, passenger_id, flight_id, price, sale_date                     |
| **Passenger**| id, name, identity, address, phone, gender                            |

---

## Business Rules

- **Limits:** maximum of 50 flights, 100 passengers, and 100 tickets per execution
- **Unique identifiers:** flights and passengers cannot have duplicate IDs
- **Referential integrity:**
  - When a flight is removed, all associated tickets and passengers are automatically removed
  - When a passenger is removed, their tickets are automatically removed
- **Validation:** when creating a ticket, the system checks that the specified passenger and flight exist
- **Test data:** 2 flights, 3 passengers, and 3 tickets are pre-loaded at initialization

---

## Building and Testing

```bash
cd Code && make                    # compile the program
cd Code && make test               # run automated tests (12 testbenchs)
cd Code && make clean              # remove build artifacts
cd Code && ./airport_manager       # run the program
```

### Automated Tests

The `Code/testbenchs/` directory contains 12 test scripts covering:

- Initial report integrity
- Add / duplicate rejection for flights, passengers, and tickets
- Cascade deletion (flight and passenger removal)
- Ticket removal and counter consistency
- Flight data update
- Empty system state

---

## Technologies

- **Language:** C (C99 standard)
- **Libraries:** `stdio.h`, `stdlib.h`, `string.h`
- **Compiler:** GCC (or any standard C compiler)

> No external dependencies — only the standard C library is used.

---

## Implementation Choices

These are deliberate design decisions made to keep the project simple and focused:

- **Arbitrary limits** — the 50-flight, 100-passenger, and 100-ticket caps are
  not business requirements; they exist to prevent unbounded memory growth in
  this academic project.
- **Monolithic code** — the entire system lives in a single `.c` file for
  straightforward compilation with no external dependencies.
- **In-memory storage** — all data resides in linked lists and is lost when the
  program exits. No file or database persistence was implemented.

