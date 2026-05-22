#!/usr/bin/env python3
"""Compress CPAchecker violation witnesses by CFA dependency slicing."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

try:
    from pycparser import c_ast, c_parser
except ImportError:
    c_ast = None
    c_parser = None


IDENT_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
IF_RE = re.compile(r"\bif\s*\((.*)\)")
ASSIGN_RE = re.compile(r"^\s*(?:[A-Za-z_][\w\s\*]*\s+)?([A-Za-z_]\w*)\s*(?:[+\-*/%&|^]|<<|>>)?=")
CALL_RE = re.compile(r"\b([A-Za-z_]\w*)\s*\(")

KEYWORDS = {
    "auto",
    "break",
    "case",
    "char",
    "const",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extern",
    "float",
    "for",
    "goto",
    "if",
    "inline",
    "int",
    "long",
    "register",
    "restrict",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "typedef",
    "union",
    "unsigned",
    "void",
    "volatile",
    "while",
    "__attribute__",
    "__nothrow__",
    "__leaf__",
    "__noreturn__",
}


@dataclass
class CFAEdge:
    edge_id: int
    source: int
    target: int
    line: int
    text: str
    kind: str
    defs: set[str] = field(default_factory=set)
    uses: set[str] = field(default_factory=set)
    controls: list[int] = field(default_factory=list)
    calls: set[str] = field(default_factory=set)
    end_line: int | None = None
    terminates: bool = False
    loop_transfer: bool = False


@dataclass
class CFANode:
    node_id: int
    line: int
    function: str


@dataclass
class CFA:
    nodes: dict[int, CFANode]
    edges: list[CFAEdge]
    edge_by_line: dict[int, CFAEdge]
    functions: dict[str, int]
    control_dependents: dict[int, set[int]]
    branch_sides: dict[int, tuple[set[int], set[int]]] = field(default_factory=dict)
    loop_headers: set[int] = field(default_factory=set)


@dataclass
class WaypointSegment:
    lines: list[str]
    waypoint_type: str | None = None
    action: str | None = None
    line: int | None = None
    function: str | None = None


def strip_comments(line: str, in_block: bool) -> tuple[str, bool]:
    out = []
    i = 0
    while i < len(line):
        if in_block:
            end = line.find("*/", i)
            if end == -1:
                return "".join(out), True
            i = end + 2
            in_block = False
            continue
        if line.startswith("/*", i):
            in_block = True
            i += 2
            continue
        if line.startswith("//", i):
            break
        out.append(line[i])
        i += 1
    return "".join(out), in_block


def vars_in(expr: str) -> set[str]:
    expr = re.sub(r'"(?:\\.|[^"\\])*"', " ", expr)
    names = set(IDENT_RE.findall(expr))
    calls = set(CALL_RE.findall(expr))
    return {name for name in names - calls if name not in KEYWORDS}


class LineCParser:
    """Small generated-C parser that constructs a line-located CFA.

    It handles the subset used by CPAchecker witnesses here: functions, if
    branches, declarations, assignments, calls, and returns.  The CFA is
    explicit even though parsing is lightweight: each executable source item is
    an edge between two CFA nodes and carries DEF/USE/control metadata.
    """

    function_def_re = re.compile(r"^\s*(?:[A-Za-z_][\w\s\*]*\s+)+([A-Za-z_]\w*)\s*\([^;]*\)\s*\{")

    def __init__(self, path: Path):
        self.path = path
        self.lines = path.read_text(encoding="utf-8").splitlines()
        self.nodes: dict[int, CFANode] = {}
        self.edges: list[CFAEdge] = []
        self.edge_by_line: dict[int, CFAEdge] = {}
        self.functions: dict[str, int] = {}
        self.control_dependents: dict[int, set[int]] = {}
        self.branch_sides: dict[int, tuple[set[int], set[int]]] = {}
        self.loop_headers: set[int] = set()
        self.current_function = "<global>"
        self._next_node = 1
        self._next_edge = 1
        self._last_node: int | None = None

    def parse(self) -> CFA:
        control_stack: list[tuple[int, int]] = []
        pending_controls: list[int] = []
        in_block_comment = False
        depth = 0

        for lineno, raw in enumerate(self.lines, start=1):
            line, in_block_comment = strip_comments(raw, in_block_comment)
            stripped = line.strip()
            line_depth = depth

            while control_stack and control_stack[-1][1] >= line_depth:
                control_stack.pop()

            m_func = self.function_def_re.match(line)
            if m_func:
                self.current_function = m_func.group(1)
                self.functions[self.current_function] = lineno
                self._last_node = self._new_node(lineno)

            edge = self._parse_edge(lineno, stripped, [ctrl for ctrl, _ in control_stack])
            if edge:
                self.edges.append(edge)
                self.edge_by_line[lineno] = edge
                for ctrl in edge.controls:
                    self.control_dependents.setdefault(ctrl, set()).add(edge.line)
                if edge.kind == "branch":
                    pending_controls.append(edge.line)

            opens = line.count("{")
            closes = line.count("}")
            for _ in range(opens):
                depth += 1
                for ctrl_line in pending_controls:
                    control_stack.append((ctrl_line, depth))
                pending_controls.clear()
            depth -= closes

        for edge in self.edges:
            if edge.kind == "branch":
                deps = self.control_dependents.get(edge.line, set())
                edge.end_line = max(deps) if deps else edge.line

        return CFA(
            self.nodes,
            self.edges,
            self.edge_by_line,
            self.functions,
            self.control_dependents,
            self.branch_sides,
            self.loop_headers,
        )

    def _parse_edge(self, lineno: int, text: str, controls: list[int]) -> CFAEdge | None:
        if not text or text in {"{", "}"} or text.startswith("#"):
            return None
        if self.function_def_re.match(text):
            return None

        kind = "stmt"
        defs: set[str] = set()
        uses = vars_in(text)
        condition = self._if_condition(text)
        if condition is not None:
            kind = "branch"
            uses = vars_in(condition)
        elif text.startswith("return"):
            kind = "return"
        elif text.startswith("break"):
            kind = "break"
        elif text.startswith("continue"):
            kind = "continue"
        else:
            m_assign = ASSIGN_RE.match(text)
            if m_assign:
                lhs = m_assign.group(1)
                defs.add(lhs)
                uses.discard(lhs)
                if re.search(rf"\b{re.escape(lhs)}\s*(?:\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|\+\+|--)", text):
                    uses.add(lhs)

        calls = set(CALL_RE.findall(text)) - KEYWORDS
        source = self._last_node or self._new_node(lineno)
        target = self._new_node(lineno)
        self._last_node = target
        terminates = self._terminates(kind, text, calls)
        loop_transfer = kind in {"break", "continue"}
        edge = CFAEdge(
            self._next_edge,
            source,
            target,
            lineno,
            text,
            kind,
            defs,
            uses,
            controls,
            calls,
            None,
            terminates,
            loop_transfer,
        )
        self._next_edge += 1
        return edge

    def _new_node(self, line: int) -> int:
        node_id = self._next_node
        self._next_node += 1
        self.nodes[node_id] = CFANode(node_id, line, self.current_function)
        return node_id

    @staticmethod
    def _terminates(kind: str, text: str, calls: set[str]) -> bool:
        compact = re.sub(r"\s+", "", text)
        return (
            kind == "return"
            or bool(calls & {"exit", "abort"})
            or ("__VERIFIER_assume" in calls and compact.endswith("(0);"))
        )

    @staticmethod
    def _if_condition(text: str) -> str | None:
        start = text.find("if")
        if start == -1:
            return None
        open_paren = text.find("(", start)
        if open_paren == -1:
            return None
        depth = 0
        for idx in range(open_paren, len(text)):
            if text[idx] == "(":
                depth += 1
            elif text[idx] == ")":
                depth -= 1
                if depth == 0:
                    return text[open_paren + 1 : idx]
        return None


class ExprVars:
    def __init__(self) -> None:
        self.uses: set[str] = set()
        self.calls: set[str] = set()

    def collect(self, node: object | None) -> tuple[set[str], set[str]]:
        self.uses = set()
        self.calls = set()
        if node is not None:
            self._visit(node)
        return self.uses, self.calls

    def _visit(self, node: object | None) -> None:
        if node is None or c_ast is None:
            return
        if isinstance(node, c_ast.ID):
            self.uses.add(node.name)
            return
        if isinstance(node, c_ast.FuncCall):
            if isinstance(node.name, c_ast.ID):
                self.calls.add(node.name.name)
            self._visit(node.args)
            return
        for _, child in node.children():
            self._visit(child)


class PycparserCFAParser:
    def __init__(self, path: Path):
        self.path = path
        self.source_lines = path.read_text(encoding="utf-8").splitlines()
        self.nodes: dict[int, CFANode] = {}
        self.edges: list[CFAEdge] = []
        self.edge_by_line: dict[int, CFAEdge] = {}
        self.functions: dict[str, int] = {}
        self.control_dependents: dict[int, set[int]] = {}
        self.branch_sides: dict[int, tuple[set[int], set[int]]] = {}
        self.loop_headers: set[int] = set()
        self.current_function = "<global>"
        self._next_node = 1
        self._next_edge = 1
        self._last_node: int | None = None
        self._expr_vars = ExprVars()

    def parse(self) -> CFA:
        if c_parser is None or c_ast is None:
            raise RuntimeError("pycparser is not available")
        parser = c_parser.CParser()
        ast = parser.parse(self._sanitized_source(), filename=str(self.path))
        for ext in ast.ext:
            if isinstance(ext, c_ast.FuncDef):
                self._function(ext)
            elif isinstance(ext, c_ast.Decl):
                self._decl(ext, [])
        return CFA(
            self.nodes,
            self.edges,
            self.edge_by_line,
            self.functions,
            self.control_dependents,
            self.branch_sides,
            self.loop_headers,
        )

    def _sanitized_source(self) -> str:
        source = "\n".join(self.source_lines)
        source = re.sub(r"^\s*#.*$", "", source, flags=re.MULTILINE)
        source = re.sub(r"__attribute__\s*\(\([^)]*\)\)", "", source)
        return source

    def _function(self, node: object) -> None:
        assert c_ast is not None
        name = node.decl.name
        line = self._line(node.decl)
        self.current_function = name
        self.functions[name] = line
        self._last_node = self._new_node(line)
        self._statement(node.body, [])

    def _statement(self, node: object | None, controls: list[int]) -> None:
        if node is None or c_ast is None:
            return
        if isinstance(node, c_ast.Compound):
            for item in node.block_items or []:
                self._statement(item, controls)
        elif isinstance(node, c_ast.If):
            self._if(node, controls)
        elif isinstance(node, c_ast.Decl):
            self._decl(node, controls)
        elif isinstance(node, c_ast.Assignment):
            self._assignment(node, controls)
        elif isinstance(node, c_ast.UnaryOp):
            self._unary(node, controls)
        elif isinstance(node, c_ast.FuncCall):
            uses, calls = self._expr_vars.collect(node)
            self._add_edge(self._line(node), "stmt", set(), uses, calls, controls)
        elif isinstance(node, c_ast.Return):
            uses, calls = self._expr_vars.collect(node.expr)
            self._add_edge(self._line(node), "return", set(), uses, calls, controls)
        elif isinstance(node, c_ast.Break):
            self._add_edge(self._line(node), "break", set(), set(), set(), controls)
        elif isinstance(node, c_ast.Continue):
            self._add_edge(self._line(node), "continue", set(), set(), set(), controls)
        elif isinstance(node, c_ast.For):
            self._statement(node.init, controls)
            cond_uses, cond_calls = self._expr_vars.collect(node.cond)
            line = self._line(node)
            self.loop_headers.add(line)
            self._add_edge(line, "branch", set(), cond_uses, cond_calls, controls)
            self._statement(node.stmt, controls + [line])
            self._statement(node.next, controls + [line])
        elif isinstance(node, (c_ast.While, c_ast.DoWhile)):
            cond_uses, cond_calls = self._expr_vars.collect(node.cond)
            line = self._line(node)
            self.loop_headers.add(line)
            self._add_edge(line, "branch", set(), cond_uses, cond_calls, controls)
            self._statement(node.stmt, controls + [line])
        else:
            uses, calls = self._expr_vars.collect(node)
            if uses or calls:
                self._add_edge(self._line(node), "stmt", set(), uses, calls, controls)

    def _if(self, node: object, controls: list[int]) -> None:
        line = self._line(node)
        uses, calls = self._expr_vars.collect(node.cond)
        self._add_edge(line, "branch", set(), uses, calls, controls)
        nested_controls = controls + [line]
        before_true = set(self.edge_by_line)
        self._statement(node.iftrue, nested_controls)
        true_lines = set(self.edge_by_line) - before_true
        before_false = set(self.edge_by_line)
        self._statement(node.iffalse, nested_controls)
        false_lines = set(self.edge_by_line) - before_false
        self.branch_sides[line] = (true_lines, false_lines)

    def _decl(self, node: object, controls: list[int]) -> None:
        defs = {node.name} if getattr(node, "name", None) else set()
        uses, calls = self._expr_vars.collect(getattr(node, "init", None))
        self._add_edge(self._line(node), "stmt", defs, uses, calls, controls)

    def _assignment(self, node: object, controls: list[int]) -> None:
        defs = self._lvalue_vars(node.lvalue)
        ruses, calls = self._expr_vars.collect(node.rvalue)
        uses = set(ruses)
        if node.op != "=":
            uses |= defs
        self._add_edge(self._line(node), "stmt", defs, uses, calls, controls)

    def _unary(self, node: object, controls: list[int]) -> None:
        uses, calls = self._expr_vars.collect(node)
        defs = set(uses) if node.op in {"p++", "p--", "++", "--"} else set()
        self._add_edge(self._line(node), "stmt", defs, uses, calls, controls)

    def _lvalue_vars(self, node: object | None) -> set[str]:
        if c_ast is None or node is None:
            return set()
        if isinstance(node, c_ast.ID):
            return {node.name}
        names, _ = self._expr_vars.collect(node)
        return names

    def _add_edge(
        self,
        line: int,
        kind: str,
        defs: set[str],
        uses: set[str],
        calls: set[str],
        controls: list[int],
    ) -> None:
        if line <= 0:
            return
        text = self.source_lines[line - 1].strip() if line <= len(self.source_lines) else ""
        source = self._last_node or self._new_node(line)
        target = self._new_node(line)
        self._last_node = target
        terminates = self._terminates(kind, text, calls)
        loop_transfer = kind in {"break", "continue"}
        edge = CFAEdge(
            self._next_edge,
            source,
            target,
            line,
            text,
            kind,
            defs,
            uses,
            controls,
            calls,
            None,
            terminates,
            loop_transfer,
        )
        self._next_edge += 1
        self.edges.append(edge)
        self.edge_by_line.setdefault(line, edge)
        for ctrl in controls:
            self.control_dependents.setdefault(ctrl, set()).add(line)

    def _new_node(self, line: int) -> int:
        node_id = self._next_node
        self._next_node += 1
        self.nodes[node_id] = CFANode(node_id, line, self.current_function)
        return node_id

    @staticmethod
    def _line(node: object | None) -> int:
        coord = getattr(node, "coord", None)
        return int(coord.line) if coord and coord.line else -1

    @staticmethod
    def _terminates(kind: str, text: str, calls: set[str]) -> bool:
        compact = re.sub(r"\s+", "", text)
        return (
            kind == "return"
            or bool(calls & {"exit", "abort"})
            or ("__VERIFIER_assume" in calls and compact.endswith("(0);"))
        )


def parse_c(path: Path) -> CFA:
    if c_parser is not None and c_ast is not None:
        try:
            return PycparserCFAParser(path).parse()
        except Exception as exc:
            print(f"warning: pycparser failed ({exc}); falling back to line parser")
    return LineCParser(path).parse()


def parse_witness(path: Path) -> tuple[list[str], list[WaypointSegment]]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    first_segment = next(
        (idx for idx, line in enumerate(lines) if re.match(r"\s*-\s+segment:\s*$", line)),
        len(lines),
    )
    prefix = lines[:first_segment]
    segments: list[WaypointSegment] = []
    idx = first_segment
    while idx < len(lines):
        start = idx
        idx += 1
        while idx < len(lines) and not re.match(r"\s*-\s+segment:\s*$", lines[idx]):
            idx += 1
        block = lines[start:idx]
        segments.append(parse_segment(block))
    return prefix, segments


def parse_segment(lines: list[str]) -> WaypointSegment:
    segment = WaypointSegment(lines=lines)
    for line in lines:
        if re.search(r"\btype:\s*", line):
            segment.waypoint_type = scalar_value(line)
        elif re.search(r"\baction:\s*", line):
            segment.action = scalar_value(line)
        elif re.search(r"\bline:\s*", line):
            try:
                segment.line = int(scalar_value(line) or "")
            except ValueError:
                segment.line = None
        elif re.search(r"\bfunction:\s*", line):
            segment.function = scalar_value(line)
    return segment


def scalar_value(line: str) -> str | None:
    if ":" not in line:
        return None
    value = line.split(":", 1)[1].strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value or None


def find_target_segment(segments: Iterable[WaypointSegment]) -> WaypointSegment | None:
    target = None
    for segment in segments:
        if segment.waypoint_type == "target":
            target = segment
    return target


def initial_relevant_vars(
    segments: list[WaypointSegment],
    cfa: CFA,
    target: WaypointSegment | None,
) -> tuple[set[str], set[int]]:
    marked: set[int] = set()
    if target is None:
        return set(), marked

    target_edge = cfa.edge_by_line.get(target.line or -1)
    if target_edge and target_edge.uses:
        return set(target_edge.uses), marked

    target_function = target.function
    if target_function and target_function in cfa.functions:
        call_lines = [
            edge.line
            for edge in cfa.edges
            if edge.line != cfa.functions[target_function] and target_function in edge.calls
        ]
        if call_lines:
            call_line = max(call_lines)
            marked.add(call_line)
            call_edge = cfa.edge_by_line.get(call_line)
            if call_edge and call_edge.controls:
                nearest = call_edge.controls[-1]
                marked.add(nearest)
                return set(cfa.edge_by_line[nearest].uses), marked

    for segment in reversed(segments):
        if segment.waypoint_type == "branching" and segment.action == "follow":
            edge = cfa.edge_by_line.get(segment.line or -1)
            if edge:
                marked.add(edge.line)
                return set(edge.uses), marked

    return set(), marked


def branch_has_terminating_side_reaching_target(cfa: CFA, branch_line: int, target_or_marked: set[int]) -> bool:
    sides = cfa.branch_sides.get(branch_line)
    if not sides:
        return False
    true_lines, false_lines = sides
    true_cuts_path = any(edge_cuts_current_path(cfa.edge_by_line[line]) for line in true_lines if line in cfa.edge_by_line)
    false_cuts_path = any(edge_cuts_current_path(cfa.edge_by_line[line]) for line in false_lines if line in cfa.edge_by_line)

    later_reaches_target = any(line > branch_line for line in target_or_marked)
    true_reaches_target = bool(true_lines & target_or_marked) or later_reaches_target
    false_reaches_target = bool(false_lines & target_or_marked) or later_reaches_target
    return (true_cuts_path and false_reaches_target) or (false_cuts_path and true_reaches_target)


def edge_cuts_current_path(edge: CFAEdge) -> bool:
    return edge.terminates or edge.loop_transfer


def backward_slice(cfa: CFA, initial_vars: set[str], initial_marked: set[int]) -> tuple[set[int], set[int]]:
    relevant = set(initial_vars)
    marked = set(initial_marked)
    reachability_relevant_branches: set[int] = set()
    target_or_marked = set(initial_marked)

    for edge in reversed(cfa.edges):
        should_mark = False
        if edge_cuts_current_path(edge) and edge.controls:
            for branch_line in edge.controls:
                reachability_relevant_branches.add(branch_line)
                target_or_marked.add(branch_line)
                branch = cfa.edge_by_line.get(branch_line)
                if branch:
                    relevant |= branch.uses
        if edge.kind == "continue":
            for loop_line in reversed(edge.controls):
                if loop_line in cfa.loop_headers:
                    reachability_relevant_branches.add(loop_line)
                    target_or_marked.add(loop_line)
                    loop = cfa.edge_by_line.get(loop_line)
                    if loop:
                        relevant |= loop.uses
                    break

        if edge.kind == "branch":
            controls_marked = bool(cfa.control_dependents.get(edge.line, set()) & target_or_marked)
            data_relevant = bool(edge.uses & relevant)
            reachability_relevant = (
                edge.line in reachability_relevant_branches
                or branch_has_terminating_side_reaching_target(cfa, edge.line, target_or_marked)
            )
            should_mark = data_relevant or controls_marked or reachability_relevant
            if should_mark:
                relevant |= edge.uses
            if reachability_relevant:
                reachability_relevant_branches.add(edge.line)
        elif edge.defs & relevant:
            should_mark = True
            relevant -= edge.defs
            relevant |= edge.uses

        if should_mark:
            marked.add(edge.line)
            target_or_marked.add(edge.line)

    return marked, reachability_relevant_branches


def keep_segment(
    segment: WaypointSegment,
    marked_lines: set[int],
    reachability_relevant_branches: set[int],
    cfa: CFA,
) -> bool:
    if segment.waypoint_type == "target":
        return True
    if segment.line is None:
        return True
    if segment.line not in cfa.edge_by_line:
        return True
    return segment.line in marked_lines or segment.line in reachability_relevant_branches


def cleanup_segments(segments: list[WaypointSegment]) -> list[WaypointSegment]:
    cleaned = []
    for segment in segments:
        if not segment.lines:
            continue
        if segment.action == "avoid" and segment.waypoint_type != "target":
            continue
        cleaned.append(segment)

    last_target = None
    for idx, segment in enumerate(cleaned):
        if segment.waypoint_type == "target":
            last_target = idx
    if last_target is not None and last_target != len(cleaned) - 1:
        target = cleaned.pop(last_target)
        cleaned.append(target)
    return cleaned


def slice_witness(c_path: Path, witness_path: Path, output_path: Path) -> tuple[int, int, int, int]:
    cfa = parse_c(c_path)
    prefix, segments = parse_witness(witness_path)
    target = find_target_segment(segments)
    initial_vars, initial_marked = initial_relevant_vars(segments, cfa, target)
    marked_lines, reachability_branches = backward_slice(cfa, initial_vars, initial_marked)
    kept = [
        segment
        for segment in segments
        if keep_segment(segment, marked_lines, reachability_branches, cfa)
    ]
    kept = cleanup_segments(kept)
    output_path.write_text("".join(prefix + [line for seg in kept for line in seg.lines]), encoding="utf-8")
    return len(segments), len(kept), len(marked_lines), len(reachability_branches)


def write_cfa_dot(cfa: CFA, output_path: Path) -> None:
    lines = ["digraph CFA {\n", "  node [shape=circle];\n"]
    for node in cfa.nodes.values():
        lines.append(f'  n{node.node_id} [label="{node.node_id}\\n{node.function}:{node.line}"];\n')
    for edge in cfa.edges:
        label = edge.text.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'  n{edge.source} -> n{edge.target} [label="{edge.line}: {label}"];\n')
    lines.append("}\n")
    output_path.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Slice a CPAchecker witness using C DEF/USE dependencies.")
    parser.add_argument("program", type=Path, help="C program P")
    parser.add_argument("witness", type=Path, help="CPAchecker witness W")
    parser.add_argument("-o", "--output", type=Path, help="Output sliced witness W'")
    parser.add_argument("--dump-cfa-dot", type=Path, help="Write the constructed CFA as Graphviz DOT")
    args = parser.parse_args()

    output = args.output
    if output is None:
        output = args.witness.with_name(args.witness.stem + ".sliced.yml")

    if args.dump_cfa_dot:
        write_cfa_dot(parse_c(args.program), args.dump_cfa_dot)

    before, after, marked, reach_branches = slice_witness(args.program, args.witness, output)
    print(
        f"{args.witness.name}: kept {after}/{before} segments, "
        f"marked {marked} data/control C locations, "
        f"{reach_branches} reachability branches -> {output}"
    )
    if args.dump_cfa_dot:
        print(f"CFA DOT -> {args.dump_cfa_dot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
