from enum import Enum, auto
from StaticCheck import SignalType
from tqdm import tqdm


class NodeType(Enum):
    SIGNAL = auto()
    CONSTANT = auto()


class EdgeType(Enum):
    DEPEND = auto()
    CONSTRAINT = auto()


class Node:
    def __init__(self, locate, id, node_type, signal_type, component):
        self.locate = locate
        self.id = id
        self.node_type = node_type
        self.signal_type = signal_type
        self.component = component
        # node == edge.node_from
        self.flow_to = []
        # node = edge.node_to
        self.flow_from = []

    def __repr__(self):
        return f"Node({self.id})"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

    def is_signal(self):
        return self.node_type == NodeType.SIGNAL

    def is_signal_in(self):
        return self.is_signal() and self.signal_type == SignalType.INPUT

    def is_signal_out(self):
        return self.is_signal() and self.signal_type == SignalType.OUTPUT

    def is_signal_in_of(self, component):
        return self.is_signal_in() and self.component == component

    def is_signal_out_of(self, component):
        return self.is_signal_out() and self.component == component

    def is_signal_of(self, component):
        return self.is_signal() and self.component == component


class Edge:
    def __init__(self, node_from, node_to, edge_type, name, ast=None):
        self.node_from = node_from
        self.node_to = node_to
        self.edge_type = edge_type
        self.name = name
        self.ast = ast


def getEdgeName(edge_type, nFrom, nTo):
    if edge_type == EdgeType.DEPEND:
        return f"data:{nFrom.id}-{nTo.id}"
    else:
        return f"constraint:{nFrom.id}-{nTo.id}"


