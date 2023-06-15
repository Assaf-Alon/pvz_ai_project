%module mcts
%include "std_string.i"
%include "std_vector.i"
%include "std_pair.i"
%include "typemaps.i"
%include "std_list.i"
%{
    #define SWIG_FILE_WITH_INIT
    #include "mcts.h"
%}
%include "mcts.h"