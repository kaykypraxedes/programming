/* airport_manager.c */
/*
Desenvolvedores:
    Kayky Moreira Praxedes
    Carlos Ernesto Cardoso dos Reis
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Constantes para limites do sistema:
 * MAX_FLIGHTS    – número máximo de voos suportados
 * MAX_PASSENGERS – número máximo de passageiros suportados
 * MAX_TICKETS    – número máximo de passagens suportadas
 */
#define MAX_FLIGHTS    50
#define MAX_PASSENGERS 100
#define MAX_TICKETS    100

/* === Estruturas de Dados === */

typedef struct flight {
    int id;
    int aircraft_number;
    char airline[20];
    char origin[50];
    char destination[50];
    char departure_date[15];
    char departure_time[10];
    struct flight *next;
} FLIGHT;

typedef FLIGHT *FLIGHT_PTR;

typedef struct ticket {
    int number;
    int passenger_id;
    int flight_id;
    double price;
    char sale_date[15];
    struct ticket *next;
} TICKET;

typedef TICKET *TICKET_PTR;

typedef struct passenger {
    int id;
    char name[30];
    char identity[20];
    char address[50];
    char phone[20];
    char gender;
    struct passenger *next;
} PASSENGER;

typedef PASSENGER *PASSENGER_PTR;

/* === Protótipos === */

int MainMenu(void);
int SubMenu(void);

int total_flights = 0;
int total_passengers = 0;
int total_tickets = 0;

void ExecuteAction(FLIGHT_PTR *, TICKET_PTR *, PASSENGER_PTR *, int, int);
void Add(FLIGHT_PTR *, TICKET_PTR *, PASSENGER_PTR *, int);
void Update(FLIGHT_PTR *, TICKET_PTR *, PASSENGER_PTR *, int);
void View(const FLIGHT_PTR *, const TICKET_PTR *, const PASSENGER_PTR *, int);
void Delete(FLIGHT_PTR *, TICKET_PTR *, PASSENGER_PTR *, int);
void Report(FLIGHT_PTR, PASSENGER_PTR, TICKET_PTR);

/* === Função Principal === */

