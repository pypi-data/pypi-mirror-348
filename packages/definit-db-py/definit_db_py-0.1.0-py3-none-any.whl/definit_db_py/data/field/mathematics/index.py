from definit_db_py.data.field.mathematics.definitions.algorithm.algorithm import ALGORITHM
from definit_db_py.data.field.mathematics.definitions.foundamental.finite_sequence import FINITE_SEQUENCE
from definit_db_py.data.field.mathematics.definitions.foundamental.finite_set import FINITE_SET
from definit_db_py.data.field.mathematics.definitions.foundamental.function import FUNCTION
from definit_db_py.data.field.mathematics.definitions.foundamental.hash_function import HASH_FUNCTION
from definit_db_py.data.field.mathematics.definitions.foundamental.information import INFORMATION
from definit_db_py.data.field.mathematics.definitions.foundamental.instruction import INSTRUCTION
from definit_db_py.data.field.mathematics.definitions.foundamental.multiset import MULTISET
from definit_db_py.data.field.mathematics.definitions.foundamental.notations.label import LABEL
from definit_db_py.data.field.mathematics.definitions.foundamental.object import OBJECT
from definit_db_py.data.field.mathematics.definitions.foundamental.operation import OPERATION
from definit_db_py.data.field.mathematics.definitions.foundamental.relation import RELATION
from definit_db_py.data.field.mathematics.definitions.foundamental.sequence import SEQUENCE
from definit_db_py.data.field.mathematics.definitions.foundamental.set import SET
from definit_db_py.data.field.mathematics.definitions.graph.adjacency_list import ADJACENCY_LIST
from definit_db_py.data.field.mathematics.definitions.graph.bipartite_graph import BIPARTITE_GRAPH
from definit_db_py.data.field.mathematics.definitions.graph.cycle import CYCLE
from definit_db_py.data.field.mathematics.definitions.graph.directed_acyclic_graph import DIRECTED_ACYCLIC_GRAPH
from definit_db_py.data.field.mathematics.definitions.graph.directed_graph import DIRECTED_GRAPH
from definit_db_py.data.field.mathematics.definitions.graph.edge import EDGE
from definit_db_py.data.field.mathematics.definitions.graph.graph import GRAPH
from definit_db_py.data.field.mathematics.definitions.graph.graph_distance import GRAPH_DISTANCE
from definit_db_py.data.field.mathematics.definitions.graph.node import NODE
from definit_db_py.data.field.mathematics.definitions.graph.path import PATH
from definit_db_py.data.field.mathematics.definitions.graph.tree.avl_tree import AVL_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.b_tree import B_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.balanced_binary_tree import BALANCED_BINARY_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.binary_search_tree import BINARY_SEARCH_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.binary_tree import BINARY_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.complete_binary_tree import COMPLETE_BINARY_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.interval_tree import INTERVAL_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.k_ary_tree import K_ARY_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.leaf import LEAF
from definit_db_py.data.field.mathematics.definitions.graph.tree.minimum_spanning_tree import MINIMUM_SPANNING_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.red_black_tree import RED_BLACK_TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.subtree import SUBTREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.tree import TREE
from definit_db_py.data.field.mathematics.definitions.graph.tree.unbalanced_binary_tree import UNBALANCED_BINARY_TREE
from definit_db_py.data.field.mathematics.definitions.problem.criterion import CRITERION
from definit_db_py.data.field.mathematics.definitions.problem.optimal_solution import OPTIMAL_SOLUTION
from definit_db_py.data.field.mathematics.definitions.problem.optimal_substructure import OPTIMAL_SUBSTRUCTURE
from definit_db_py.data.field.mathematics.definitions.problem.problem import PROBLEM
from definit_db_py.data.field.mathematics.definitions.problem.solution import SOLUTION
from definit_db_py.data.field.mathematics.definitions.problem.subproblem import SUBPROBLEM
from definit_db_py.definition.definition import Definition

field_index: list[Definition] = [
    OBJECT,
    INFORMATION,
    SEQUENCE,
    FINITE_SEQUENCE,
    INSTRUCTION,
    OPERATION,
    RELATION,
    SET,
    FINITE_SET,
    FUNCTION,
    HASH_FUNCTION,
    MULTISET,
    LABEL,
    PROBLEM,
    CRITERION,
    OPTIMAL_SOLUTION,
    OPTIMAL_SUBSTRUCTURE,
    SOLUTION,
    SUBPROBLEM,
    ALGORITHM,
    GRAPH,
    NODE,
    EDGE,
    ADJACENCY_LIST,
    BIPARTITE_GRAPH,
    CYCLE,
    DIRECTED_ACYCLIC_GRAPH,
    DIRECTED_GRAPH,
    GRAPH_DISTANCE,
    PATH,
    AVL_TREE,
    B_TREE,
    BALANCED_BINARY_TREE,
    BINARY_SEARCH_TREE,
    BINARY_TREE,
    COMPLETE_BINARY_TREE,
    INTERVAL_TREE,
    K_ARY_TREE,
    LEAF,
    MINIMUM_SPANNING_TREE,
    RED_BLACK_TREE,
    SUBTREE,
    TREE,
    UNBALANCED_BINARY_TREE,
]
