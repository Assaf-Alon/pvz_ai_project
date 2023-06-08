%module level
%include "std_string.i"
%include "std_vector.i"
%include "std_pair.i"
%include "std_deque.i"
%include "typemaps.i"
%{
    #define SWIG_FILE_WITH_INIT
    #include "level.hpp"
%}
namespace std{
    %template(LegalPlantVector) vector<int>;
    %template(ZombieQueue) deque<ZombieSpawnTemplate>;
    %template(FreePositions) pair<int, int>;
    %template(PlantDataVector) vector<PlantData>;
}
%include "level.hpp"