int main(void) {
    FLIGHT_PTR flight = NULL;
    TICKET_PTR ticket = NULL;
    PASSENGER_PTR passenger = NULL;

    /* --- Dados de teste --- */

    /* Voo 1 */
    FLIGHT *flight1 = malloc(sizeof(FLIGHT));
    flight1->id = 1;
    flight1->aircraft_number = 101;
    snprintf(flight1->airline, sizeof(flight1->airline), "EmpresaX");
    snprintf(flight1->departure_date, sizeof(flight1->departure_date), "01/10/2024");
    snprintf(flight1->departure_time, sizeof(flight1->departure_time), "10:00");
    snprintf(flight1->origin, sizeof(flight1->origin), "Sao Paulo");
    snprintf(flight1->destination, sizeof(flight1->destination), "Rio de Janeiro");
    flight1->next = NULL;
    flight = flight1;

    /* Voo 2 */
    FLIGHT *flight2 = malloc(sizeof(FLIGHT));
    flight2->id = 2;
    flight2->aircraft_number = 911;
    snprintf(flight2->airline, sizeof(flight2->airline), "EmpresaY");
    snprintf(flight2->departure_date, sizeof(flight2->departure_date), "10/12/2024");
    snprintf(flight2->departure_time, sizeof(flight2->departure_time), "15:00");
    snprintf(flight2->origin, sizeof(flight2->origin), "Belo Horizonte");
    snprintf(flight2->destination, sizeof(flight2->destination), "Roraima");
    flight2->next = NULL;
    flight1->next = flight2;
    total_flights = 2;

    /* Passageiro 1 */
    PASSENGER *passenger1 = malloc(sizeof(PASSENGER));
    passenger1->id = 1;
    snprintf(passenger1->name, sizeof(passenger1->name), "Joao Silva");
    snprintf(passenger1->identity, sizeof(passenger1->identity), "123456789");
    snprintf(passenger1->address, sizeof(passenger1->address), "Rua A, 123");
    snprintf(passenger1->phone, sizeof(passenger1->phone), "(11) 98765-4321");
    passenger1->gender = 'M';
    passenger1->next = NULL;
    passenger = passenger1;
    total_passengers++;

    /* Passageiro 2 */
    PASSENGER *passenger2 = malloc(sizeof(PASSENGER));
    passenger2->id = 2;
    snprintf(passenger2->name, sizeof(passenger2->name), "Maria Oliveira");
    snprintf(passenger2->identity, sizeof(passenger2->identity), "987654321");
    snprintf(passenger2->address, sizeof(passenger2->address), "Rua B, 456");
    snprintf(passenger2->phone, sizeof(passenger2->phone), "(21) 91234-5678");
    passenger2->gender = 'F';
    passenger2->next = NULL;
    passenger1->next = passenger2;
    total_passengers++;

    /* Passageiro 3 */
    PASSENGER *passenger3 = malloc(sizeof(PASSENGER));
    passenger3->id = 3;
    snprintf(passenger3->name, sizeof(passenger3->name), "Kayky Praxedes");
    snprintf(passenger3->identity, sizeof(passenger3->identity), "11122233344");
    snprintf(passenger3->address, sizeof(passenger3->address), "Rua dos Bobos, 456");
    snprintf(passenger3->phone, sizeof(passenger3->phone), "(11) 91255-5678");
    passenger3->gender = 'M';
    passenger3->next = NULL;
    passenger2->next = passenger3;
    total_passengers++;

    /* Passagem 1 */
    TICKET *ticket1 = malloc(sizeof(TICKET));
    ticket1->number = 1;
    ticket1->passenger_id = 1;
    ticket1->flight_id = 1;
    ticket1->price = 500.00;
    snprintf(ticket1->sale_date, sizeof(ticket1->sale_date), "01/09/2024");
    ticket1->next = NULL;
    ticket = ticket1;
    total_tickets++;

    /* Passagem 2 */
    TICKET *ticket2 = malloc(sizeof(TICKET));
    ticket2->number = 2;
    ticket2->passenger_id = 2;
    ticket2->flight_id = 1;
    ticket2->price = 550.00;
    snprintf(ticket2->sale_date, sizeof(ticket2->sale_date), "02/09/2024");
    ticket2->next = NULL;
    ticket1->next = ticket2;
    total_tickets++;

    /* Passagem 3 */
    TICKET *ticket3 = malloc(sizeof(TICKET));
    ticket3->number = 3;
    ticket3->passenger_id = 3;
    ticket3->flight_id = 2;
    ticket3->price = 230.00;
    snprintf(ticket3->sale_date, sizeof(ticket3->sale_date), "05/12/2024");
    ticket3->next = NULL;
    ticket2->next = ticket3;
    total_tickets++;

    /* Loop principal do programa */
    int choice;
    while ((choice = MainMenu()) != 5) {
        int inner_choice;
        switch (choice) {
        case 1:
            puts("Voos");
            inner_choice = SubMenu();
            ExecuteAction(&flight, &ticket, &passenger, choice, inner_choice);
            break;
        case 2:
            puts("Passagens");
            inner_choice = SubMenu();
            ExecuteAction(&flight, &ticket, &passenger, choice, inner_choice);
            break;
        case 3:
            puts("Passageiros");
            inner_choice = SubMenu();
            ExecuteAction(&flight, &ticket, &passenger, choice, inner_choice);
            break;
        case 4:
            Report(flight, passenger, ticket);
            break;
        default:
            puts("Opcao Invalida");
            break;
        }
    }

    /* Libera a memória alocada antes de encerrar */
    {
        FLIGHT_PTR f = flight;
        while (f != NULL) {
            FLIGHT_PTR next = f->next;
            free(f);
            f = next;
        }
    }
    {
        TICKET_PTR t = ticket;
        while (t != NULL) {
            TICKET_PTR next = t->next;
            free(t);
            t = next;
        }
    }
    {
        PASSENGER_PTR p = passenger;
        while (p != NULL) {
            PASSENGER_PTR next = p->next;
            free(p);
            p = next;
        }
    }

    return 0;
}

