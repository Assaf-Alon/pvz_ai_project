# Define the source files and object files
SWIG_SRCS := mcts_wrap.cxx mcts.cpp 
SWIG_OBJS := $(SWIG_SRCS:%.cpp=%.o)
SWIG_OBJS := $(SWIG_OBJS:%.cxx=%.o)
LEVEL_LIB := lib_level.so
EXEC := mcts.out
SWIG_LIBRARY := _mcts.so
PYTHONI := -I/usr/include/python3.11
PYTHONL := -Xlinker -export-dynamic
LIBFLAGS := -L/usr/local/lib -lgmpxx -lgmp
CFLAGS := -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -O2 -flto
DFLAGS := -DDEBUG -fsanitize=address,undefined,leak,thread -g $(CFLAGS) -OO
CC := clang++

# Default target
all: $(SWIG_LIBRARY)

# Rule for generating object files from source files
%.o: %.cpp
		$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

%.o: %.cxx
		$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

# Rule for generating the library by linking object files
$(SWIG_LIBRARY): $(SWIG_OBJS)
		$(CC) $(PYTHONL) -L. -l:lib_level.so -flto -shared $(SWIG_OBJS) $(LEVEL_LIB) $(LIBFLAGS) -fopenmp -o $(SWIG_LIBRARY)

$(LIBRARY): $(OBJS)
	$(CC) $(CFLAGS) -shared $(OBJS) -o $(LIBRARY)

# Rule for generating the swig interface file
mcts_wrap.cxx: mcts.i
		swig -c++ -python mcts.i

# Clean target to remove generated files
.PHONY: clean
clean:
		rm -f $(SWIG_OBJS) $(SWIG_LIBRARY) mcts_wrap.cxx mcts_wrap.o mcts.py

# Additional dependencies
$(SWIG_OBJS): mcts.h

# Disable implicit rules
.SUFFIXES: