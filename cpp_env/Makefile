CC=g++
CFLAGS=-I. -std=c++17 -Wall -Werror -Wextra# -O3
DFLAGS = -DDEBUG -g $(CFLAGS)
DEPS = level.h
OBJ = main.o plant.o zombie.o level.o
EXEC = main.out

all: $(OBJ)
	$(CC) -o $(EXEC) $^ $(CFLAGS)

debug: #$(OBJ)
	$(CC) -o $(EXEC) -DDEBUG *.cpp
# $(CC) -o $(EXEC) $^ $(DFLAGS)

clean:
	rm -f $(OBJ) main.out