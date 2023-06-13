# Define the source files and object files
SRCS := level_wrap.cxx zombie.cpp plant.cpp level.cpp 
OBJS := $(SRCS:%.cpp=%.o)
OBJS := $(OBJS:%.cxx=%.o)
EXEC := main.out
LIBRARY := _level.so
PYTHONI := -I/usr/include/python3.11
PYTHONL := -Xlinker -export-dynamic
LIBFLAGS := -L/usr/local/lib -lgmpxx -lgmp
CFLAGS := -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -O2 -flto
DFLAGS := -DDEBUG -fsanitize=address,undefined,leak,thread -g $(CFLAGS) -OO
CC := clang++

# Default target
all: $(LIBRARY)

# Rule for generating object files from source files
%.o: %.cpp
		$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

%.o: %.cxx
		$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

# Rule for generating the library by linking object files
$(LIBRARY): $(OBJS)
		$(CC) $(PYTHONL) -flto -shared $(OBJS) $(LIBFLAGS) -fopenmp -o $(LIBRARY)

# Rule for generating the swig interface file
level_wrap.cxx: level.i
		swig -c++ -python level.i

# Clean target to remove generated files
.PHONY: clean
clean:
		rm -f $(OBJS) $(LIBRARY) level_wrap.cxx level_wrap.o level.py level.pyc

# Additional dependencies
$(OBJS): level.hpp

# Disable implicit rules
.SUFFIXES:

debug:
	$(CC) -o $(EXEC) $(DFLAGS) *.cpp

fast:
	clang++ -o $(EXEC) $(CFLAGS) *.cpp

fast-sanitize:
	clang++ -o $(EXEC) -g -std=c++20 -fopenmp -O0 -fsanitize=address,undefined,leak *.cpp

.PHONY: profile
profile:
	g++ -o $(EXEC) -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -O2 -pg *.cpp
	./$(EXEC)
	mv gmon.out profile/
	gprof main.out profile/gmon.out > profile/analysis.txt

clang-profile-optimize:
	$(CC) -o $(EXEC) $(CFLAGS) -fprofile-instr-generate *.cpp
	./$(EXEC)
	mv *.profraw profile/
	llvm-profdata merge -output=profile/code.profdata profile/*.profraw 
	$(CC) -o $(EXEC) $(CFLAGS) -fprofile-instr-use=profile/code.profdata *.cpp