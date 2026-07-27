CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -pedantic-errors
TARGET = build/TrackDetector
SRC = TrackDetector.c
CASOS = test-cases

TEST_FILES = $(wildcard $(CASOS)/test-case_*.txt)
TEST_TARGETS = $(patsubst $(CASOS)/test-case_%.txt, test-case_%, $(TEST_FILES))

.PHONY: all clean

all: $(TARGET)
	@for test in $(TEST_TARGETS); do \
		echo "========== $$test =========="; \
		./$(TARGET) < $(CASOS)/$$test.txt; \
	done

$(TARGET): $(SRC)
	@mkdir -p build
	$(CC) $(CFLAGS) -o $@ $^

test-case_%: $(TARGET) $(CASOS)/test-case_%.txt
	@echo "========== $@ =========="
	./$(TARGET) < $(CASOS)/$@.txt

clean:
	rm -rf build
