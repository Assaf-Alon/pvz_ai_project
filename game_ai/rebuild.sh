#!/bin/bash

cd cpp_env/
make clean && make -j4 && make lib -j4
cd ..
rm cpp_mcts/lib_level.so
cp cpp_env/lib_level.so cpp_mcts/
cd cpp_mcts/
make clean && make
cd ..