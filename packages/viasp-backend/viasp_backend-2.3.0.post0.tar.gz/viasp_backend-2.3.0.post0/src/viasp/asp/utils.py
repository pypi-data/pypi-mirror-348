"""Mostly graph utility functions."""
import networkx as nx
from clingo import Symbol, ast
from clingo.ast import ASTType, AST, Transformer, ASTSequence
from typing import Callable, List, Sequence, Collection, Tuple, Dict, Set, FrozenSet, Optional
import re

from ..shared.simple_logging import warn
from ..shared.model import Node, SymbolIdentifier, Transformation, RuleContainer
from ..shared.util import pairwise, get_root_node_from_graph, RuleType

def is_constraint(rule: RuleType) -> bool:
    return rule.ast_type == ASTType.Rule and "atom" in rule.head.child_keys and rule.head.atom.ast_type == ASTType.BooleanConstant  # type: ignore

def is_minimize(rule: RuleType) -> bool:
    return rule.ast_type == ASTType.Minimize  # type: ignore

def merge_constraints(g: nx.DiGraph) -> nx.DiGraph:
    mapping = {}
    constraints = set([
        ruleset for ruleset in g.nodes for rule in ruleset.ast
        if is_constraint(rule)
    ])
    if constraints:
        merge_node = merge_rule_container(constraints)
        mapping = {c: merge_node for c in constraints}
    return nx.relabel_nodes(g, mapping)


def merge_cycles(g: nx.DiGraph) -> Tuple[nx.DiGraph, FrozenSet[RuleContainer]]:
    mapping: Dict[AST, AST] = {}
    merge_node: RuleContainer
    where_recursion_happens = set()
    for cycle in nx.algorithms.components.strongly_connected_components(g):
        merge_node = merge_rule_container(cycle)
        mapping.update({old_node: merge_node for old_node in cycle})
    # which nodes were merged
    for k, v in mapping.items():
        if k != v:
            where_recursion_happens.add(merge_node)
    return nx.relabel_nodes(g, mapping), frozenset(where_recursion_happens)


def merge_rule_container(set: Collection[RuleContainer]) -> RuleContainer:
    ast = []
    str_ = []
    for rule_container in set:
        ast.extend(rule_container.ast)
        str_.extend(rule_container.str_)
    return RuleContainer(ast=tuple(ast), str_=tuple(str_))


def remove_loops(g: nx.DiGraph) -> Tuple[nx.DiGraph, FrozenSet[RuleContainer]]:
    remove_edges: List[Tuple[AST, AST]] = []
    where_recursion_happens: Set[RuleContainer] = set()
    for edge in g.edges:
        u, v = edge
        if u == v:
            remove_edges.append(edge)
            # info on which node's loop is removed
            where_recursion_happens.add(u)

    for edge in remove_edges:
        g.remove_edge(*edge)
    return g, frozenset(where_recursion_happens)

def move_constraints_only_transformations_to_end(sorted_program: List[RuleContainer]) -> None:
    constraints_only_rules = set()
    for rc in sorted_program:
        if all(is_constraint(r) for r in rc.ast):
            sorted_program.remove(rc)
            constraints_only_rules.add(rc)
    for constraint_rule in constraints_only_rules:
        sorted_program.append(constraint_rule)


def insert_atoms_into_nodes(path: List[Node]) -> None:
    if not path:
        return
    facts = path[0]
    state = set(facts.diff)
    facts.atoms = frozenset(state)
    state = set(map(SymbolIdentifier, (s.symbol for s in state)))
    for u, v in pairwise(path):
        state.update(v.diff)
        state.update(u.diff)
        v.atoms = frozenset(state)
        state = set(map(SymbolIdentifier, (s.symbol for s in state)))


