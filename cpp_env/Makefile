CC=g++
CFLAGS=-I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp
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

fast-sanitize:
	clang++ -O2 -o $(EXEC) $(CFLAGS) -fsanitize=address,undefined,leak *.cpp

profile:
	$(CC) -O2 -o $(EXEC) $(CFLAGS) -pg *.cpp
	./$(EXEC)
	gprof main.out  gmon.out > analysis.txt

intel-profile:
	icpx -O2 -o $(EXEC) $(CFLAGS) -lsvml -shared-intel -debug inline-debug-info -qopenmp -g *.cpp

clang-profile-optimize: #WARNING: SLOW
	clang++ -O2 -o $(EXEC) $(CFLAGS) -fprofile-instr-generate *.cpp
	./$(EXEC)
	llvm-profdata merge -output=code.profdata *.profraw 
	clang++ -O2 -o $(EXEC) $(CFLAGS) -fprofile-instr-use=code.profdata *.cpp

clean:
	rm -f $(OBJ) main.out