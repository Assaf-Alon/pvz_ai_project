# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _mcts
else:
    import _mcts

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _mcts.delete_SwigPyIterator

    def value(self):
        return _mcts.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _mcts.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _mcts.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _mcts.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _mcts.SwigPyIterator_equal(self, x)

    def copy(self):
        return _mcts.SwigPyIterator_copy(self)

    def next(self):
        return _mcts.SwigPyIterator_next(self)

    def __next__(self):
        return _mcts.SwigPyIterator___next__(self)

    def previous(self):
        return _mcts.SwigPyIterator_previous(self)

    def advance(self, n):
        return _mcts.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _mcts.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _mcts.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _mcts.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _mcts.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _mcts.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _mcts.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _mcts:
_mcts.SwigPyIterator_swigregister(SwigPyIterator)

class run_result(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _mcts.run_result_swiginit(self, _mcts.new_run_result(*args))
    first = property(_mcts.run_result_first_get, _mcts.run_result_first_set)
    second = property(_mcts.run_result_second_get, _mcts.run_result_second_set)
    def __len__(self):
        return 2
    def __repr__(self):
        return str((self.first, self.second))
    def __getitem__(self, index): 
        if not (index % 2):
            return self.first
        else:
            return self.second
    def __setitem__(self, index, val):
        if not (index % 2):
            self.first = val
        else:
            self.second = val
    __swig_destroy__ = _mcts.delete_run_result

# Register run_result in _mcts:
_mcts.run_result_swigregister(run_result)

NORMAL_MCTS = _mcts.NORMAL_MCTS
MAX_NODE = _mcts.MAX_NODE
AVG_NODE = _mcts.AVG_NODE
PARALLEL_TREES = _mcts.PARALLEL_TREES
NO_HEURISTIC = _mcts.NO_HEURISTIC
HEURISTIC_SELECT = _mcts.HEURISTIC_SELECT
FULL_EXPAND = _mcts.FULL_EXPAND
SQUARE_RATIO = _mcts.SQUARE_RATIO
FRAME_HEURISTIC = _mcts.FRAME_HEURISTIC
TOTAL_PLANT_COST_HEURISTIC = _mcts.TOTAL_PLANT_COST_HEURISTIC
TOTAL_ZOMBIE_HP_HEURISTIC = _mcts.TOTAL_ZOMBIE_HP_HEURISTIC
ZOMBIES_LEFT_TO_SPAWN_HEURISTIC = _mcts.ZOMBIES_LEFT_TO_SPAWN_HEURISTIC
EXPAND_BATCH = _mcts.EXPAND_BATCH
class Node(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    simulations = property(_mcts.Node_simulations_get, _mcts.Node_simulations_set)
    wins = property(_mcts.Node_wins_get, _mcts.Node_wins_set)
    terminal = property(_mcts.Node_terminal_get, _mcts.Node_terminal_set)
    parent = property(_mcts.Node_parent_get, _mcts.Node_parent_set)
    action = property(_mcts.Node_action_get, _mcts.Node_action_set)
    children = property(_mcts.Node_children_get, _mcts.Node_children_set)
    available_actions = property(_mcts.Node_available_actions_get, _mcts.Node_available_actions_set)

    def ucb(self):
        return _mcts.Node_ucb(self)

    def __init__(self, parent, action):
        _mcts.Node_swiginit(self, _mcts.new_Node(parent, action))
    __swig_destroy__ = _mcts.delete_Node

# Register Node in _mcts:
_mcts.Node_swigregister(Node)
cvar = _mcts.cvar


def select(root, cloned_level, use_heuristic=False):
    return _mcts.select(root, cloned_level, use_heuristic)

def expand(selected_node, cloned_level):
    return _mcts.expand(selected_node, cloned_level)

def rollout(selected_node, cloned_level):
    return _mcts.rollout(selected_node, cloned_level)

def backpropagate(start_node):
    return _mcts.backpropagate(start_node)

def select_best_action(root):
    return _mcts.select_best_action(root)

def run(level, timeout_ms, simulations_per_leaf, debug=False, ucb_const=1.4, mode=0, heuristic_mode=0, selection_type=0, loss_heuristic=0):
    return _mcts.run(level, timeout_ms, simulations_per_leaf, debug, ucb_const, mode, heuristic_mode, selection_type, loss_heuristic)

def _parallel_trees_run(level, timeout_ms, num_trees, debug, heurisic_mode):
    return _mcts._parallel_trees_run(level, timeout_ms, num_trees, debug, heurisic_mode)

def heuristic_basic_sunflowers(level, action):
    return _mcts.heuristic_basic_sunflowers(level, action)

def heuristic2(level):
    return _mcts.heuristic2(level)


