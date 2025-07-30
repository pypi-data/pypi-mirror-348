# Directed Edge Geography

from typing import Dict
from networkx import DiGraph, descendants
from generalized_geography.common.constants import LOSE, WIN
from generalized_geography.common.types import NodeValue
from generalized_geography.common.unlabeled_multidigraph import UnlabeledMultiDiGraph
from generalized_geography.solver.RDG import RDGSolver


class DEGSolver(RDGSolver):
    graph: UnlabeledMultiDiGraph
    winlose: Dict[NodeValue, int]

    def __init__(self, graph: UnlabeledMultiDiGraph):
        super().__init__(graph)
        self.classify_winlose_involving_2_cycles()

    def remove_2_cycles(self, verbose=0):

        if verbose == 1:
            print("Remove 2 cycles : ", end="")

        to_remove = []

        # self loop 짝수 개 검출
        for node in self.graph.nodes:
            m = self.graph.get_multiplicity(node, node)
            to_remove.append((node, node, m - m % 2))

        # (a,b), (b,a) 꼴 엣지 검출
        for u, v in [(u, v) for u, v in self.graph.edges if u > v]:
            if self.graph.has_edge(v, u):
                delete_num = min(self.graph.get_multiplicity(u, v),
                                 self.graph.get_multiplicity(v, u))
                to_remove.extend([(u, v, delete_num), (v, u, delete_num)])

        self.graph.decrease_edges_from(to_remove)

        if verbose == 1:
            print(sum([m for _, _, m in to_remove]), "edges removed")

    def classify_winlose_involving_1_cycles(self, verbose=0, lose_sinks=None, win_sinks=None):

        if verbose == 1:
            print("Classify loop winlose : ", end="")

        # outedge가 없는 노드들
        if not lose_sinks:
            lose_sinks = [node for node,
                          deg in self.graph.out_degree() if deg == 0]
        # outedge가 loop edge 하나뿐인 노드들
        if not win_sinks:
            win_sinks = [node for node, deg in self.graph.out_degree(
            ) if deg == 1 and self.graph.has_edge(node, node)]

        for n in lose_sinks:
            self.winlose[n] = LOSE
        for n in win_sinks:
            self.winlose[n] = WIN

        sinks = lose_sinks + win_sinks

        while sinks:
            node = sinks.pop()
            if self.winlose[node] == LOSE:
                preds = [pred for pred in self.graph.predecessors(
                    node) if pred not in self.winlose]
                self.graph.remove_node(node)
                for pred in preds:
                    self.winlose[pred] = WIN
                    sinks.append(pred)

            else:
                preds = [pred for pred in self.graph.predecessors(
                    node) if pred not in self.winlose]
                self.graph.remove_node(node)
                for pred in preds:
                    if self.graph.out_degree(pred) == 0:
                        self.winlose[pred] = LOSE
                        sinks.append(pred)
                    elif self.graph.out_degree(pred) == 1 and self.graph.get_multiplicity(pred, pred) == 1:
                        self.winlose[pred] = WIN
                        sinks.append(pred)

        if verbose == 1:
            win_nodes = [
                node for node in self.winlose if self.winlose[node] == WIN]
            lose_nodes = [
                node for node in self.winlose if self.winlose[node] == LOSE]
            print(len(win_nodes), "win,", len(lose_nodes),
                  "lose,", len(self.graph), "remain")

    def classify_winlose_involving_2_cycles(self, verbose=0):
        self.classify_repetitive_winlose(verbose)
        self.remove_2_cycles(verbose)
        self.classify_winlose_involving_1_cycles(verbose)

    def is_win_dfs(self, node):

        if node in self.winlose:
            if self.winlose[node] == WIN:
                return True
            else:
                return False

        reachable_nodes = descendants(self.graph, node) | {node}
        subgraph: UnlabeledMultiDiGraph = self.graph.subgraph(reachable_nodes)
        subgraph_copy = UnlabeledMultiDiGraph(subgraph)
        for succ in self.graph.successors(node):

            subgraph_copy.decrease_edge(node, succ)

            if not DEGSolver(subgraph_copy).is_win_dfs(succ):
                return True
            subgraph_copy.increase_edge(node, succ)

        return False

    def completely_classify(self):
        new_winlose = {node: WIN if self.is_win_dfs(
            node) else LOSE for node in self.graph.nodes}
        self.winlose.update(new_winlose)


def get_critical_edges(graph: UnlabeledMultiDiGraph):
    result = []
    for node in graph.nodes:
        outdeg = graph.multi_out_degree(node)

        if outdeg == 1:
            result.append(list(graph.out_edges(node))[0])

        elif outdeg == 2:
            edges = list(graph.out_edges(node, data="multiplicity"))

            if len(edges) == 1:
                continue

            if edges[1] == node:
                result.append((edges[0][0], edges[0][1]))

            elif edges[0] == node:
                result.append((edges[1][0], edges[1][1]))

    return result


if __name__ == "__main__":
    g = UnlabeledMultiDiGraph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 1)

    solver = DEGSolver(g)
    solver.completely_classify()
    print(solver.winlose)