/* === Menu Principal === */

int MainMenu(void) {
    int option;
    printf("1 - Voos\n"
           "2 - Passagens\n"
           "3 - Passageiros\n"
           "4 - Relatorios\n"
           "5 - Sair\n? ");
    scanf(" %d", &option);
    return option;
}

/* === Submenu CRUD === */

int SubMenu(void) {
    int option;
    printf("1 - Adicionar\n"
           "2 - Alterar\n"
           "3 - Excluir\n"
           "4 - Consultar\n"
           "5 - Sair\n? ");
    scanf(" %d", &option);
    return option;
}

/* === Roteador de Ações === */

void ExecuteAction(FLIGHT_PTR *flight_ptr, TICKET_PTR *ticket_ptr,
                   PASSENGER_PTR *passenger_ptr, int choice, int inner_choice) {
    switch (inner_choice) {
    case 1:
        Add(flight_ptr, ticket_ptr, passenger_ptr, choice);
        break;
    case 2:
        Update(flight_ptr, ticket_ptr, passenger_ptr, choice);
        break;
    case 3:
        Delete(flight_ptr, ticket_ptr, passenger_ptr, choice);
        break;
    case 4:
        View(flight_ptr, ticket_ptr, passenger_ptr, choice);
        break;
    case 5:
        break;
    default:
        puts("Opcao Invalida");
        break;
    }
}

/* === Adicionar === */

