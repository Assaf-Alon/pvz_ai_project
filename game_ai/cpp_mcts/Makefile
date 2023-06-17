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

debug-FUBAR:
	mkdir tmp/
	swig -c++ -python mcts.i
	cp ../cpp_env/*.cpp tmp/
	cp ../cpp_env/*.cxx tmp/
	cp ../cpp_env/*.hpp tmp/
	cp ../cpp_env/*.h tmp/
	cp mcts* tmp/
	clang++ -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -fsanitize=address,leak,undefined -O2 -flto -I/usr/include/python3.11 -c tmp/mcts_wrap.cxx -o mcts_wrap.o -fPIC
	clang++ -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -fsanitize=address,leak,undefined -O2 -flto -I/usr/include/python3.11 -c tmp/level_wrap.cxx -o level_wrap.o -fPIC
	clang++ -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -fsanitize=address,leak,undefined -O2 -flto -I/usr/include/python3.11 -c tmp/zombie.cpp -o zombie.o -fPIC
	clang++ -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -fsanitize=address,leak,undefined -O2 -flto -I/usr/include/python3.11 -c tmp/plant.cpp -o plant.o -fPIC
	clang++ -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -fsanitize=address,leak,undefined -O2 -flto -I/usr/include/python3.11 -c tmp/level.cpp -o level.o -fPIC
	clang++ -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -fsanitize=address,leak,undefined -O2 -flto -I/usr/include/python3.11 -c tmp/mcts.cpp -o mcts.o -fPIC
	clang++ -Xlinker -export-dynamic -flto -shared *.o -L/usr/local/lib -lgmpxx -lgmp -fopenmp -fsanitize=address,leak,undefined -o _mcts.so
	rm -r tmp/

# Rule for generating the swig interface file
mcts_wrap.cxx: mcts.i
		swig -c++ -python mcts.i

# Clean target to remove generated files
.PHONY: clean
clean:
		rm -f $(SWIG_OBJS) $(SWIG_LIBRARY) mcts_wrap.cxx mcts_wrap.o mcts.py *.o

# Additional dependencies
$(SWIG_OBJS): mcts.h

# Disable implicit rules
.SUFFIXES: