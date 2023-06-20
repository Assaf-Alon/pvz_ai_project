%module level
%include "std_string.i"
%include "std_vector.i"
%include "std_pair.i"
%include "std_array.i"
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
    // %template(PlantDataVector) vector<PlantData>;
    %template(Lawnmower) vector<bool>;
    %template(position) pair<int, int>;
    // %template(cell_observation) vector<int>;
    %template(observation_vector) vector<vector<int>>;
    %template(observation_matrix) vector<vector<vector<int>>>;
    %template(state_lane) vector<Cell>;
    %template(state_matrix) vector<vector<Cell>>;
    %template(Plant_list) array<PlantData, 18>; 
}
%include "level.hpp"