void Add(FLIGHT_PTR *flight_ptr, TICKET_PTR *ticket_ptr,
         PASSENGER_PTR *passenger_ptr, int choice) {
    switch (choice) {
    case 1: {
        /* Adicionar voo */
        if (total_flights >= MAX_FLIGHTS) {
            puts("Limite maximo de 50 voos ja foi excedido");
            return;
        }
        puts("Adicionando Voos:");

        FLIGHT_PTR new_node = malloc(sizeof(FLIGHT));
        if (new_node == NULL) {
            puts("Erro de alocacao de memoria");
            return;
        }

        printf("Identificador\n? ");
        scanf(" %d", &new_node->id);

        /* Verifica se o identificador já existe na lista */
        FLIGHT_PTR current_ptr = *flight_ptr;
        while (current_ptr != NULL) {
            if (current_ptr->id == new_node->id) {
                puts("Esse identificador ja foi cadastrado\n");
                free(new_node);
                return;
            }
            current_ptr = current_ptr->next;
        }

        printf("Numero da Aeronave\n? ");
        scanf(" %d", &new_node->aircraft_number);
        printf("Empresa\n? ");
        scanf(" %19[^\n]", new_node->airline);
        printf("Data da partida \"00/00/0000\"\n? ");
        scanf(" %14[^\n]", new_node->departure_date);
        printf("Horario da partida \"00:00\"\n? ");
        scanf(" %9[^\n]", new_node->departure_time);
        printf("Origem\n? ");
        scanf(" %49[^\n]", new_node->origin);
        printf("Destino\n? ");
        scanf(" %49[^\n]", new_node->destination);
        new_node->next = NULL;

        /* Insere no final da lista */
        if (*flight_ptr == NULL) {
            *flight_ptr = new_node;
        } else {
            current_ptr = *flight_ptr;
            while (current_ptr->next != NULL) {
                current_ptr = current_ptr->next;
            }
            current_ptr->next = new_node;
        }
        total_flights++;
        break;
    }
    case 2: {
        /* Adicionar passagem */
        if (*flight_ptr == NULL || *passenger_ptr == NULL) {
            puts("Sem passageiros ou voos para passagens\n");
            return;
        }
        if (total_tickets >= MAX_TICKETS) {
            puts("Limite maximo de 100 passagens ja foi excedido");
            return;
        }
        puts("Adicionando Passagens:");

        TICKET_PTR new_node = malloc(sizeof(TICKET));
        if (new_node == NULL) {
            puts("Erro de alocacao de memoria");
            return;
        }

        printf("Identificador Passageiro\n? ");
        scanf(" %d", &new_node->passenger_id);

        /* Verifica se o passageiro existe */
        PASSENGER_PTR temp_passenger = *passenger_ptr;
        while (temp_passenger != NULL && new_node->passenger_id != temp_passenger->id) {
            temp_passenger = temp_passenger->next;
        }
        if (temp_passenger == NULL) {
            puts("Esse identificador nao existe\n");
            free(new_node);
            return;
        }

        printf("Identificador Voo\n? ");
        scanf(" %d", &new_node->flight_id);

        /* Verifica se o voo existe */
        FLIGHT_PTR temp_flight = *flight_ptr;
        while (temp_flight != NULL && new_node->flight_id != temp_flight->id) {
            temp_flight = temp_flight->next;
        }
        if (temp_flight == NULL) {
            puts("Esse identificador nao existe\n");
            free(new_node);
            return;
        }

        printf("Valor\n? ");
        scanf(" %lf", &new_node->price);
        printf("Data da Venda \"00/00/0000\"\n? ");
        scanf(" %14[^\n]", new_node->sale_date);
        new_node->next = NULL;

        /* Insere no final e atribui número sequencial (máximo atual + 1) */
        if (*ticket_ptr == NULL) {
            *ticket_ptr = new_node;
            new_node->number = 1;
        } else {
            /* Encontra o maior número existente */
            int max_number = 0;
            TICKET_PTR current = *ticket_ptr;
            while (current != NULL) {
                if (current->number > max_number) {
                    max_number = current->number;
                }
                current = current->next;
            }
            /* Encontra o último nó para encadear */
            current = *ticket_ptr;
            while (current->next != NULL) {
                current = current->next;
            }
            current->next = new_node;
            new_node->number = max_number + 1;
        }
        total_tickets++;
        break;
    }
    case 3: {
        /* Adicionar passageiro */
        if (total_passengers >= MAX_PASSENGERS) {
            puts("Limite maximo de 100 passageiros ja foi excedido");
            return;
        }
        puts("Adicionando Passageiros:");

        PASSENGER_PTR new_node = malloc(sizeof(PASSENGER));
        if (new_node == NULL) {
            puts("Erro de alocacao de memoria");
            return;
        }

        printf("Identificador\n? ");
        scanf(" %d", &new_node->id);

        /* Verifica se o identificador já existe */
        PASSENGER_PTR current_ptr = *passenger_ptr;
        while (current_ptr != NULL && current_ptr->id != new_node->id) {
            current_ptr = current_ptr->next;
        }
        if (current_ptr != NULL) {
            puts("Esse identificador ja foi cadastrado\n");
            free(new_node);
            return;
        }

        printf("Nome\n? ");
        scanf(" %29[^\n]", new_node->name);
        printf("Identidade\n? ");
        scanf(" %19[^\n]", new_node->identity);
        printf("Endereco\n? ");
        scanf(" %49[^\n]", new_node->address);
        printf("Telefone \"(00)0 0000-0000\"\n? ");
        scanf(" %19[^\n]", new_node->phone);
        printf("Sexo\"H\", \"M\"\n? ");
        scanf(" %c", &new_node->gender);
        new_node->next = NULL;

        /* Insere no final da lista */
        if (*passenger_ptr == NULL) {
            *passenger_ptr = new_node;
        } else {
            current_ptr = *passenger_ptr;
            while (current_ptr->next != NULL) {
                current_ptr = current_ptr->next;
            }
            current_ptr->next = new_node;
        }
        total_passengers++;
        break;
    }
    }
}

