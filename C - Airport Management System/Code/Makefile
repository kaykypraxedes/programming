CC       = gcc
CFLAGS   = -std=c99 -Wall -Wextra -pedantic
TARGET   = airport_manager

.PHONY: all test valgrind clean

all: $(TARGET)

$(TARGET): airport_manager.c
	$(CC) $(CFLAGS) -o $@ $<

test: $(TARGET)
	./testbenchs/run_all.sh

valgrind: $(TARGET)
	valgrind --leak-check=full --error-exitcode=1 ./testbenchs/run_all.sh

clean:
	rm -f $(TARGET)
