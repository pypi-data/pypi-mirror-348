from CDG import *
from Report import *
from StaticCheck import SignalType
from AST import *
import sys
from tqdm import tqdm

sys.setrecursionlimit(5000)


class Detector:
    def __init__(self, graphs):
        self.graphs = graphs
        self.reports = {}
        self.as_const = {}

    def detect(self):
        for graph in self.graphs.values():
            self.reports[graph.name] = {}
            print(
                f"[Info]       Starting the analysis process of graph {graph.name}.")

            print("[Info]       Detecting unconstrainted output...")
            self.detect_unconstrainted_output(graph)

            print("[Info]       Detecting unconstrained component input...")
            self.detect_unconstrained_comp_input(graph)

            print("[Info]       Detecting data flow constraint discrepancy...")
            self.detect_data_flow_constraint_discrepancy(graph)

            print("[Info]       Detecting unused component output...")
            self.detect_unused_comp_output(graph)

            print("[Info]       Detecting type mismatch...")
            self.detect_type_mismatch(graph)

            print("[Info]       Detecting assignment misuse...")
            self.detect_assignment_misue(graph)

            print("[Info]       Detecting unused signals...")
            self.detect_unused_signal(graph)

            print("[Info]       Detecting divide by zero unsafe...")
            self.detect_divide_by_zero_unsafe(graph)

            print("[Info]       Detecting nondeterministic data flow...")
            self.detect_nondeterministic_data_flow(graph)
        return self.reports

    def detect_unconstrainted_output(self, graph):
        results = []
        for n_id in tqdm(graph.components[graph.name][SignalType.OUTPUT]):
            node = graph.nodes[n_id]
            if self.unconstrainted_ouput(graph, node):
                results.append(Report(ReportType.WARNING, node.locate,
                               f"Output signal '{node.id}' is not constrained by any constraint."))
        self.reports[graph.name]["unconstrained_output"] = results

    def unconstrainted_ouput(self, graph, node):
        if not node.is_signal_out():
            return False
        constrainted_by_input = self.constrainted_by_input(graph, node)
        constrainted_as_const = self.constrainted_as_const(graph, node)
        return not (constrainted_by_input or constrainted_as_const)

    def constrainted_by_input(self, graph, node):
        for n1 in graph.nodes.values():
            if not n1.is_signal_in():
                continue
            if self.is_constrainted(graph, node, n1):
                return True
        return False

    def constrainted_as_const(self, graph, node):
        if node.id in self.as_const:
            return self.as_const[node.id]
        else:
            self.as_const[node.id] = False
        for edge in node.flow_to:
            if edge.edge_type == EdgeType.CONSTRAINT:
                if edge.node_to.node_type == NodeType.CONSTANT:
                    self.as_const[node.id] = True
                    return True
        for edge in node.flow_from:
            if edge.edge_type == EdgeType.CONSTRAINT:
                node_from = edge.node_from
                if node_from.node_type == NodeType.CONSTANT:
                    self.as_const[node.id] = True
                    return True
                if node_from.node_type == NodeType.SIGNAL and node_from.signal_type == SignalType.INTERMEDIATE:
                    if self.constrainted_as_const(graph, node_from):
                        self.as_const[node.id] = True
                        return True
        self.as_const[node.id] = False
        return False

    def is_constrainted(self, graph, node_a, node_b):
        return graph.has_path_constraint(node_a, node_b)

    def is_depended(self, graph, node_a, node_b):
        if node_a.id not in graph.node_flows_to:
            return False
        return node_b.id in graph.node_flows_to[node_a.id]

    def unconstrained_comp_input(self, graph, node):
        component = node.component.split("|")[0]
        if graph.name == component or not node.is_signal_in():
            return False
        for edge in node.flow_from:
            if edge.edge_type == EdgeType.CONSTRAINT:
                node_from = edge.node_from
                node_from_var_name = node_from.id.split(".")[0]
                node_var_name = node.id.split(".")[0]
                if node_from_var_name != node_var_name:
                    return False
        for edge in node.flow_to:
            if edge.edge_type == EdgeType.CONSTRAINT:
                node_to = edge.node_to
                node_to_var_name = node_to.id.split(".")[0]
                node_var_name = node.id.split(".")[0]
                if node_to_var_name != node_var_name:
                    return False
            if edge.node_to.node_type == NodeType.CONSTANT:
                node_to = edge.node_to
                for e1 in node_to.flow_to:
                    if e1.edge_type == EdgeType.CONSTRAINT:
                        return False
                for e1 in node_to.flow_from:
                    if e1.edge_type == EdgeType.CONSTRAINT:
                        return False
        return True

    def detect_unconstrained_comp_input(self, graph):
        results = []
        for node in tqdm(graph.nodes.values()):
            if self.unconstrained_comp_input(graph, node):
                results.append(Report(ReportType.WARNING, node.locate,
                               f"Input signal '{node.id}' is unconstrained and may accept unchecked values."))
        self.reports[graph.name]["unconstrained component input"] = results

    def detect_data_flow_constraint_discrepancy(self, graph):
        resutlts = []
        for n_id, n_set in tqdm(graph.node_flows_to.items()):
            for n1_id in n_set:
                node = graph.nodes[n_id]
                node_1 = graph.nodes[n1_id]
                if not self.is_constrainted(graph, node, node_1):
                    resutlts.append(Report(ReportType.WARNING, node_1.locate,
                                    f"Signal '{node_1.id}' depends on '{node.id}' via dataflow, but there is no corresponding constraint dependency."))
        self.reports[graph.name]["data flow constraint discrepancy"] = resutlts

    def is_checking_signal(self, node):
        for edge in node.flow_to:
            if edge.edge_type == EdgeType.DEPEND:
                return True
        return False

    def unused_comp_output(self, graph, node):
        component = node.component.split("|")[0]
        if not node.is_signal_out() or component == graph.name:
            return False
        sub_graph = self.graphs[component]
        node_var_name, signal_name = node.id.split(".")
        if signal_name not in sub_graph.nodes:
            return False
        sub_o_node = sub_graph.nodes[signal_name]
        if self.is_checking_signal(sub_o_node):
            return False
        for edge in node.flow_to:
            node_to_var_name = edge.node_to.id.split(".")[0]
            if node_var_name != node_to_var_name:
                return False
        for edge in node.flow_from:
            node_from_var_name = edge.node_from.id.split(".")[0]
            if node_var_name != node_from_var_name:
                return False
        return True

    def detect_unused_comp_output(self, graph):
        resuluts = []
        for node in tqdm(graph.nodes.values()):
            if self.unused_comp_output(graph, node):
                resuluts.append(Report(ReportType.WARNING, node.locate,
                                f"This output '{node.id}' is not checked nor used from the call site."))
        self.reports[graph.name]["unused component output"] = resuluts

    def unsused_signal(self, graph, node):
        component = node.component.split("|")[0]
        if node.is_signal_out() and component == graph.name:
            return False
        if node.node_type == NodeType.CONSTANT:
            return False
        return (len(node.flow_from) + len(node.flow_to)) == 0

    def detect_unused_signal(self, graph):
        results = []
        for node in tqdm(graph.nodes.values()):
            if self.unsused_signal(graph, node):
                results.append(Report(ReportType.WARNING, node.locate,
                               f"This signal '{node.id}' is declared but never used in any computation or constraint."))
        self.reports[graph.name]["unused signal"] = results

    def detect_type_mismatch(self, graph):
        num2bits_required = {"LessThan", "LessEqThan",
                             "GreaterThan", "GreaterEqThan", "BigLessThan"}
        num2bits_like = {"Num2Bits", "Num2Bits_strict",
                         "RangeProof", "MultiRangeProof", "RangeCheck2D"}
        results = []
        for node in tqdm(graph.nodes.values()):
            component = node.component.split("|")[0]
            if not node.is_signal_in() or component == graph.name:
                continue
            template_name = component.split("@")[0]
            if template_name not in num2bits_required:
                continue
            input_nodes = []
            for edge in node.flow_from:
                if edge.edge_type == EdgeType.CONSTRAINT:
                    continue
                if edge.node_from.is_signal():
                    input_nodes.append(edge.node_from)
                if edge.node_from.node_type == NodeType.CONSTANT:
                    for e1 in edge.node_from.flow_from:
                        if e1.edge_type == EdgeType.DEPEND and e1.node_from.is_signal():
                            input_nodes.append(e1.node_from)
            for n1 in input_nodes:
                is_checked = False
                flows_to = graph.flows_to(n1)
                for n2_id in flows_to:
                    n2 = graph.nodes[n2_id]
                    n2_comp = n2.component.split("|")[0]
                    if not n1.is_signal_in() or n2_comp == graph.name:
                        continue
                    template_name_n2 = n2_comp.split("@")[0]
                    if template_name_n2 in num2bits_like:
                        is_checked = True
                        break
                if not is_checked:
                    results.append(Report(ReportType.WARNING, node.locate,
                                   f"Signal '{n1.id}' flows into '{template_name}' without being properly range-checked."))
        self.reports[graph.name]["type mismatch"] = results

    def is_trivial_instruction(self, ast):
        if isinstance(ast, Variable) or isinstance(ast, Number):
            return True
        elif isinstance(ast, PrefixOp):
            return self.is_trivial_instruction(ast.rhe)
        elif isinstance(ast, InfixOp):
            return self.is_trivial_instruction(ast.lhe) and self.is_trivial_instruction(ast.rhe)
        else:
            return False

    def is_rewritable_assignment(self, edge):
        if edge.edge_type != EdgeType.DEPEND or edge.ast is None:
            return False
        node_from = edge.node_from
        node_to = edge.node_to
        for e1 in node_from.flow_to:
            if e1.node_to.id == node_to.id and e1.edge_type == EdgeType.CONSTRAINT:
                return False
        for e1 in node_from.flow_from:
            if e1.node_from.id == node_to.id and e1.edge_type == EdgeType.CONSTRAINT:
                return False
        if node_to.node_type == NodeType.CONSTANT:
            return False
        if node_from.node_type != NodeType.CONSTANT:
            return True
        return self.is_trivial_instruction(edge.ast.rhe)

    def detect_assignment_misue(self, graph):
        results = []
        for edge in tqdm(graph.edges.values()):
            if self.is_rewritable_assignment(edge):
                op = edge.ast.op
                if op == "<--":
                    instead_op = "<=="
                else:
                    instead_op = "==>"
                results.append(Report(ReportType.WARNING, edge.ast.locate,
                               f"Variable {edge.ast.var} is assigned using {op} instead of {instead_op}."))
        self.reports[graph.name]["assignment missue"] = results

    def flat_expr(self, graph, expr):
        if isinstance(expr, Variable):
            name = expr.name
            for node in graph.nodes.values():
                if name in node.id and node.is_signal():
                    return True
        elif isinstance(expr, InfixOp):
            return self.flat_expr(graph, expr.lhe) or self.flat_expr(graph, expr.rhe)
        elif isinstance(expr, PrefixOp):
            return self.flat_expr(graph, expr.rhe)
        elif isinstance(expr, InlineSwitchOp):
            return self.flat_expr(graph, expr.cond) or self.flat_expr(graph, expr.if_true) or self.flat_expr(graph, expr.if_false)
        elif isinstance(expr, Call):
            for arg in expr.args:
                if self.flat_expr(graph, arg):
                    return True
        return False

    def is_denominator_with_signal(self, graph, expr):
        if isinstance(expr, InfixOp):
            if expr.infix_op == "/":
                if self.flat_expr(graph, expr.rhe):
                    return True
            if self.is_denominator_with_signal(graph, expr.lhe) or self.is_denominator_with_signal(graph, expr.rhe):
                return True
        elif isinstance(expr, InlineSwitchOp):
            return self.is_denominator_with_signal(graph, expr.cond) or self.is_denominator_with_signal(graph, expr.if_true) or self.is_denominator_with_signal(graph, expr.if_false)
        return False

    def detect_divide_by_zero_unsafe(self, graph):
        results = []
        for edge in tqdm(graph.edges.values()):
            if edge.ast and self.is_denominator_with_signal(graph, edge.ast.rhe):
                results.append(Report(ReportType.WARNING, edge.ast.locate,
                               f"Potential divide-by-zero issue detected."))
        self.reports[graph.name]["divide by zero"] = results

    def is_branch_cond_with_signal(self, graph, expr):
        if isinstance(expr, InfixOp):
            if self.is_branch_cond_with_signal(graph, expr.lhe) or self.is_branch_cond_with_signal(graph, expr.rhe):
                return True
        elif isinstance(expr, InlineSwitchOp):
            return self.flat_expr(graph, expr.cond)
        return False

    def detect_nondeterministic_data_flow(self, graph):
        results = []
        for edge in tqdm(graph.edges.values()):
            if edge.ast and self.is_branch_cond_with_signal(graph, edge.ast.rhe):
                results.append(Report(ReportType.WARNING, edge.ast.locate,
                                      "Potential non-deterministic dataflow: conditional assignment depends on a signal."))
        self.reports[graph.name]["nondeterministic data flow"] = results
