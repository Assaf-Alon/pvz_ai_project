CC=g++
CFLAGS=-I. -std=c++20 -Wall -Werror -Wextra -fopenmp
DFLAGS = -DDEBUG -g $(CFLAGS)
DEPS = level.h
OBJ = main.o plant.o zombie.o level.o
EXEC = main.out

all: $(OBJ)
	$(CC) -o $(EXEC) $^ $(CFLAGS)

debug: #$(OBJ)
	$(CC) -o $(EXEC) $(DFLAGS) *.cpp
# $(CC) -o $(EXEC) $^ $(DFLAGS)

clang-debug: #$(OBJ)
	clang++ -fsanitize=address -o $(EXEC) $(DFLAGS) *.cpp

fast:
	clang++ -O2 -o $(EXEC) $(CFLAGS) *.cpp

profile:
	$(CC) -O2 -o $(EXEC) $(CFLAGS) -pg *.cpp

clean:
	rm -f $(OBJ) main.out