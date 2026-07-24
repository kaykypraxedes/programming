CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -pedantic-errors
TARGET = detectarPista
SRC = detectarPista.c
CASOS = casos-teste

.PHONY: all clean run-teste1 run-teste2 run-teste3 run-teste4 run-all

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $^

run-teste1: $(TARGET)
	@echo "========== Caso de Teste 1 =========="
	./$(TARGET) < $(CASOS)/caso-teste-1.txt

run-teste2: $(TARGET)
	@echo "========== Caso de Teste 2 =========="
	./$(TARGET) < $(CASOS)/caso-teste-2.txt

run-teste3: $(TARGET)
	@echo "========== Caso de Teste 3 =========="
	./$(TARGET) < $(CASOS)/caso-teste-3.txt

run-teste4: $(TARGET)
	@echo "========== Caso de Teste 4 =========="
	./$(TARGET) < $(CASOS)/caso-teste-4.txt

run-all: run-teste1 run-teste2 run-teste3 run-teste4

clean:
	rm -f $(TARGET)
