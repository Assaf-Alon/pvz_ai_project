CC=g++
CFLAGS=-I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -O2
DFLAGS = -DDEBUG -g $(CFLAGS)
DEPS = level.h
OBJ = main.o plant.o zombie.o level.o
EXEC = main.out
PYTHONI = -I/usr/include/python3.11
PYTHONL = -Xlinker -export-dynamic
LIBFLAGS = -L/usr/local/lib -lgmpxx -lgmp

all: $(OBJ)
	$(CC) -o $(EXEC) $^ $(CFLAGS)

debug: #$(OBJ)
	$(CC) -o $(EXEC) $(DFLAGS) *.cpp

clang-debug: #$(OBJ)
	clang++ -fsanitize=address -o $(EXEC) $(DFLAGS) *.cpp

fast:
	clang++ -O2 -o $(EXEC) $(CFLAGS) *.cpp

fast-sanitize:
	clang++ -O2 -o $(EXEC) -g $(CFLAGS) -fsanitize=address,undefined,leak *.cpp

profile:
	$(CC) -O2 -o $(EXEC) $(CFLAGS) -pg *.cpp
	./$(EXEC)
	gprof main.out gmon.out > analysis.txt

intel-profile:
	icpx -O2 -o $(EXEC) $(CFLAGS) -lsvml -shared-intel -debug inline-debug-info -qopenmp -g *.cpp

clang-profile-optimize: #WARNING: SLOW
	clang++ -O2 -o $(EXEC) $(CFLAGS) -fprofile-instr-generate *.cpp
	./$(EXEC)
	llvm-profdata merge -output=code.profdata *.profraw 
	clang++ -O2 -o $(EXEC) $(CFLAGS) -fprofile-instr-use=code.profdata *.cpp

swig:
	-rm level_wrap.*
	-rm *.so
	-rm level.py
	swig -c++ -python level.i 
	g++ -fPIC $(CFLAGS) $(PYTHONI) -c level.cpp      -o level.o
	g++ -fPIC $(CFLAGS) $(PYTHONI) -c zombie.cpp     -o zombie.o
	g++ -fPIC $(CFLAGS) $(PYTHONI) -c plant.cpp      -o plant.o
	g++ -fPIC $(CFLAGS) $(PYTHONI) -c level_wrap.cxx -o level_wrap.o
	g++ -O2 $(PYTHONL) -shared level.o plant.o zombie.o level_wrap.o -fopenmp $(LIBFLAGS) -o _level.so
	-rm *.o

clean:
	rm -f $(OBJ) main.out
	rm *.o 
	rm *.so