/* === Alterar === */

void Update(FLIGHT_PTR *flight_ptr, TICKET_PTR *ticket_ptr,
            PASSENGER_PTR *passenger_ptr, int choice) {
    switch (choice) {
    case 1: {
        /* Alterar voo */
        if (*flight_ptr == NULL) {
            puts("Nao existem voos no sistema");
            return;
        }
        puts("Alterando Voos:");
        int id;
        printf("Digite o identificador do voo a ser alterado\n? ");
        scanf(" %d", &id);

        FLIGHT_PTR current_ptr = *flight_ptr;
        while (current_ptr != NULL && current_ptr->id != id) {
            current_ptr = current_ptr->next;
        }

        if (current_ptr == NULL) {
            puts("Voo nao encontrado");
        } else {
            printf("Numero da Aeronave (atual: %d)\n? ", current_ptr->aircraft_number);
            scanf(" %d", &current_ptr->aircraft_number);
            printf("Empresa (atual: %s)\n? ", current_ptr->airline);
            scanf(" %19[^\n]", current_ptr->airline);
            printf("Data da partida (atual: %s)\n? ", current_ptr->departure_date);
            scanf(" %14[^\n]", current_ptr->departure_date);
            printf("Horario da partida (atual: %s)\n? ", current_ptr->departure_time);
            scanf(" %9[^\n]", current_ptr->departure_time);
            printf("Origem (atual: %s)\n? ", current_ptr->origin);
            scanf(" %49[^\n]", current_ptr->origin);
            printf("Destino (atual: %s)\n? ", current_ptr->destination);
            scanf(" %49[^\n]", current_ptr->destination);
            puts("Voo alterado com sucesso");
        }
        break;
    }
    case 2: {
        /* Alterar passagem */
        if (*ticket_ptr == NULL) {
            puts("Nao existem passagens no sistema");
            return;
        }
        puts("Alterando Passagens:");
        int number;
        printf("Digite o numero da passagem a ser alterada\n? ");
        scanf(" %d", &number);

        TICKET_PTR current_ptr = *ticket_ptr;
        while (current_ptr != NULL && current_ptr->number != number) {
            current_ptr = current_ptr->next;
        }

        if (current_ptr == NULL) {
            puts("Passagem nao encontrada");
        } else {
            printf("Identificador do Passageiro (atual: %d)\n? ",
                   current_ptr->passenger_id);
            scanf(" %d", &current_ptr->passenger_id);
            printf("Identificador do Voo (atual: %d)\n? ",
                   current_ptr->flight_id);
            scanf(" %d", &current_ptr->flight_id);
            printf("Valor (atual: %.2f)\n? ", current_ptr->price);
            scanf(" %lf", &current_ptr->price);
            printf("Data da Venda (atual: %s)\n? ", current_ptr->sale_date);
            scanf(" %14[^\n]", current_ptr->sale_date);
            puts("Passagem alterada com sucesso");
        }
        break;
    }
    case 3: {
        /* Alterar passageiro */
        if (*passenger_ptr == NULL) {
            puts("Nao existem passageiros no sistema");
            return;
        }
        puts("Alterando Passageiros:");
        int id;
        printf("Digite o identificador do passageiro a ser alterado\n? ");
        scanf(" %d", &id);

        PASSENGER_PTR current_ptr = *passenger_ptr;
        while (current_ptr != NULL && current_ptr->id != id) {
            current_ptr = current_ptr->next;
        }

        if (current_ptr == NULL) {
            puts("Passageiro nao encontrado");
        } else {
            printf("Nome (atual: %s)\n? ", current_ptr->name);
            scanf(" %29[^\n]", current_ptr->name);
            printf("Identidade (atual: %s)\n? ", current_ptr->identity);
            scanf(" %19[^\n]", current_ptr->identity);
            printf("Endereco (atual: %s)\n? ", current_ptr->address);
            scanf(" %49[^\n]", current_ptr->address);
            printf("Telefone (atual: %s)\n? ", current_ptr->phone);
            scanf(" %19[^\n]", current_ptr->phone);
            printf("Sexo (atual: %c)\n? ", current_ptr->gender);
            scanf(" %c", &current_ptr->gender);
            puts("Passageiro alterado com sucesso");
        }
        break;
    }
    }
}

