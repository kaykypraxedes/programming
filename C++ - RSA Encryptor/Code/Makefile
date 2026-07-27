CXX      = g++
CXXFLAGS = -Wall -Wextra -MMD
TARGET   = build/RSAEncryptor
SRCS     = Main.cpp Crypto.cpp Factor.cpp Primes.cpp Time.cpp
OBJS     = $(SRCS:%.cpp=build/%.o)
DEPS     = $(OBJS:.o=.d)

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

build/%.o: %.cpp
	@mkdir -p build
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -rf build

-include $(DEPS)
