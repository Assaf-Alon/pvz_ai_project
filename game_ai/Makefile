BUILD_DIR := build/
# ======== level srcs ===========================
LEVEL_DIR := cpp_env/
LEVEL_SRCS := $(wildcard $(addsuffix *.cpp, $(LEVEL_DIR)))
LEVEL_SWIG_SRCS := $(wildcard $(addsuffix *.cxx, $(LEVEL_DIR)))
LEVEL_OBJS := $(patsubst $(LEVEL_DIR)%.cpp, $(BUILD_DIR)%.o, $(LEVEL_SRCS))
LEVEL_SWIG_OBJS := $(patsubst $(LEVEL_DIR)%.cpp, $(BUILD_DIR)%.o, $(LEVEL_SRCS)) \
				   $(patsubst $(LEVEL_DIR)%.cxx, $(BUILD_DIR)%.o, $(LEVEL_SWIG_SRCS))
LEVEL_SWIG_FILE := $(wildcard $(addsuffix *.i, $(LEVEL_DIR)))
LEVEL_PY := $(LEVEL_DIR)level.py
# ======== mcts srcs ============================
MCTS_DIR := cpp_mcts/
MCTS_SRCS := $(wildcard $(addsuffix *.cpp, $(MCTS_DIR)))
MCTS_SWIG_SRCS := $(wildcard $(addsuffix *.cxx, $(MCTS_DIR)))
MCTS_SWIG_OBJS := $(patsubst $(MCTS_DIR)%.cpp, $(BUILD_DIR)%.o, $(MCTS_SRCS)) \
				  $(patsubst $(MCTS_DIR)%.cxx, $(BUILD_DIR)%.o, $(MCTS_SWIG_SRCS))
MCTS_SWIG_FILE := $(wildcard $(addsuffix *.i, $(MCTS_DIR)))
MCTS_PY := $(MCTS_DIR)mcts.py
# ===============================================
LEVEL_LIB := lib_level.so # name of the swig-less level lib
EXEC := ai.out
LEVEL_SWIG_LIB := _level.so
MCTS_SWIG_LIB := _mcts.so
PYTHONI := -I/usr/include/python3.11 # change to 3.10 if 3.11 is not installed
PYTHONL := -Xlinker -export-dynamic
LIBFLAGS := -L/usr/local/lib -lgmpxx -lgmp -fopenmp
CFLAGS := -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -O2 -flto
# available sanitizers: address, undefined, leak, thread. Note: some of these are incompatible with eachother!
DFLAGS := -fsanitize=address,undefined,leak -g -O1 -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp
PRINT_DFLAGS := $(DFLAGS) -DDEBUG
CC := clang++
DEBUG_CPP := debug.cpp
DEBUG_EXEC := debug.out

# all: $(LEVEL_SWIG_LIB) $(MCTS_SWIG_LIB)
all: $(LEVEL_SWIG_LIB) $(MCTS_SWIG_LIB)
	cp $(LEVEL_PY) .
	cp $(MCTS_PY) .
	@echo "do: 'export LD_LIBRARY_PATH=$(pwd)"

$(BUILD_DIR)%.o: $(LEVEL_DIR)%.cpp
	$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

$(BUILD_DIR)%.o: $(LEVEL_DIR)%.cxx
	$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

$(BUILD_DIR)%.o: $(MCTS_DIR)%.cpp
	$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

$(BUILD_DIR)%.o: $(MCTS_DIR)%.cxx
	$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

$(LEVEL_LIB): $(LEVEL_OBJS)
	$(CC) -flto -shared $(LEVEL_OBJS) $(LIBFLAGS) -o $(LEVEL_LIB)

$(LEVEL_SWIG_LIB): $(LEVEL_SWIG_OBJS)
	$(CC) -flto -shared $(LEVEL_SWIG_OBJS) $(LIBFLAGS) -o $(LEVEL_SWIG_LIB)

$(MCTS_SWIG_LIB): $(MCTS_SWIG_OBJS) $(LEVEL_LIB)
	$(CC) -flto -shared -L. -l:$(LEVEL_LIB) $(MCTS_SWIG_OBJS) $(LEVEL_LIB) $(LIBFLAGS) -o $(MCTS_SWIG_LIB)

level_wrap.cxx: level.i
	swig -c++ -python level.i

mcts_wrap.cxx: mcts.i
	swig -c++ -python mcts.i

.PHONY: debug
debug:
	$(CC) -o $(DEBUG_EXEC) $(DFLAGS) $(LEVEL_SRCS) $(MCTS_SRCS) $(DEBUG_CPP)

.PHONY: check
check:
	@echo $(LEVEL_SRCS)
	@echo $(LEVEL_SWIG_SRCS)
	@echo $(LEVEL_OBJS)
	@echo $(LEVEL_SWIG_OBJS)
	@echo $(LEVEL_SWIG_FILE)
	@echo "mcts:"
	@echo $(MCTS_SRCS)
	@echo $(MCTS_SWIG_OBJS)
	@echo $(MCTS_SWIG_FILE)
	

# $(MCTS_SWIG_LIB): $(MCTS_SWIG_OBJS) $(LEVEL_OBJS) ADAPT THIS FOR DEBUG!!!
# 	$(CC) -flto -shared $(MCTS_SWIG_OBJS) $(LEVEL_OBJS) $(LIBFLAGS) -o $(MCTS_SWIG_LIB)




.PHONY: clean
clean:
	rm -r build/*
	rm *.so

.SUFFIXES:

# debug: 
# 	swig 