class CircuitDependenceGraph:
    def __init__(self, edges, nodes, name, components):
        self.edges = edges
        self.nodes = nodes
        self.name = name
        self.components = components
        self.node_flows_to = {}

    def is_signal(self, node):
        return node.node_type == NodeType.SIGNAL

    def is_signal_in(self, node):
        return self.is_signal(node) and node.signal_type == SignalType.INPUT

    def is_signal_out(self, node):
        return self.is_signal(node) and node.signal_type == SignalType.OUTPUT

    def is_signal_of(self, node, component):
        return self.is_signal(node) and node.component == component

    def is_signal_in_of(self, node, component):
        return self.is_signal_of(node, component) and self.is_signal_in(node)

    def is_signal_out_of(self, node, component):
        return self.is_signal_of(node, component) and self.is_signal_out(node)

    def has_path_depend(self, a: Node, b: Node) -> bool:
        visited = set()
        stack = [a]
        while stack:
            current = stack.pop()
            if current.id == b.id:
                return True
            if current.id in visited:
                continue
            visited.add(current.id)
            for edge in a.flow_to:
                if edge.edge_type == EdgeType.DEPEND:
                    stack.append(edge.node_to)
        return False

    def has_path_constraint(self, a: Node, b: Node) -> bool:
        visited = set()
        stack = [a]
        while stack:
            current = stack.pop()
            if current.id == b.id:
                return True
            if current.id in visited:
                continue
            visited.add(current.id)
            for edge in current.flow_to:
                if edge.edge_type == EdgeType.CONSTRAINT:
                    stack.append(edge.node_to)
        return False

    def build_conditional_depend_edges(self, graphs):
        print(
            f"[Info]       Building conditional dependency edges of {self.name}...")
        for u in tqdm(self.nodes.values()):
            if self.is_signal_in(u):
                component = u.component
                for v_id in self.components[component][SignalType.OUTPUT]:
                    v = self.nodes[v_id]
                    if self.has_path_depend(u, v):
                        edge_name = getEdgeName(EdgeType.DEPEND, u, v)
                        if edge_name not in self.edges:
                            edge = self.edges[edge_name] = Edge(
                                u, v, EdgeType.DEPEND, edge_name)
                            u.flow_to.append(edge)
                            v.flow_from.append(edge)
                    else:
                        graph_name = component.split("|")[0]
                        if graph_name != self.name:
                            graph = graphs[graph_name]
                            a_id = u.id.split(".")[1]
                            b_id = v_id.split(".")[1]
                            if a_id not in graph.nodes or b_id not in graph.nodes:
                                continue
                            node_a = graph.nodes[a_id]
                            node_b = graph.nodes[b_id]
                            if graph.has_path_depend(node_a, node_b):
                                edge_name = getEdgeName(EdgeType.DEPEND, u, v)
                                if edge_name not in self.edges:
                                    edge = self.edges[edge_name] = Edge(
                                        u, v, EdgeType.DEPEND, edge_name)
                                    u.flow_to.append(edge)
                                    v.flow_from.append(edge)

    def build_condition_constraint_edges(self, graphs):
        print(
            f"[Info]       Building condition constraint edges of {self.name}...")
        for u in tqdm(self.nodes.values()):
            if self.is_signal_in(u):
                component = u.component
                for v_id in self.components[component][SignalType.OUTPUT]:
                    v = self.nodes[v_id]
                    if self.has_path_constraint(u, v):
                        edge_name = getEdgeName(EdgeType.CONSTRAINT, u, v)
                        if edge_name not in self.edges:
                            edge = self.edges[edge_name] = Edge(
                                u, v, EdgeType.CONSTRAINT, edge_name)
                            u.flow_to.append(edge)
                            v.flow_from.append(edge)
                            edge_name_reversed = getEdgeName(
                                EdgeType.CONSTRAINT, v, u)
                            if edge_name_reversed not in self.edges:
                                edge = self.edges[edge_name] = Edge(
                                    v, u, EdgeType.CONSTRAINT, edge_name_reversed)
                                v.flow_to.append(edge)
                                u.flow_from.append(edge)
                    else:
                        graph_name = component.split("|")[0]
                        if graph_name != self.name:
                            graph = graphs[graph_name]
                            a_id = u.id.split(".")[1]
                            b_id = v_id.split(".")[1]
                            if a_id not in graph.nodes or b_id not in graph.nodes:
                                continue
                            node_a = graph.nodes[a_id]
                            node_b = graph.nodes[b_id]
                            if graph.has_path_constraint(node_a, node_b):
                                edge_name = getEdgeName(
                                    EdgeType.CONSTRAINT, u, v)
                                if edge_name not in self.edges:
                                    edge = self.edges[edge_name] = Edge(
                                        u, v, EdgeType.CONSTRAINT, edge_name)
                                    u.flow_to.append(edge)
                                    v.flow_from.append(edge)
                                    edge_name_reversed = getEdgeName(
                                        EdgeType.CONSTRAINT, v, u)
                                    if edge_name_reversed not in self.edges:
                                        edge = self.edges[edge_name] = Edge(
                                            v, u, EdgeType.CONSTRAINT, edge_name_reversed)
                                        v.flow_to.append(edge)
                                        u.flow_from.append(edge)

    def flows_to(self, node):
        if node.id in self.node_flows_to:
            return self.node_flows_to[node.id]
        flows_to_set = set()
        for edge in node.flow_to:
            if edge.edge_type == EdgeType.CONSTRAINT:
                continue
            node_to = edge.node_to
            if node_to.is_signal():
                flows_to_sub = self.flows_to(node_to)
                flows_to_set.union(flows_to_sub)
                flows_to_set.add(node_to.id)
            else:
                for e1 in node_to.flow_to:
                    if e1.edge_type == EdgeType.CONSTRAINT:
                        continue
                    to_1 = e1.node_to
                    if to_1.is_signal():
                        flows_to_sub = self.flows_to(to_1)
                        flows_to_set.union(flows_to_sub)
                        flows_to_set.add(to_1.id)
        self.node_flows_to[node.id] = flows_to_set
        return flows_to_set

    def compute(self):
        for node in self.nodes.values():
            if node.is_signal():
                self.flows_to(node)

    def build_graph(self, graphs):
        self.build_conditional_depend_edges(graphs)
        self.build_condition_constraint_edges(graphs)
        self.compute()