/* === Consultar === */

void View(const FLIGHT_PTR *flight_ptr, const TICKET_PTR *ticket_ptr,
          const PASSENGER_PTR *passenger_ptr, int choice) {
    switch (choice) {
    case 1: {
        /* Consultar voos */
        if (*flight_ptr == NULL) {
            puts("Nao existem voos no sistema");
            return;
        }
        puts("Consultando Voos:");
        FLIGHT_PTR current_ptr = *flight_ptr;
        int counter = 1;
        while (current_ptr != NULL) {
            printf("Voo: #%d\n", counter);
            printf("Identificador:              %d\n", current_ptr->id);
            printf("Numero da Aeronave:         %d\n", current_ptr->aircraft_number);
            printf("Empresa:                    %s\n", current_ptr->airline);
            printf("Data da partida:            %s\n", current_ptr->departure_date);
            printf("Horario da partida:         %s\n", current_ptr->departure_time);
            printf("Origem:                     %s\n", current_ptr->origin);
            printf("Destino:                    %s\n", current_ptr->destination);

            /* Calcula passageiros deste voo dinamicamente via passagens */
            int passengers_in_flight = 0;
            TICKET_PTR current_ticket = *ticket_ptr;
            while (current_ticket != NULL) {
                if (current_ticket->flight_id == current_ptr->id) {
                    passengers_in_flight++;
                }
                current_ticket = current_ticket->next;
            }
            printf("Quantidade de Passageiros:  %d\n\n", passengers_in_flight);

            current_ptr = current_ptr->next;
            counter++;
        }
        break;
    }
    case 2: {
        /* Consultar passagens */
        if (*ticket_ptr == NULL) {
            puts("Nao existem passagens no sistema");
            return;
        }
        puts("Consultando Passagens");
        TICKET_PTR current_ptr = *ticket_ptr;
        while (current_ptr != NULL) {
            printf("Numero:                     #%d\n", current_ptr->number);
            printf("Identificador Passageiro:   %d\n", current_ptr->passenger_id);
            printf("Identificador Voo:          %d\n", current_ptr->flight_id);
            printf("Valor:                      R$%.2lf\n", current_ptr->price);
            printf("Data da Venda:              %s\n\n", current_ptr->sale_date);
            current_ptr = current_ptr->next;
        }
        break;
    }
    case 3: {
        /* Consultar passageiros */
        if (*passenger_ptr == NULL) {
            puts("Nao existem passageiros no sistema");
            return;
        }
        puts("Consultando Passageiros:");
        PASSENGER_PTR current_ptr = *passenger_ptr;
        int counter = 1;
        while (current_ptr != NULL) {
            printf("Passageiro: #%d\n", counter);
            printf("Identificador: %d\n", current_ptr->id);
            printf("Nome:           %s\n", current_ptr->name);
            printf("Identidade:     %s\n", current_ptr->identity);
            printf("Endereco:       %s\n", current_ptr->address);
            printf("Telefone:       %s\n", current_ptr->phone);
            printf("Sexo:           %c\n\n", current_ptr->gender);
            current_ptr = current_ptr->next;
            counter++;
        }
        break;
    }
    }
}

/* === Remover === */

