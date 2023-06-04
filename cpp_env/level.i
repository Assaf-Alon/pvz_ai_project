%module level
%include "std_string.i"
%include "std_vector.i"
%include "std_deque.i"
%include "typemaps.i"
// %template(ZombieSpawnTemplateDeque) std::deque<ZombieSpawnTemplate>;
%{
    #define SWIG_FILE_WITH_INIT
    #include "level.hpp"
%}
// %ignore std::deque<ZombieSpawnTemplate>::vector(size_type);
// %ignore std::deque<ZombieSpawnTemplate>::resize;
namespace std{
    %template(LegalPlantVector) vector<int>;
    %template(ZombieQueue) deque<ZombieSpawnTemplate>;
}
%include "level.hpp"