# Define the source files and object files
SWIG_SRCS := level_wrap.cxx zombie.cpp plant.cpp level.cpp 
SWIG_OBJS := $(SWIG_SRCS:%.cpp=%.o)
SWIG_OBJS := $(SWIG_OBJS:%.cxx=%.o)
EXEC := main.out
SWIG_LIBRARY := _level.so
LIBRARY := lib_level.so
LIB_SRCS := zombie.cpp plant.cpp level.cpp 
LIB_OBJS := $(LIB_SRCS:%.cpp=%.o)
PYTHONI := -I/usr/include/python3.11
PYTHONL := -Xlinker -export-dynamic
LIBFLAGS := -L/usr/local/lib -lgmpxx -lgmp
CFLAGS := -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -O2 -flto
DFLAGS := -DDEBUG -fsanitize=address,undefined,leak,thread -g $(CFLAGS) -OO
CC := clang++

# Default target
all: $(SWIG_LIBRARY)

lib: $(LIBRARY)

# Rule for generating object files from source files
%.o: %.cpp
		$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

%.o: %.cxx
		$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

# Rule for generating the library by linking object files
$(SWIG_LIBRARY): $(SWIG_OBJS)
		$(CC) $(PYTHONL) -flto -shared $(SWIG_OBJS) $(LIBFLAGS) -fopenmp -o $(SWIG_LIBRARY)


$(LIBRARY): $(LIB_OBJS)
	$(CC) -flto -shared $(LIB_OBJS) $(LIBFLAGS) -fopenmp -o $(LIBRARY)

# Rule for generating the swig interface file
level_wrap.cxx: level.i
		swig -c++ -python level.i

# Clean target to remove generated files
.PHONY: clean
clean:
		rm -f $(SWIG_OBJS) $(SWIG_LIBRARY) level_wrap.cxx level_wrap.o level.py level.pyc

# Additional dependencies
$(SWIG_OBJS): level.hpp

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