BUILD_DIR := build/
# ======== level srcs ===========================
LEVEL_DIR := cpp_env/
LEVEL_SRCS := $(wildcard $(addsuffix *.cpp, $(LEVEL_DIR)))
LEVEL_HEADERS := $(wildcard $(addsuffix *.hpp, $(LEVEL_DIR)))
LEVEL_SWIG_SRCS := $(LEVEL_DIR)level_wrap.cxx
LEVEL_OBJS := $(patsubst $(LEVEL_DIR)%.cpp, $(BUILD_DIR)%.o, $(LEVEL_SRCS))
LEVEL_SWIG_OBJS := $(patsubst $(LEVEL_DIR)%.cpp, $(BUILD_DIR)%.o, $(LEVEL_SRCS)) \
				   $(patsubst $(LEVEL_DIR)%.cxx, $(BUILD_DIR)%.o, $(LEVEL_SWIG_SRCS))
LEVEL_SWIG_FILE := $(wildcard $(addsuffix *.i, $(LEVEL_DIR)))
LEVEL_PY := $(LEVEL_DIR)level.py
# ======== mcts srcs ============================
MCTS_DIR := cpp_mcts/
MCTS_SRCS := $(wildcard $(addsuffix *.cpp, $(MCTS_DIR)))
MCTS_HEADERS := $(wildcard $(addsuffix *.h, $(MCTS_DIR)))
MCTS_SWIG_SRCS := $(MCTS_DIR)mcts_wrap.cxx
MCTS_SWIG_OBJS := $(patsubst $(MCTS_DIR)%.cpp, $(BUILD_DIR)%.o, $(MCTS_SRCS)) \
				  $(patsubst $(MCTS_DIR)%.cxx, $(BUILD_DIR)%.o, $(MCTS_SWIG_SRCS))
MCTS_SWIG_FILE := $(wildcard $(addsuffix *.i, $(MCTS_DIR)))
MCTS_PY := $(MCTS_DIR)mcts.py
# ===============================================
LEVEL_LIB := $(BUILD_DIR)lib_level.so # name of the swig-less level lib
EXEC := ai.out
LEVEL_SWIG_LIB := $(BUILD_DIR)_level.so
MCTS_SWIG_LIB := $(BUILD_DIR)_mcts.so
PYTHONI := -I/usr/include/python3.11 # change to 3.10 if 3.11 is not installed
PYTHONL := -Xlinker -export-dynamic
LIBFLAGS := -L/usr/local/lib -lgmpxx -lgmp -fopenmp
CFLAGS := -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp -O2 -flto -Wno-missing-field-initializers # -funroll-loops # -mavx # -march=native -ffast-math -fvectorize
# available sanitizers: address, undefined, leak, thread. Note: some of these are incompatible with eachother!
DFLAGS := -fsanitize=address,undefined,leak -g -O1 -I. -std=c++20 -Wall -Werror -Wextra -Wno-unused-parameter -fopenmp
PRINT_DFLAGS := $(DFLAGS) -DDEBUG
CC := clang++
DEBUG_CPP := debug.cpp
DEBUG_EXEC := debug.out
PROFILE_EXEC := profile_exec.out

# all: $(LEVEL_SWIG_LIB) $(MCTS_SWIG_LIB)
all: $(LEVEL_SWIG_LIB) $(MCTS_SWIG_LIB) $(LEVEL_SWIG_SRCS) $(MCTS_SWIG_SRCS)
	cp $(LEVEL_PY) $(BUILD_DIR)
	cp $(MCTS_PY) $(BUILD_DIR)
	export LD_LIBRARY_PATH=$(realpath .)
	@echo "do: 'export LD_LIBRARY_PATH=$(pwd)"

$(BUILD_DIR)%.o: $(LEVEL_DIR)%.cpp
	$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

$(BUILD_DIR)%.o: $(LEVEL_DIR)%.cxx
	$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

$(BUILD_DIR)%.o: $(MCTS_DIR)%.cpp $(MCTS_HEADERS)
	$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

$(BUILD_DIR)%.o: $(MCTS_DIR)%.cxx
	$(CC) $(CFLAGS) $(PYTHONI) -c $< -o $@ -fPIC

$(LEVEL_LIB): $(LEVEL_OBJS) 
	$(CC) -flto -shared $(LEVEL_OBJS) $(LIBFLAGS) -o $(LEVEL_LIB)

$(LEVEL_SWIG_LIB): $(LEVEL_SWIG_OBJS) $(LEVEL_SWIG_SRCS)
	$(CC) $(PYTHONL) -flto -shared $(LEVEL_SWIG_OBJS) $(LIBFLAGS) -o $(LEVEL_SWIG_LIB)

$(MCTS_SWIG_LIB): $(MCTS_SWIG_OBJS) $(LEVEL_LIB) $(MCTS_SWIG_SRCS) 
	$(CC) $(PYTHONL) -flto -shared -L. -l:$(LEVEL_LIB) $(MCTS_SWIG_OBJS) $(LEVEL_LIB) $(LIBFLAGS) -o $(MCTS_SWIG_LIB)

# .PHONY: $(LEVEL_SWIG_SRCS)
$(LEVEL_SWIG_SRCS): $(LEVEL_DIR)level.hpp # $(LEVEL_SWIG_FILE) $(LEVEL_SRCS)
	swig -c++ -python $(LEVEL_DIR)level.i

# .PHONY: $(MCTS_SWIG_SRCS)
$(MCTS_SWIG_SRCS): $(MCTS_DIR)mcts.h # $(MCTS_SWIG_FILE) $(MCTS_SRCS)
	swig -c++ -python $(MCTS_DIR)mcts.i

.PHONY: fast
fast:
	$(CC) -o $(EXEC) $(CFLAGS) $(LEVEL_SRCS) $(MCTS_SRCS) $(DEBUG_CPP)

.PHONY: debug
debug:
	$(CC) -o $(DEBUG_EXEC) $(DFLAGS) $(LEVEL_SRCS) $(MCTS_SRCS) $(DEBUG_CPP)

.PHONY: profile
profile:
	g++ -pg -O2 -fopenmp -o $(PROFILE_EXEC) $(LEVEL_SRCS) $(MCTS_SRCS) $(DEBUG_CPP)

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
	touch build/__init__.py
	rm cpp_env/level_wrap.cxx
	rm cpp_env/level.py
	rm cpp_mcts/mcts_wrap.cxx
	rm cpp_mcts/mcts.py

.SUFFIXES:

# debug: 
# 	swig 
