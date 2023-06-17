#!/bin/bash

cd cpp_env/
make clean && make -j4 && make lib -j4
cd ..
rm cpp_mcts/lib_level.so
cp cpp_env/lib_level.so cpp_mcts/
cd cpp_mcts/
make clean && make
cd ..
echo "==========================================================================================="
echo "do 'export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/PATH/TO/cpp_env/' if you want things to work!"
echo "==========================================================================================="