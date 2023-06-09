CC=g++
CFLAGS=-I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -O2
DFLAGS = -DDEBUG -g $(CFLAGS)
DEPS = level.h
OBJ = main.o plant.o zombie.o level.o
EXEC = main.out
BUILD_DIR = build
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
	mv gmon.out profile/
	gprof main.out profile/gmon.out > analysis.txt

intel-profile:
	icpx -O2 -o $(EXEC) $(CFLAGS) -lsvml -shared-intel -debug inline-debug-info -qopenmp -g *.cpp

clang-profile-optimize: #WARNING: SLOW
	clang++ -O2 -o $(EXEC) $(CFLAGS) -fprofile-instr-generate *.cpp
	./$(EXEC)
	mv *.profraw profile/
	llvm-profdata merge -output=profile/code.profdata *.profraw 
	clang++ -O2 -o $(EXEC) $(CFLAGS) -fprofile-instr-use=profile/code.profdata *.cpp

swig:

	swig -c++ -python -outdir $(BUILD_DIR) level.i 
	g++ -fPIC $(CFLAGS) $(PYTHONI) -c level.cpp      -o $(BUILD_DIR)/level.o
	g++ -fPIC $(CFLAGS) $(PYTHONI) -c zombie.cpp     -o $(BUILD_DIR)/zombie.o
	g++ -fPIC $(CFLAGS) $(PYTHONI) -c plant.cpp      -o $(BUILD_DIR)/plant.o
	g++ -fPIC $(CFLAGS) $(PYTHONI) -c level_wrap.cxx -o $(BUILD_DIR)/level_wrap.o
	g++ -O2 $(PYTHONL) -shared $(BUILD_DIR)/level.o $(BUILD_DIR)/plant.o $(BUILD_DIR)/zombie.o $(BUILD_DIR)/level_wrap.o -fopenmp $(LIBFLAGS) -o _level.so

clean:
	rm -f $(OBJ) main.out
	rm *.o 
	rm *.so