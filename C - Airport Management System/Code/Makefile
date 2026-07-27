CC       = gcc
CFLAGS   = -std=c99 -Wall -Wextra -pedantic
TARGET   = build/AirportManager

.PHONY: all test valgrind clean

all: $(TARGET)

$(TARGET): AirportManager.c
	@mkdir -p build
	$(CC) $(CFLAGS) -o $@ $<

test: $(TARGET)
	./testbenchs/run_all.sh

valgrind: $(TARGET)
	valgrind --leak-check=full --error-exitcode=1 ./testbenchs/run_all.sh

clean:
	rm -rf build
