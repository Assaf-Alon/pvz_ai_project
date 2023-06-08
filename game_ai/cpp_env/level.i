%module level
%include "std_string.i"
%include "std_vector.i"
%include "std_pair.i"
%include "std_deque.i"
%include "typemaps.i"
%include "std_pair.i"
%{
    #define SWIG_FILE_WITH_INIT
    #include "level.hpp"
%}
namespace std{
    %template(LegalPlantVector) vector<int>;
    %template(ZombieQueue) deque<ZombieSpawnTemplate>;
    %template(FreePositions) pair<int, int>;
    %template(PlantDataVector) vector<PlantData>;
    %template(position) pair<int, int>;
    %template(observation_vector) vector<CellObservation>;
    %template(observation_matrix) vector<vector<CellObservation>>;
    %template(state_lane) vector<Cell>;
    %template(state_matrix) vector<vector<Cell>>;
}
%include "level.hpp"