void Delete(FLIGHT_PTR *flight_ptr, TICKET_PTR *ticket_ptr,
            PASSENGER_PTR *passenger_ptr, int choice) {

    switch (choice) {
    case 1: {
        /*
         * Remove um voo e, em cascata, todas as passagens e passageiros
         * associados àquele voo.
         */
        if (*flight_ptr == NULL) {
            puts("Nao existem voos no sistema");
            return;
        }
        int id;
        puts("Removendo Voo:");
        printf("Digite o identificador do voo a ser removido\n? ");
        scanf(" %d", &id);

        FLIGHT_PTR current_ptr = *flight_ptr, prev_ptr = NULL;
        while (current_ptr != NULL && current_ptr->id != id) {
            prev_ptr = current_ptr;
            current_ptr = current_ptr->next;
        }

        if (current_ptr == NULL) {
            puts("Voo nao encontrado");
            return;
        }

        /* Remove passagens e passageiros associados ao voo */
        TICKET_PTR current_ticket = *ticket_ptr, ticket_prev = NULL;
        while (current_ticket != NULL) {
            if (current_ticket->flight_id == id) {

                /* Remove o passageiro vinculado a esta passagem */
                PASSENGER_PTR current_passenger = *passenger_ptr;
                PASSENGER_PTR passenger_prev = NULL;
                while (current_passenger != NULL) {
                    if (current_passenger->id == current_ticket->passenger_id) {
                        if (passenger_prev == NULL) {
                            *passenger_ptr = current_passenger->next;
                        } else {
                            passenger_prev->next = current_passenger->next;
                        }
                        free(current_passenger);
                        total_passengers--;
                        break;
                    }
                    passenger_prev = current_passenger;
                    current_passenger = current_passenger->next;
                }

                /* Remove a passagem */
                TICKET_PTR ticket_to_remove = current_ticket;
                current_ticket = current_ticket->next;

                if (ticket_prev == NULL) {
                    *ticket_ptr = current_ticket;
                } else {
                    ticket_prev->next = current_ticket;
                }
                free(ticket_to_remove);
                total_tickets--;
            } else {
                ticket_prev = current_ticket;
                current_ticket = current_ticket->next;
            }
        }

        /* Remove o voo da lista */
        if (prev_ptr == NULL) {
            *flight_ptr = current_ptr->next;
        } else {
            prev_ptr->next = current_ptr->next;
        }
        free(current_ptr);
        total_flights--;

        puts("Voo, passagens e passageiros associados removidos com sucesso");
        break;
    }
    case 2: {
        /* Remove apenas uma passagem */
        if (*ticket_ptr == NULL) {
            puts("Nao existem passagens no sistema");
            return;
        }
        int number;
        puts("Removendo Passagem:");
        printf("Digite o numero da passagem a ser removida\n? ");
        scanf(" %d", &number);

        TICKET_PTR current_ptr = *ticket_ptr, prev_ptr = NULL;
        while (current_ptr != NULL && current_ptr->number != number) {
            prev_ptr = current_ptr;
            current_ptr = current_ptr->next;
        }

        if (current_ptr == NULL) {
            puts("Passagem nao encontrada");
            return;
        }

        if (prev_ptr == NULL) {
            *ticket_ptr = current_ptr->next;
        } else {
            prev_ptr->next = current_ptr->next;
        }
        free(current_ptr);
        total_tickets--;
        puts("Passagem removida com sucesso");
        break;
    }
    case 3: {
        /*
         * Remove um passageiro e todas as suas passagens associadas.
         */
        if (*passenger_ptr == NULL) {
            puts("Nao existem passageiros no sistema");
            return;
        }
        int id;
        puts("Removendo Passageiro:");
        printf("Digite o identificador do passageiro a ser removido\n? ");
        scanf(" %d", &id);

        PASSENGER_PTR current_ptr = *passenger_ptr, prev_ptr = NULL;
        while (current_ptr != NULL && current_ptr->id != id) {
            prev_ptr = current_ptr;
            current_ptr = current_ptr->next;
        }

        if (current_ptr == NULL) {
            puts("Passageiro nao encontrado");
            return;
        }

        /* Remove passagens associadas ao passageiro */
        TICKET_PTR current_ticket = *ticket_ptr, ticket_prev = NULL;
        while (current_ticket != NULL) {
            if (current_ticket->passenger_id == id) {
                TICKET_PTR ticket_to_remove = current_ticket;
                current_ticket = current_ticket->next;

                if (ticket_prev == NULL) {
                    *ticket_ptr = current_ticket;
                } else {
                    ticket_prev->next = current_ticket;
                }
                free(ticket_to_remove);
                total_tickets--;
            } else {
                ticket_prev = current_ticket;
                current_ticket = current_ticket->next;
            }
        }

        /* Remove o passageiro */
        if (prev_ptr == NULL) {
            *passenger_ptr = current_ptr->next;
        } else {
            prev_ptr->next = current_ptr->next;
        }
        free(current_ptr);
        total_passengers--;

        puts("Passageiro e suas passagens removidos com sucesso");
        break;
    }
    default:
        puts("Opcao invalida");
        break;
    }
}