def identify_reasons(g: nx.DiGraph) -> None:
    """
    Identify the reasons for each symbol in the graph.
    Takes the Symbol from node.reason and overwrites the values of the Dict node.reason
    with the SymbolIdentifier of the corresponding symbol.

    :param g: The graph to identify the reasons for.
    """
    # get fact node:
    root_node = get_root_node_from_graph(g)

    # go through entire graph, starting at root_node and traveling down the graph via successors
    children_next = set()
    searched_nodes = set()
    children_current = [root_node]
    while len(children_current) != 0:
        for v in children_current:
            for new, rr in v.reason.items():
                tmp_reason = []
                for r in rr:
                    tmp_reason.append(get_identifiable_reason(g, v, r))
                v.reason[str(new)] = tmp_reason
            for node in v.recursive:
                for new, rr in node.reason.items():
                    tmp_reason = []
                    for r in rr:
                        tmp_reason.append(
                            get_identifiable_reason_of_recursive_subnode(v.recursive,
                                                    node,
                                                    r,
                                                    g,
                                                    v))
                    node.reason[str(new)] = tmp_reason
            for s in v.diff:
                if str(s.symbol) in v.reason.keys() and len(v.reason[str(
                        s.symbol)]) > 0:
                    s.has_reason = True
            searched_nodes.add(v)
            for w in g.successors(v):
                children_next.add(w)
            children_next = children_next.difference(searched_nodes)
        children_current = list(children_next)


def get_identifiable_reason(g: nx.DiGraph,
                            v: Node,
                            r: Symbol,
                            super_graph=None,
                            super_node=None) -> Optional[SymbolIdentifier]:
    """
    Returns the SymbolIdentifier that is the reason for the given Symbol r.
    If the reason is not in the node, it returns recursively calls itself with the predecessor.


    :param g: The graph that contains the nodes
    :param v: The node that contains the symbol r
    :param r: The symbol that is the reason
    """
    if (r in v.diff): return next(s for s in v.atoms if s == r)
    if (g.in_degree(v) != 0):
        for u in g.predecessors(v):
            return get_identifiable_reason(g,
                                           u,
                                           r,
                                           super_graph=super_graph,
                                           super_node=super_node)
    if (super_graph != None and super_node != None):
        return get_identifiable_reason(super_graph, super_node, r)

    # stop criterion: v is the root node and there is no super_graph
    warn(f"An explanation could not be made")
    return None

def get_identifiable_reason_of_recursive_subnode(recursive_subgraph: List[Node],
                                                 v: Node,
                                                 r: Symbol,
                                                 super_graph,
                                                 super_node) -> Optional[SymbolIdentifier]:
    if (r in v.diff): return next(s for s in v.atoms if s == r)
    if (recursive_subgraph.index(v) != 0):
        return get_identifiable_reason_of_recursive_subnode(recursive_subgraph,
                                                            recursive_subgraph[recursive_subgraph.index(v)-1],
                                                            r,
                                                            super_graph,
                                                            super_node)
    if (super_graph != None and super_node != None):
        return get_identifiable_reason(super_graph, super_node, r)

    # stop criterion: v is the root node and there is no super_graph
    warn(f"An explanation could not be made")
    return None

def calculate_spacing_factor(g: nx.DiGraph) -> None:
    """
    Calculate the spacing factor for each node the graph.
    This will make sure the branches of the graph are spaced out evenly.

    :param g: The graph.
    """
    # get fact node:
    root_node = get_root_node_from_graph(g)

    # go through entire graph, starting at root_node and traveling down the graph via successors
    children_next = []
    searched_nodes = set()
    children_current = [root_node]
    while len(children_current) != 0:
        for v in children_current:
            successors: List[Node] = list(g.successors(v))
            if len(successors) != 0:
                for w in successors:
                    w.space_multiplier = v.space_multiplier / len(successors)

            searched_nodes.add(v)
            for w in g.successors(v):
                children_next.append(w)
        children_current = children_next
        children_next = []