/* === Relatórios === */

void Report(FLIGHT_PTR flight_ptr, PASSENGER_PTR passenger_ptr,
            TICKET_PTR ticket_ptr) {
    printf("\n--- Relatorio ---\n");

    /* Quantidade de passagens por voo */
    printf("Quantidade de passagens por voo:\n");
    FLIGHT_PTR current_flight = flight_ptr;
    while (current_flight != NULL) {
        int tickets_per_flight = 0;
        TICKET_PTR current_ticket = ticket_ptr;
        while (current_ticket != NULL) {
            if (current_ticket->flight_id == current_flight->id) {
                tickets_per_flight++;
            }
            current_ticket = current_ticket->next;
        }
        printf("Voo %d: %d passagens\n",
               current_flight->id, tickets_per_flight);
        current_flight = current_flight->next;
    }

    /* Quantidade de voos por empresa (agrupado, sem repetições) */
    printf("\nQuantidade de voos por empresa:\n");
    {
        char printed_airlines[50][20];
        int printed_count = 0;

        current_flight = flight_ptr;
        while (current_flight != NULL) {
            /* Pula empresas já exibidas */
            int already_printed = 0;
            for (int i = 0; i < printed_count; i++) {
                if (strcmp(printed_airlines[i], current_flight->airline) == 0) {
                    already_printed = 1;
                    break;
                }
            }

            if (!already_printed) {
                int flights_per_airline = 0;
                FLIGHT_PTR temp_flight = flight_ptr;
                while (temp_flight != NULL) {
                    if (strcmp(temp_flight->airline, current_flight->airline) == 0) {
                        flights_per_airline++;
                    }
                    temp_flight = temp_flight->next;
                }
                printf("Empresa %s: %d voo(s)\n",
                       current_flight->airline, flights_per_airline);
                snprintf(printed_airlines[printed_count],
                         sizeof(printed_airlines[0]),
                         "%s", current_flight->airline);
                printed_count++;
            }
            current_flight = current_flight->next;
        }
    }

    /* Lista de passageiros por voo */
    printf("\nLista de passageiros por voo:\n");
    current_flight = flight_ptr;
    while (current_flight != NULL) {
        printf("Voo %d:\n", current_flight->id);
        TICKET_PTR current_ticket = ticket_ptr;
        while (current_ticket != NULL) {
            if (current_ticket->flight_id == current_flight->id) {
                PASSENGER_PTR current_passenger = passenger_ptr;
                while (current_passenger != NULL) {
                    if (current_passenger->id == current_ticket->passenger_id) {
                        printf("  - %s\n", current_passenger->name);
                        break;
                    }
                    current_passenger = current_passenger->next;
                }
            }
            current_ticket = current_ticket->next;
        }
        current_flight = current_flight->next;
    }
    printf("-----------------\n");
}