def topological_sort(g: nx.DiGraph, rules: Sequence[ast.Rule]) -> List:  # type: ignore
    """ Topological sort of the graph.
        If the order is ambiguous, prefer the order of the rules.
        Note: Rule = Node

        :param g: Graph
        :param rules: List of Rules
    """
    sorted: List = []  # L list of the sorted elements
    no_incoming_edge = set()  # set of all nodes with no incoming edges

    no_incoming_edge.update(
        [node for node in g.nodes if g.in_degree(node) == 0])
    while len(no_incoming_edge):
        earliest_node_index = len(rules)
        earliest_node = None
        for node in no_incoming_edge:
            for rule in node.ast:
                node_index = rules.index(rule)
                if node_index < earliest_node_index:
                    earliest_node_index = node_index
                    earliest_node = node

        no_incoming_edge.remove(earliest_node)
        sorted.append(earliest_node)

        # update graph
        for node in list(g.successors(earliest_node)):
            g.remove_edge(earliest_node, node)
            if g.in_degree(node) == 0:
                no_incoming_edge.add(node)

    if len(g.edges):
        warn("Could not sort the graph.")
        raise Exception("Could not sort the graph.")
    return sorted


def find_index_mapping_for_adjacent_topological_sorts(
    g: nx.DiGraph,
    sorted_program: List[RuleContainer]) -> Dict[int, Dict[str, int]]:
    new_indices: Dict[int, Dict[str, int]] = {}
    for i, rule_container in enumerate(sorted_program):
        lower_bound = max([sorted_program.index(u) for u in g.predecessors(rule_container)]+[-1])
        upper_bound = min([sorted_program.index(u) for u in g.successors(rule_container)]+[len(sorted_program)])
        new_indices[i] = {"lower_bound": lower_bound+1, "upper_bound": upper_bound-1}
    return new_indices


def recalculate_transformation_ids(sort: List[Transformation]):
    for i, transformation in enumerate(sort):
        transformation.id = i


def filter_body_aggregates(element: AST):
    aggregate_types = [
        ASTType.Aggregate, ASTType.BodyAggregate, ASTType.ConditionalLiteral
    ]
    if (element.ast_type in aggregate_types):
        return False
    if (getattr(getattr(element, "atom", None), "ast_type", None)
            in aggregate_types):
        return False
    return True

class VariableConflictResolver(Transformer):

    def __init__(self, *args, **kwargs):
        self.counter = 1
        self.conflict_free_anon_str = kwargs.get("conflict_free_anon_str",
                                                 "_A")

    def visit_Variable(self, variable: ast.Variable, **kwargs) -> None:  # type: ignore
        if variable.name == "_":
            variable.name = self.conflict_free_anon_str + str(self.counter)
            self.counter += 1
        return variable.update(**self.visit_children(variable, **kwargs))

class FindConflictFreeAnonVariableName(Transformer):

    def __init__(self, *args, **kwargs):
        self.names = set()

    def visit_Variable(self, variable: ast.Variable, **kwargs) -> None:  # type: ignore
        self.names.add(variable.name)
        return variable.update(**self.visit_children(variable, **kwargs))

    def get_conflict_free_anon_replacement(self) -> str:
        """
        Get a conflict free variable name.
        """
        sentinel = -1
        for i in range(100):
            name = "_"* i + "_A"
            search = re.compile(fr"^{name}(\d+)$")
            if next(filter(search.match, self.names), sentinel) is sentinel:
                return name
        raise ValueError("Could not find a conflict free variable name")


def replace_anon_variables(
        literals: ASTSequence,
        context: AST) -> None:
    name_finder = FindConflictFreeAnonVariableName()
    name_finder.visit(context)
    conflict_free_anon_str = name_finder.get_conflict_free_anon_replacement()

    visitor = VariableConflictResolver(
        conflict_free_anon_str=conflict_free_anon_str)
    visitor.visit_sequence(literals)
