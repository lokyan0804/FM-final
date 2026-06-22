#!/usr/bin/env python3
"""Compress CPAchecker violation witnesses by CFA dependency slicing."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Iterable

try:
    from pycparser import c_ast, c_generator, c_parser
except ImportError:
    c_ast = None
    c_generator = None
    c_parser = None

try:
    import z3
except ImportError:
    z3 = None


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
    function: str | None = None
    file: str | None = None


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


@dataclass
class SmtResult:
    necessary_branches: set[int]
    removable_branches: set[int]
    unknown_branches: set[int]


@dataclass
class SlicedCFA:
    original: CFA
    edges: list[CFAEdge]
    edge_by_line: dict[int, CFAEdge]
    kept_lines: set[int]
    data_relevant_lines: set[int]
    reachability_relevant_branches: set[int]
    target_lines: set[int]


@dataclass
class TraceFormula:
    formula: object
    edge: CFAEdge
    role: str


@dataclass
class LocalizationResult:
    suspicious_edges: set[int]
    suspicious_edge_ids: set[int]
    unknown_edges: set[int]
    fallback_used: bool
    method: str = "unsat-core"
    solver_result: str = "unknown"
    trace_formula: list[dict[str, object]] = field(default_factory=list)
    precondition: list[str] = field(default_factory=list)
    pi: list[dict[str, object]] = field(default_factory=list)
    error_guard: dict[str, object] | None = None
    safe_postcondition: str | None = None
    unsat_core_literals: list[str] = field(default_factory=list)
    fallback_reason: str | None = None


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
            self.current_function,
            str(self.path),
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
        cleaned: list[str] = []
        in_block_comment = False
        for raw in self.source_lines:
            line, in_block_comment = strip_comments(raw, in_block_comment)
            cleaned.append(line)
        source = "\n".join(cleaned)
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
            self.current_function,
            str(self.path),
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


def parse_c_ast(path: Path) -> object:
    if c_parser is None or c_ast is None:
        raise RuntimeError("pycparser is not available")
    source = PycparserCFAParser(path)._sanitized_source()
    return c_parser.CParser().parse(source, filename=str(path))


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


def witness_branch_choices(segments: Iterable[WaypointSegment]) -> dict[int, bool]:
    choices = {}
    for segment in segments:
        if segment.waypoint_type != "branching" or segment.line is None:
            continue
        value = None
        for line in segment.lines:
            if re.search(r"\bvalue:\s*", line):
                value = scalar_value(line)
                break
        if value == "true":
            choices[segment.line] = True
        elif value == "false":
            choices[segment.line] = False
    return choices


def witness_branch_choice_queues(segments: Iterable[WaypointSegment]) -> dict[int, list[bool]]:
    choices: dict[int, list[bool]] = {}
    for segment in segments:
        if segment.waypoint_type != "branching" or segment.line is None:
            continue
        value = None
        for line in segment.lines:
            if re.search(r"\bvalue:\s*", line):
                value = scalar_value(line)
                break
        if value == "true":
            choices.setdefault(segment.line, []).append(True)
        elif value == "false":
            choices.setdefault(segment.line, []).append(False)
    return choices


def main_function(ast: object) -> object | None:
    if c_ast is None:
        return None
    for ext in getattr(ast, "ext", []):
        if isinstance(ext, c_ast.FuncDef) and ext.decl.name == "main":
            return ext
    return None


class UnsupportedSmtConstruct(Exception):
    pass


class SmtState:
    def __init__(self) -> None:
        self.env: dict[str, object] = {}
        self.versions: dict[str, int] = {}
        self.constraints: list[object] = []
        self.hit_target = False
        self.terminated = False

    def clone(self) -> "SmtState":
        other = SmtState()
        other.env = dict(self.env)
        other.versions = dict(self.versions)
        other.constraints = list(self.constraints)
        other.hit_target = self.hit_target
        other.terminated = self.terminated
        return other


class SmtTraceExecutor:
    BV_BITS = 32

    def __init__(self, choices: dict[int, bool], override: tuple[int, bool] | None = None):
        if z3 is None or c_ast is None:
            raise RuntimeError("z3 and pycparser are required for SMT slicing")
        self.choices = choices
        self.override = override
        self._fresh_counter = 0
        self.fresh_symbols: list[object] = []

    def reaches_target_sat(self, func: object) -> bool:
        states = [SmtState()]
        final_states = self.exec_stmt(func.body, states)
        for state in final_states:
            if not state.hit_target:
                continue
            solver = z3.Solver()
            solver.add(*state.constraints)
            if solver.check() == z3.sat:
                return True
        return False

    def exec_stmt(self, node: object | None, states: list[SmtState]) -> list[SmtState]:
        if node is None:
            return states
        if c_ast is None:
            raise UnsupportedSmtConstruct("pycparser AST unavailable")
        if isinstance(node, c_ast.Compound):
            for item in node.block_items or []:
                states = self.exec_stmt(item, states)
            return states
        if isinstance(node, c_ast.Decl):
            return [self.exec_decl(node, state) for state in states if not state.terminated]
        if isinstance(node, c_ast.Assignment):
            return [self.exec_assignment(node, state) for state in states if not state.terminated]
        if isinstance(node, c_ast.UnaryOp):
            return [self.exec_unary(node, state) for state in states if not state.terminated]
        if isinstance(node, c_ast.If):
            return self.exec_if(node, states)
        if isinstance(node, c_ast.FuncCall):
            return [self.exec_call(node, state) for state in states if not state.terminated]
        if isinstance(node, c_ast.Return):
            out = []
            for state in states:
                state = state.clone()
                state.terminated = True
                out.append(state)
            return out
        if isinstance(node, (c_ast.Break, c_ast.Continue, c_ast.For, c_ast.While, c_ast.DoWhile, c_ast.Switch)):
            raise UnsupportedSmtConstruct(f"unsupported SMT statement: {type(node).__name__}")
        return states

    def exec_if(self, node: object, states: list[SmtState]) -> list[SmtState]:
        line = self.line(node)
        if self.override and self.override[0] == line:
            choice = self.override[1]
        else:
            choice = self.choices.get(line)
        if choice is None:
            raise UnsupportedSmtConstruct(f"branch line {line} has no witness choice")

        out = []
        for state in states:
            if state.terminated:
                out.append(state)
                continue
            cond = self.bool_expr(node.cond, state)
            chosen = state.clone()
            chosen.constraints.append(cond if choice else z3.Not(cond))
            branch_node = node.iftrue if choice else node.iffalse
            out.extend(self.exec_stmt(branch_node, [chosen]))
        return out

    def exec_decl(self, node: object, state: SmtState) -> SmtState:
        state = state.clone()
        if getattr(node, "name", None) is None:
            return state
        if getattr(node, "init", None) is None:
            self.assign_fresh(state, node.name)
        else:
            self.assign_value(state, node.name, self.bv_expr(node.init, state))
        return state

    def exec_assignment(self, node: object, state: SmtState) -> SmtState:
        state = state.clone()
        if not isinstance(node.lvalue, c_ast.ID):
            raise UnsupportedSmtConstruct("only scalar ID assignments are supported")
        name = node.lvalue.name
        rhs = self.bv_expr(node.rvalue, state)
        if node.op != "=":
            lhs = self.var(state, name)
            rhs = self.apply_assignment_op(node.op, lhs, rhs)
        self.assign_value(state, name, rhs)
        return state

    def exec_unary(self, node: object, state: SmtState) -> SmtState:
        if node.op not in {"p++", "p--", "++", "--"} or not isinstance(node.expr, c_ast.ID):
            return state
        state = state.clone()
        name = node.expr.name
        cur = self.var(state, name)
        one = z3.BitVecVal(1, self.BV_BITS)
        self.assign_value(state, name, cur + one if "++" in node.op else cur - one)
        return state

    def exec_call(self, node: object, state: SmtState) -> SmtState:
        state = state.clone()
        name = self.call_name(node)
        if name in {"reach_error", "__VERIFIER_error", "__assert_fail"}:
            state.hit_target = True
            return state
        if name == "__VERIFIER_assume":
            args = getattr(node.args, "exprs", []) if node.args else []
            if len(args) != 1:
                raise UnsupportedSmtConstruct("assume expects one argument")
            state.constraints.append(self.bool_expr(args[0], state))
            return state
        if name == "assert":
            args = getattr(node.args, "exprs", []) if node.args else []
            if len(args) != 1:
                raise UnsupportedSmtConstruct("assert expects one argument")
            fail = state.clone()
            fail.constraints.append(z3.Not(self.bool_expr(args[0], state)))
            fail.hit_target = True
            return fail
        raise UnsupportedSmtConstruct(f"unsupported call statement: {name}")

    def bv_expr(self, node: object, state: SmtState) -> object:
        if isinstance(node, c_ast.ID):
            return self.var(state, node.name)
        if isinstance(node, c_ast.Constant):
            if node.type not in {"int", "unsigned int"}:
                raise UnsupportedSmtConstruct(f"unsupported constant type {node.type}")
            value = int(re.sub(r"[uUlL]+$", "", node.value), 0)
            return z3.BitVecVal(value, self.BV_BITS)
        if isinstance(node, c_ast.BinaryOp):
            if node.op in {"==", "!=", "<", "<=", ">", ">=", "&&", "||"}:
                return z3.If(self.bool_expr(node, state), z3.BitVecVal(1, self.BV_BITS), z3.BitVecVal(0, self.BV_BITS))
            left = self.bv_expr(node.left, state)
            right = self.bv_expr(node.right, state)
            return self.apply_binary_bv(node.op, left, right)
        if isinstance(node, c_ast.Cast):
            return self.bv_expr(node.expr, state)
        if isinstance(node, c_ast.UnaryOp):
            expr = self.bv_expr(node.expr, state)
            if node.op == "+":
                return expr
            if node.op == "-":
                return -expr
            if node.op == "~":
                return ~expr
            if node.op == "!":
                return z3.If(self.bool_expr(node, state), z3.BitVecVal(1, self.BV_BITS), z3.BitVecVal(0, self.BV_BITS))
        if isinstance(node, c_ast.FuncCall):
            name = self.call_name(node)
            if name.startswith("__VERIFIER_nondet_"):
                return self.fresh_symbol(f"nondet_{self.line(node)}")
        raise UnsupportedSmtConstruct(f"unsupported expression: {type(node).__name__}")

    def bool_expr(self, node: object, state: SmtState) -> object:
        if isinstance(node, c_ast.BinaryOp):
            if node.op == "&&":
                return z3.And(self.bool_expr(node.left, state), self.bool_expr(node.right, state))
            if node.op == "||":
                return z3.Or(self.bool_expr(node.left, state), self.bool_expr(node.right, state))
            left = self.bv_expr(node.left, state)
            right = self.bv_expr(node.right, state)
            if node.op == "==":
                return left == right
            if node.op == "!=":
                return left != right
            if node.op == "<":
                return left < right
            if node.op == "<=":
                return left <= right
            if node.op == ">":
                return left > right
            if node.op == ">=":
                return left >= right
        if isinstance(node, c_ast.UnaryOp) and node.op == "!":
            return z3.Not(self.bool_expr(node.expr, state))
        return self.bv_expr(node, state) != z3.BitVecVal(0, self.BV_BITS)

    def apply_binary_bv(self, op: str, left: object, right: object) -> object:
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            return left / right
        if op == "%":
            return left % right
        if op == "&":
            return left & right
        if op == "|":
            return left | right
        if op == "^":
            return left ^ right
        if op == "<<":
            return left << right
        if op == ">>":
            return left >> right
        raise UnsupportedSmtConstruct(f"unsupported binary operator {op}")

    def apply_assignment_op(self, op: str, left: object, right: object) -> object:
        return self.apply_binary_bv(op[:-1], left, right)

    def assign_fresh(self, state: SmtState, name: str) -> None:
        self.assign_value(state, name, self.fresh_symbol(name))

    def assign_value(self, state: SmtState, name: str, value: object) -> None:
        version = state.versions.get(name, 0) + 1
        state.versions[name] = version
        symbol = z3.BitVec(f"{name}_{version}", self.BV_BITS)
        state.env[name] = symbol
        state.constraints.append(symbol == value)

    def var(self, state: SmtState, name: str) -> object:
        if name not in state.env:
            self.assign_fresh(state, name)
        return state.env[name]

    def fresh_symbol(self, base: str) -> object:
        safe = re.sub(r"\W+", "_", base)
        self._fresh_counter += 1
        symbol = z3.BitVec(f"{safe}_fresh_{self._fresh_counter}", self.BV_BITS)
        self.fresh_symbols.append(symbol)
        return symbol

    @staticmethod
    def call_name(node: object) -> str:
        if isinstance(node.name, c_ast.ID):
            return node.name.name
        raise UnsupportedSmtConstruct("unsupported call target")

    @staticmethod
    def line(node: object | None) -> int:
        coord = getattr(node, "coord", None)
        return int(coord.line) if coord and coord.line else -1


def smt_branch_prune(c_path: Path, segments: list[WaypointSegment]) -> SmtResult:
    ast = parse_c_ast(c_path)
    func = main_function(ast)
    if func is None:
        raise RuntimeError("main function not found")
    choices = witness_branch_choices(segments)
    necessary: set[int] = set()
    removable: set[int] = set()
    unknown: set[int] = set()
    branch_lines = [segment.line for segment in segments if segment.waypoint_type == "branching" and segment.line in choices]

    for line in reversed(branch_lines):
        opposite = not choices[line]
        try:
            sat_after_flip = SmtTraceExecutor(choices, (line, opposite)).reaches_target_sat(func)
        except UnsupportedSmtConstruct:
            unknown.add(line)
            necessary.add(line)
            continue
        if sat_after_flip:
            removable.add(line)
        else:
            necessary.add(line)
    return SmtResult(necessary, removable, unknown)


class SlicedPathFormulaBuilder:
    def __init__(self, branch_choices: dict[int, bool] | dict[int, list[bool]]):
        if z3 is None or c_ast is None or c_parser is None:
            raise RuntimeError("z3 and pycparser are required for SMT localization")
        self.branch_choices = self._normalize_choices(branch_choices)
        self.executor = SmtTraceExecutor({})
        self.parser = c_parser.CParser()
        self.state = SmtState()
        self.unknown_edges: set[int] = set()

    @staticmethod
    def _normalize_choices(branch_choices: dict[int, bool] | dict[int, list[bool]]) -> dict[int, list[bool]]:
        queues: dict[int, list[bool]] = {}
        for line, value in branch_choices.items():
            if isinstance(value, list):
                queues[line] = list(value)
            else:
                queues[line] = [value]
        return queues

    def next_branch_choice(self, line: int) -> bool | None:
        queue = self.branch_choices.get(line)
        if not queue:
            return None
        if len(queue) == 1:
            return queue[0]
        return queue.pop(0)

    def build(self, path: list[CFAEdge]) -> tuple[list[TraceFormula], set[int]]:
        formulas: list[TraceFormula] = []
        for edge in path:
            before = len(self.state.constraints)
            try:
                role = self.encode_edge(edge)
                new_constraints = self.state.constraints[before:]
                if not new_constraints:
                    new_constraints = [z3.BoolVal(True)]
                for formula in new_constraints:
                    formulas.append(TraceFormula(formula, edge, role))
            except UnsupportedSmtConstruct:
                self.unknown_edges.add(edge.line)
                formulas.append(TraceFormula(z3.BoolVal(True), edge, "unknown"))
        return formulas, self.unknown_edges

    def encode_edge(self, edge: CFAEdge) -> str:
        if edge.kind == "branch":
            condition = self.parse_branch_condition(edge.text)
            cond = self.executor.bool_expr(condition, self.state)
            choice = self.next_branch_choice(edge.line)
            if choice is None:
                self.unknown_edges.add(edge.line)
                self.state.constraints.append(z3.BoolVal(True))
                return "unknown_branch"
            self.state.constraints.append(cond if choice else z3.Not(cond))
            return "guard"

        if edge.kind == "stmt" and edge.text.lstrip().startswith("for"):
            update = self.for_update_statement(edge.text)
            if update is None:
                raise UnsupportedSmtConstruct("for update not found")
            node = self.parse_statement(update)
        else:
            node = self.parse_statement(edge.text)
        if isinstance(node, c_ast.Decl):
            self.state = self.executor.exec_decl(node, self.state)
            return "transition"
        if isinstance(node, c_ast.Assignment):
            self.state = self.executor.exec_assignment(node, self.state)
            return "transition"
        if isinstance(node, c_ast.UnaryOp):
            self.state = self.executor.exec_unary(node, self.state)
            return "transition"
        if isinstance(node, c_ast.FuncCall):
            name = self.executor.call_name(node)
            if name in {"reach_error", "__VERIFIER_error", "__assert_fail"}:
                self.state.hit_target = True
                self.state.constraints.append(z3.BoolVal(True))
                return "target"
            self.state = self.executor.exec_call(node, self.state)
            return "assume" if name == "__VERIFIER_assume" else "transition"
        if isinstance(node, c_ast.Return):
            self.state.constraints.append(z3.BoolVal(True))
            self.state.terminated = True
            return "return"
        self.state.constraints.append(z3.BoolVal(True))
        return "unknown"

    def parse_statement(self, text: str) -> object:
        try:
            ast = self.parser.parse(f"void __trace(void) {{ {text} }}")
        except Exception as exc:
            raise UnsupportedSmtConstruct(f"statement did not parse: {text}") from exc
        func = ast.ext[0]
        items = func.body.block_items or []
        if not items:
            raise UnsupportedSmtConstruct("empty statement")
        return items[0]

    def parse_branch_condition(self, text: str) -> object:
        condition = self.branch_condition_text(text)
        if condition is None:
            raise UnsupportedSmtConstruct("branch condition not found")
        try:
            ast = self.parser.parse(f"void __trace(void) {{ if ({condition}) {{ }} }}")
        except Exception as exc:
            raise UnsupportedSmtConstruct(f"branch condition did not parse: {condition}") from exc
        func = ast.ext[0]
        items = func.body.block_items or []
        if not items or not isinstance(items[0], c_ast.If):
            raise UnsupportedSmtConstruct("branch did not parse as if")
        return items[0].cond

    @staticmethod
    def branch_condition_text(text: str) -> str | None:
        stripped = text.strip()
        if stripped.startswith("if"):
            return LineCParser._if_condition(stripped)
        if stripped.startswith("while"):
            return LineCParser._if_condition("if" + stripped[len("while") :])
        if stripped.startswith("for"):
            inside = SlicedPathFormulaBuilder.parenthesized_text(stripped)
            if inside is None:
                return None
            parts = SlicedPathFormulaBuilder.split_top_level_semicolons(inside)
            if len(parts) != 3:
                return None
            return parts[1].strip() or "1"
        return None

    @staticmethod
    def for_update_statement(text: str) -> str | None:
        inside = SlicedPathFormulaBuilder.parenthesized_text(text.strip())
        if inside is None:
            return None
        parts = SlicedPathFormulaBuilder.split_top_level_semicolons(inside)
        if len(parts) != 3:
            return None
        update = parts[2].strip()
        if not update:
            return None
        return update if update.endswith(";") else f"{update};"

    @staticmethod
    def parenthesized_text(text: str) -> str | None:
        open_paren = text.find("(")
        if open_paren == -1:
            return None
        depth = 0
        for idx in range(open_paren, len(text)):
            char = text[idx]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    return text[open_paren + 1 : idx]
        return None

    @staticmethod
    def split_top_level_semicolons(text: str) -> list[str]:
        parts: list[str] = []
        start = 0
        depth = 0
        for idx, char in enumerate(text):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == ";" and depth == 0:
                parts.append(text[start:idx])
                start = idx + 1
        parts.append(text[start:])
        return parts


class WitnessDrivenPathBuilder:
    MAX_LOOP_STEPS = 10000

    def __init__(self, c_path: Path, sliced_cfa: SlicedCFA, segments: list[WaypointSegment]):
        if c_ast is None or c_generator is None:
            raise RuntimeError("pycparser is required for witness-driven path building")
        self.ast = parse_c_ast(c_path)
        self.sliced_cfa = sliced_cfa
        self.choices = witness_branch_choice_queues(segments)
        self.generator = c_generator.CGenerator()
        self.formula_choices: dict[int, list[bool]] = {}
        self.edges_by_line_kind: dict[tuple[int, str], list[CFAEdge]] = {}
        self.edges_by_line: dict[int, list[CFAEdge]] = {}
        for edge in sliced_cfa.edges:
            self.edges_by_line_kind.setdefault((edge.line, edge.kind), []).append(edge)
            self.edges_by_line.setdefault(edge.line, []).append(edge)
        self.path: list[CFAEdge] = []
        self.loop_steps = 0

    def build(self) -> list[CFAEdge]:
        func = main_function(self.ast)
        if func is None:
            return find_witness_path_on_sliced_cfa(self.sliced_cfa)
        self.exec_stmt(func.body)
        target_edges = [
            edge
            for edge in self.sliced_cfa.edges
            if edge.function != "main" and (edge.line in self.sliced_cfa.target_lines or edge.calls & {"__assert_fail"})
        ]
        for edge in target_edges:
            if edge not in self.path:
                self.path.append(edge)
        return self.path or find_witness_path_on_sliced_cfa(self.sliced_cfa)

    def exec_stmt(self, node: object | None) -> str:
        if node is None or c_ast is None:
            return "normal"
        if isinstance(node, c_ast.Compound):
            for item in node.block_items or []:
                status = self.exec_stmt(item)
                if status != "normal":
                    return status
            return "normal"
        if isinstance(node, c_ast.If):
            return self.exec_if(node)
        if isinstance(node, c_ast.For):
            return self.exec_for(node)
        if isinstance(node, c_ast.While):
            return self.exec_while(node)
        if isinstance(node, c_ast.DoWhile):
            return self.exec_do_while(node)
        if isinstance(node, c_ast.Break):
            self.append_node_edge(node, "break")
            return "break"
        if isinstance(node, c_ast.Continue):
            self.append_node_edge(node, "continue")
            return "continue"
        if isinstance(node, c_ast.Return):
            self.append_node_edge(node, "return")
            return "return"
        if isinstance(node, (c_ast.Decl, c_ast.Assignment, c_ast.UnaryOp, c_ast.FuncCall)):
            self.append_node_edge(node, "stmt")
            if isinstance(node, c_ast.FuncCall) and self.call_name(node) in {"reach_error", "__VERIFIER_error", "__assert_fail"}:
                return "return"
            return "normal"
        if isinstance(node, c_ast.DeclList):
            for decl in node.decls or []:
                self.append_generated_edge(self.line(decl), self.statement_text(decl), "stmt")
            return "normal"
        return "normal"

    def exec_if(self, node: object) -> str:
        line = self.line(node)
        self.append_generated_edge(line, f"if ({self.expr_text(node.cond)}) {{", "branch")
        choice = self.next_choice(line)
        if choice is None:
            choice = True
        self.record_choice(line, choice)
        return self.exec_stmt(node.iftrue if choice else node.iffalse)

    def exec_for(self, node: object) -> str:
        self.exec_for_init(node.init)
        line = self.line(node)
        while self.loop_guard():
            self.append_generated_edge(line, f"if ({self.expr_text(node.cond) if node.cond is not None else '1'}) {{", "branch")
            choice = self.next_choice(line)
            if choice is None:
                choice = False
            self.record_choice(line, choice)
            if not choice:
                return "normal"
            status = self.exec_stmt(node.stmt)
            if status == "break":
                return "normal"
            if status == "return":
                return "return"
            self.exec_for_next(node.next, line)
        return "normal"

    def exec_while(self, node: object) -> str:
        line = self.line(node)
        while self.loop_guard():
            self.append_generated_edge(line, f"if ({self.expr_text(node.cond)}) {{", "branch")
            choice = self.next_choice(line)
            if choice is None:
                choice = self.is_constant_true(node.cond)
            self.record_choice(line, choice)
            if not choice:
                return "normal"
            status = self.exec_stmt(node.stmt)
            if status == "break":
                return "normal"
            if status == "return":
                return "return"
        return "normal"

    def exec_do_while(self, node: object) -> str:
        line = self.line(node)
        iterations = max(1, len(self.choices.get(line, [])))
        for idx in range(iterations):
            if not self.loop_guard():
                return "normal"
            status = self.exec_stmt(node.stmt)
            if status == "break":
                return "normal"
            if status == "return":
                return "return"
            self.append_generated_edge(line, f"if ({self.expr_text(node.cond)}) {{", "branch")
            self.record_choice(line, idx < iterations - 1)
            self.discard_choice(line)
            if idx == iterations - 1:
                break
        return "normal"

    def exec_for_init(self, node: object | None) -> None:
        if node is None:
            return
        if isinstance(node, c_ast.DeclList):
            for decl in node.decls or []:
                self.append_generated_edge(self.line(decl), self.statement_text(decl), "stmt")
        elif isinstance(node, (c_ast.Assignment, c_ast.UnaryOp)):
            self.append_generated_edge(self.line(node), self.statement_text(node), "stmt")

    def exec_for_next(self, node: object | None, fallback_line: int) -> None:
        if node is None:
            return
        line = self.line(node)
        if line <= 0:
            line = fallback_line
        self.append_generated_edge(line, self.statement_text(node), "stmt")

    def append_node_edge(self, node: object, kind: str) -> None:
        self.append_generated_edge(self.line(node), self.statement_text(node), kind)

    def append_generated_edge(self, line: int, text: str, kind: str) -> None:
        if line not in self.sliced_cfa.kept_lines:
            return
        edge = self.edge_for(line, kind) or self.edge_for(line, "branch" if kind == "stmt" else "stmt")
        if edge is None:
            return
        if text and text != edge.text:
            edge = replace(edge, text=text, kind=kind)
        self.path.append(edge)

    def edge_for(self, line: int, kind: str) -> CFAEdge | None:
        edges = self.edges_by_line_kind.get((line, kind))
        if edges:
            return edges[0]
        any_edges = self.edges_by_line.get(line)
        return any_edges[0] if any_edges else None

    def next_choice(self, line: int) -> bool | None:
        queue = self.choices.get(line)
        if not queue:
            return None
        return queue.pop(0)

    def discard_choice(self, line: int) -> None:
        queue = self.choices.get(line)
        if queue:
            queue.pop(0)

    def record_choice(self, line: int, choice: bool) -> None:
        if line in self.sliced_cfa.kept_lines:
            self.formula_choices.setdefault(line, []).append(choice)

    def loop_guard(self) -> bool:
        self.loop_steps += 1
        return self.loop_steps <= self.MAX_LOOP_STEPS

    def expr_text(self, node: object | None) -> str:
        if node is None:
            return "1"
        return self.generator.visit(node)

    def statement_text(self, node: object) -> str:
        text = self.generator.visit(node)
        return text if text.endswith(";") or text.endswith("}") else f"{text};"

    @staticmethod
    def is_constant_true(node: object | None) -> bool:
        if c_ast is None or node is None:
            return False
        if isinstance(node, c_ast.Constant) and node.type in {"int", "unsigned int"}:
            return int(re.sub(r"[uUlL]+$", "", node.value), 0) != 0
        return False

    @staticmethod
    def line(node: object | None) -> int:
        coord = getattr(node, "coord", None)
        return int(coord.line) if coord and coord.line else -1

    @staticmethod
    def call_name(node: object) -> str:
        if c_ast is not None and isinstance(node.name, c_ast.ID):
            return node.name.name
        return ""


def build_witness_driven_path(
    c_path: Path,
    sliced_cfa: SlicedCFA,
    segments: list[WaypointSegment],
) -> tuple[list[CFAEdge], dict[int, list[bool]]]:
    try:
        builder = WitnessDrivenPathBuilder(c_path, sliced_cfa, segments)
        return builder.build(), builder.formula_choices
    except Exception as exc:
        print(f"warning: witness-driven path failed ({exc}); falling back to CFA order")
        return find_witness_path_on_sliced_cfa(sliced_cfa), witness_branch_choice_queues(segments)


def find_witness_path_on_sliced_cfa(sliced_cfa: SlicedCFA) -> list[CFAEdge]:
    main_edges = [edge for edge in sliced_cfa.edges if edge.function == "main"]
    if main_edges:
        return main_edges
    return list(sliced_cfa.edges)


def choose_error_guard_index(formulas: list[TraceFormula]) -> int | None:
    target_indexes = [idx for idx, item in enumerate(formulas) if item.role == "target"]
    limit = target_indexes[0] if target_indexes else len(formulas)
    for idx in range(limit - 1, -1, -1):
        if formulas[idx].role in {"guard", "assume"}:
            return idx
    return None


def guard_indexes_before_target(formulas: list[TraceFormula]) -> list[int]:
    target_indexes = [idx for idx, item in enumerate(formulas) if item.role == "target"]
    limit = target_indexes[0] if target_indexes else len(formulas)
    return [idx for idx, item in enumerate(formulas[:limit]) if item.role in {"guard", "assume"}]


def is_nondet_input_formula(item: TraceFormula) -> bool:
    return "__VERIFIER_nondet_" in item.edge.text


def trace_item_to_json(index: int, item: TraceFormula) -> dict[str, object]:
    return {
        "index": index,
        "formula": smt_formula_string(item.formula),
        "role": item.role,
        "edge": edge_summary_json(item.edge),
    }


def smt_formula_string(formula: object) -> str:
    sexpr = getattr(formula, "sexpr", None)
    return sexpr() if callable(sexpr) else str(formula)


def edge_summary_json(edge: CFAEdge) -> dict[str, object]:
    return {
        "id": f"e{edge.edge_id}",
        "line": edge.line,
        "function": edge.function,
        "kind": edge.kind,
        "statement": edge.text,
    }


def and_formula_string(formulas: list[object]) -> str:
    if not formulas:
        return "true"
    if len(formulas) == 1:
        return smt_formula_string(formulas[0])
    return smt_formula_string(z3.And(*formulas))


def and_smt_strings(formulas: list[str]) -> str:
    if not formulas:
        return "true"
    if len(formulas) == 1:
        return formulas[0]
    return "(and\n  " + "\n  ".join(formulas) + "\n)"


def compact_report_items(items: list[dict[str, object]]) -> list[dict[str, object]]:
    compacted: list[dict[str, object]] = []
    for item in items:
        key = (item.get("line"), item.get("text"))
        if compacted and compacted[-1].get("key") == key:
            compacted[-1]["count"] = int(compacted[-1]["count"]) + 1
            compacted[-1]["end_index"] = item.get("index")
            compacted[-1]["indexes"].append(item.get("index"))
            continue
        compacted.append(
            {
                "key": key,
                "line": item.get("line"),
                "text": item.get("text"),
                "start_index": item.get("index"),
                "end_index": item.get("index"),
                "indexes": [item.get("index")],
                "count": 1,
            }
        )
    return compacted


def compact_evidence_items(items: list[dict[str, object]]) -> list[dict[str, object]]:
    compacted: list[dict[str, object]] = []
    for item in sorted(items, key=lambda entry: (int(entry.get("trace_index", 10**9)), str(entry.get("part", "")))):
        key = (item.get("part"), item.get("line"), item.get("text"))
        if compacted and compacted[-1].get("key") == key:
            compacted[-1]["count"] = int(compacted[-1]["count"]) + 1
            compacted[-1]["trace_indexes"].append(item.get("trace_index"))
            compacted[-1]["indexes"].append(item.get("index"))
            continue
        compacted.append(
            {
                "key": key,
                "part": item.get("part"),
                "line": item.get("line"),
                "text": item.get("text"),
                "trace_indexes": [item.get("trace_index")],
                "indexes": [item.get("index")],
                "count": 1,
            }
        )
    return compacted


def summarize_indexes(indexes: list[object], prefix: str) -> str:
    nums = [idx for idx in indexes if isinstance(idx, int)]
    if not nums:
        return ""
    if len(nums) == 1:
        return f"{prefix}_{nums[0]}"
    if nums == list(range(nums[0], nums[-1] + 1)):
        return f"{prefix}_{nums[0]}..{prefix}_{nums[-1]}"
    if len(nums) <= 6:
        return ", ".join(f"{prefix}_{idx}" for idx in nums)
    return f"{prefix}_{nums[0]}, {prefix}_{nums[1]}, ... {prefix}_{nums[-1]}"


def summarize_report_indexes(indexes: list[object]) -> str:
    return summarize_indexes(indexes, "pi")


def precondition_from_model(formulas: list[TraceFormula], model: object) -> list[object]:
    precondition: list[object] = []
    for item in formulas:
        if not is_nondet_input_formula(item):
            continue
        formula = item.formula
        if not z3.is_eq(formula):
            continue
        lhs = formula.children()[0]
        value = model.eval(lhs, model_completion=True)
        precondition.append(lhs == value)
    return precondition


def parse_bv_literal(value: str) -> int | None:
    if value.startswith("#x"):
        return int(value[2:], 16)
    if value.startswith("#b"):
        return int(value[2:], 2)
    try:
        return int(value)
    except ValueError:
        return None


def input_values_from_formulas(precondition: list[str], pi: list[dict[str, object]]) -> list[dict[str, object]]:
    symbol_values: dict[str, dict[str, object]] = {}
    for formula in precondition:
        match = re.match(r"^\(=\s+(\S+)\s+(\S+)\)$", formula)
        if not match:
            continue
        left, right = match.groups()
        if left.startswith("#"):
            literal, symbol = left, right
        elif right.startswith("#"):
            literal, symbol = right, left
        else:
            continue
        decimal = parse_bv_literal(literal)
        symbol_values[symbol] = {
            "symbol": symbol,
            "value": literal,
            "decimal": decimal,
        }

    for item in pi:
        formula = str(item.get("formula", ""))
        match = re.match(r"^\(=\s+(\S+)\s+(\S+)\)$", formula)
        if not match:
            continue
        left, right = match.groups()
        assigned_var = None
        symbol = None
        if left in symbol_values:
            symbol = left
            assigned_var = left
        elif right in symbol_values:
            symbol = right
            assigned_var = right
        if symbol:
            symbol_values[symbol]["assigned_to"] = assigned_var
            symbol_values[symbol]["edge"] = item.get("edge")
            symbol_values[symbol]["trace_index"] = item.get("index")

    return list(symbol_values.values())


def suspicious_pi_items(localization: LocalizationResult) -> list[dict[str, object]]:
    suspicious_indexes = set()
    for lit in localization.unsat_core_literals:
        match = re.match(r"^a_(\d+)$", lit)
        if match:
            suspicious_indexes.add(int(match.group(1)))
    return [item for item in localization.pi if item.get("index") in suspicious_indexes]


def localize_suspicious_edges_unsat_core(
    path: list[CFAEdge],
    segments: list[WaypointSegment],
    branch_choices: dict[int, list[bool]] | None = None,
) -> LocalizationResult:
    branch_choices = branch_choices if branch_choices is not None else witness_branch_choice_queues(segments)
    builder = SlicedPathFormulaBuilder(branch_choices)
    formulas, unknown_edges = builder.build(path)
    trace_json = [trace_item_to_json(idx, item) for idx, item in enumerate(formulas)]
    if not formulas:
        return LocalizationResult(
            set(),
            set(),
            unknown_edges,
            True,
            trace_formula=trace_json,
            fallback_reason="empty trace formula",
        )

    full_solver = z3.Solver()
    full_solver.add(*(item.formula for item in formulas))
    full_result = full_solver.check()
    if full_result != z3.sat:
        fallback = set(edge.line for edge in path[-3:])
        return LocalizationResult(
            fallback,
            {edge.edge_id for edge in path[-3:]},
            unknown_edges,
            True,
            solver_result=str(full_result),
            trace_formula=trace_json,
            fallback_reason="full error trace was not SAT",
        )
    model = full_solver.model()
    psi = precondition_from_model(formulas, model)
    psi_json = [smt_formula_string(formula) for formula in psi]

    guard_indexes = guard_indexes_before_target(formulas)
    if not guard_indexes:
        fallback_edges = path[-3:]
        return LocalizationResult(
            {edge.line for edge in fallback_edges},
            {edge.edge_id for edge in fallback_edges},
            unknown_edges,
            True,
            solver_result="sat",
            trace_formula=trace_json,
            precondition=psi_json,
            fallback_reason="no guard/assume found before target",
        )

    error_guard_formula = z3.And(*(formulas[idx].formula for idx in guard_indexes))
    safe_phi = z3.Not(error_guard_formula)
    target_indexes = [idx for idx, item in enumerate(formulas) if item.role == "target"]
    target_limit = target_indexes[0] if target_indexes else len(formulas)
    guard_index_set = set(guard_indexes)
    pi_pairs = [
        (idx, item)
        for idx, item in enumerate(formulas[:target_limit])
        if idx not in guard_index_set and not is_nondet_input_formula(item)
    ]
    pi = [item for _, item in pi_pairs]
    pi_json = []
    for pi_idx, (trace_idx, item) in enumerate(pi_pairs):
        pi_item = trace_item_to_json(pi_idx, item)
        pi_item["trace_index"] = trace_idx
        pi_json.append(pi_item)
    error_guard_json = {
        "formula": smt_formula_string(error_guard_formula),
        "kind": "path_condition",
        "guards": [trace_item_to_json(idx, formulas[idx]) for idx in guard_indexes],
    }
    solver = z3.Solver()
    solver.add(*psi)
    solver.add(safe_phi)
    lit_to_edge: dict[str, CFAEdge] = {}
    for idx, item in enumerate(pi):
        lit = z3.Bool(f"a_{idx}")
        solver.assert_and_track(item.formula, lit)
        lit_to_edge[str(lit)] = item.edge

    result = solver.check()
    if result == z3.unsat:
        core = solver.unsat_core()
        suspicious = [lit_to_edge[str(lit)] for lit in core if str(lit) in lit_to_edge]
        return (
            LocalizationResult(
                {edge.line for edge in suspicious},
                {edge.edge_id for edge in suspicious},
                unknown_edges,
                False,
                solver_result=str(result),
                trace_formula=trace_json,
                precondition=psi_json,
                pi=pi_json,
                error_guard=error_guard_json,
                safe_postcondition=smt_formula_string(safe_phi),
                unsat_core_literals=[str(lit) for lit in core],
            )
            if suspicious
            else LocalizationResult(
                set(),
                set(),
                unknown_edges,
                False,
                solver_result=str(result),
                trace_formula=trace_json,
                precondition=psi_json,
                pi=pi_json,
                error_guard=error_guard_json,
                safe_postcondition=smt_formula_string(safe_phi),
                unsat_core_literals=[str(lit) for lit in core],
                fallback_reason="UNSAT was caused by precondition and postcondition; no tracked pi formula appears in the core",
            )
        )

    fallback_edges = [item.edge for item in pi[-3:]] or path[-3:]
    return LocalizationResult(
        {edge.line for edge in fallback_edges},
        {edge.edge_id for edge in fallback_edges},
        unknown_edges,
        True,
        solver_result=str(result),
        trace_formula=trace_json,
        precondition=psi_json,
        pi=pi_json,
        error_guard=error_guard_json,
        safe_postcondition=smt_formula_string(safe_phi),
        fallback_reason="psi and pi and safe_postcondition was not UNSAT",
    )


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

    for _ in range(len(cfa.edges) + 1):
        before = (set(relevant), set(marked), set(reachability_relevant_branches), set(target_or_marked))
        for edge in reversed(cfa.edges):
            should_mark = False
            if edge_cuts_current_path(edge) and edge.controls:
                if edge.kind in {"break", "continue"}:
                    should_mark = True
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
            else:
                for loop_line in edge.controls:
                    loop = cfa.edge_by_line.get(loop_line)
                    if loop_line in cfa.loop_headers and loop and edge.defs & loop.uses:
                        should_mark = True
                        relevant |= edge.uses
                        break

            if edge.kind != "branch" and edge.defs & relevant:
                should_mark = True
                relevant -= edge.defs
                relevant |= edge.uses

            if should_mark:
                marked.add(edge.line)
                target_or_marked.add(edge.line)
        after = (set(relevant), set(marked), set(reachability_relevant_branches), set(target_or_marked))
        if after == before:
            break

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


def keep_segment_for_sliced_cfa(segment: WaypointSegment, original_cfa: CFA, sliced_cfa: SlicedCFA) -> bool:
    if segment.waypoint_type == "target":
        return True
    if segment.line is None:
        return True
    if segment.line not in original_cfa.edge_by_line:
        return True
    return segment.line in sliced_cfa.edge_by_line or segment.line in sliced_cfa.target_lines


def build_sliced_cfa(
    cfa: CFA,
    data_relevant_lines: set[int],
    reachability_relevant_branches: set[int],
    target_lines: set[int] | None = None,
) -> SlicedCFA:
    target_lines = target_lines or set()
    kept_lines = set(data_relevant_lines) | set(reachability_relevant_branches) | set(target_lines)
    edges = [edge for edge in cfa.edges if edge.line in kept_lines]
    return SlicedCFA(
        original=cfa,
        edges=edges,
        edge_by_line={edge.line: edge for edge in edges},
        kept_lines={edge.line for edge in edges} | set(target_lines),
        data_relevant_lines=set(data_relevant_lines),
        reachability_relevant_branches=set(reachability_relevant_branches),
        target_lines=set(target_lines),
    )


def edge_to_json(edge: CFAEdge) -> dict[str, object]:
    return {
        "id": f"e{edge.edge_id}",
        "source": f"l{edge.source}",
        "target": f"l{edge.target}",
        "file": edge.file,
        "line": edge.line,
        "function": edge.function,
        "statement": edge.text,
        "kind": edge.kind,
        "defs": sorted(edge.defs),
        "uses": sorted(edge.uses),
        "controls": [f"line:{line}" for line in edge.controls],
        "calls": sorted(edge.calls),
        "terminates": edge.terminates,
        "loop_transfer": edge.loop_transfer,
    }


def sliced_cfa_to_json(sliced_cfa: SlicedCFA) -> dict[str, object]:
    first_edge = sliced_cfa.edges[0] if sliced_cfa.edges else None
    target_edges = [edge for edge in sliced_cfa.edges if edge.line in sliced_cfa.target_lines]
    error_edge = target_edges[-1] if target_edges else (sliced_cfa.edges[-1] if sliced_cfa.edges else None)
    return {
        "entry": f"l{first_edge.source}" if first_edge else None,
        "error": f"l{error_edge.target}" if error_edge else None,
        "kept_lines": sorted(sliced_cfa.kept_lines),
        "data_relevant_lines": sorted(sliced_cfa.data_relevant_lines),
        "reachability_relevant_branches": sorted(sliced_cfa.reachability_relevant_branches),
        "target_lines": sorted(sliced_cfa.target_lines),
        "edges": [edge_to_json(edge) for edge in sliced_cfa.edges],
    }


def cfa_edges_to_json(edges: list[CFAEdge], metadata: dict[str, object] | None = None) -> dict[str, object]:
    first_edge = edges[0] if edges else None
    last_edge = edges[-1] if edges else None
    data = {
        "entry": f"l{first_edge.source}" if first_edge else None,
        "error": f"l{last_edge.target}" if last_edge else None,
        "edges": [edge_to_json(edge) for edge in edges],
    }
    if metadata:
        data.update(metadata)
    return data


def write_text_with_parent(output_path: Path, text: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def write_sliced_cfa_json(sliced_cfa: SlicedCFA, output_path: Path) -> None:
    write_text_with_parent(output_path, json.dumps(sliced_cfa_to_json(sliced_cfa), indent=2))


def write_edges_cfa_json(edges: list[CFAEdge], output_path: Path, metadata: dict[str, object] | None = None) -> None:
    write_text_with_parent(output_path, json.dumps(cfa_edges_to_json(edges, metadata), indent=2))


def is_structural_c_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("#"):
        return True
    if stripped in {"{", "}", "} else {", "else {", "else"}:
        return True
    if re.match(r"^\s*(?:[A-Za-z_][\w\s\*]*\s+)+[A-Za-z_]\w*\s*\([^;]*\)\s*\{?\s*$", line):
        return True
    return False


def scan_c_blocks(lines: list[str]) -> tuple[dict[int, dict[str, object]], dict[int, list[int]], dict[int, int], set[int]]:
    blocks: dict[int, dict[str, object]] = {0: {"parent": None, "open": None, "close": None}}
    line_opens: dict[int, list[int]] = {}
    line_context: dict[int, int] = {}
    top_level_prefix: set[int] = set()
    stack = [0]
    next_block = 1
    seen_function_body = False

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        line_context[lineno] = stack[-1]
        if not seen_function_body and stack == [0]:
            top_level_prefix.add(lineno)

        if re.match(r"^\s*}\s*else\s*{\s*$", line):
            if len(stack) > 1:
                closed = stack.pop()
                blocks[closed]["close"] = lineno
            block_id = next_block
            next_block += 1
            blocks[block_id] = {"parent": stack[-1], "open": lineno, "close": None}
            line_opens.setdefault(lineno, []).append(block_id)
            stack.append(block_id)
            continue

        closes_first = len(re.findall(r"}", line))
        if stripped.startswith("}"):
            for _ in range(closes_first):
                if len(stack) > 1:
                    closed = stack.pop()
                    blocks[closed]["close"] = lineno
            closes_first = 0

        opens = len(re.findall(r"{", line))
        for _ in range(opens):
            block_id = next_block
            next_block += 1
            blocks[block_id] = {"parent": stack[-1], "open": lineno, "close": None}
            line_opens.setdefault(lineno, []).append(block_id)
            stack.append(block_id)
            seen_function_body = True

        for _ in range(closes_first):
            if len(stack) > 1:
                closed = stack.pop()
                blocks[closed]["close"] = lineno

    return blocks, line_opens, line_context, top_level_prefix


def required_structural_lines(lines: list[str], kept_lines: set[int]) -> dict[int, str]:
    blocks, line_opens, line_context, top_level_prefix = scan_c_blocks(lines)
    kept_blocks: set[int] = set()
    output: dict[int, str] = {}

    def mark_block_and_ancestors(block_id: int) -> None:
        while block_id and block_id not in kept_blocks:
            kept_blocks.add(block_id)
            parent = blocks[block_id]["parent"]
            block_id = parent if isinstance(parent, int) else 0

    for lineno in kept_lines:
        if 1 <= lineno <= len(lines):
            output[lineno] = lines[lineno - 1]
            mark_block_and_ancestors(line_context.get(lineno, 0))
            for opened in line_opens.get(lineno, []):
                mark_block_and_ancestors(opened)

    changed = True
    while changed:
        changed = False
        for block_id in list(kept_blocks):
            block = blocks[block_id]
            for key in ("open", "close"):
                line_no = block[key]
                if isinstance(line_no, int) and line_no not in output:
                    output[line_no] = lines[line_no - 1]
                    changed = True
            parent = block["parent"]
            if isinstance(parent, int) and parent and parent not in kept_blocks:
                kept_blocks.add(parent)
                changed = True

    for lineno in sorted(top_level_prefix):
        output.setdefault(lineno, lines[lineno - 1])

    transformed: dict[int, str] = {}
    for lineno, line in output.items():
        if re.match(r"^\s*}\s*else\s*{\s*$", line):
            opened_blocks = line_opens.get(lineno, [])
            opens_kept_else = any(block_id in kept_blocks for block_id in opened_blocks)
            closes_kept_block = any(
                block.get("close") == lineno and block_id in kept_blocks
                for block_id, block in blocks.items()
            )
            if opens_kept_else:
                transformed[lineno] = line
            elif closes_kept_block:
                indent = re.match(r"\s*", line).group(0)
                transformed[lineno] = f"{indent}}}"
        else:
            transformed[lineno] = line
    return transformed


def write_sliced_c(c_path: Path, sliced_cfa: SlicedCFA, output_path: Path) -> None:
    lines = c_path.read_text(encoding="utf-8").splitlines()
    kept_by_line = required_structural_lines(lines, sliced_cfa.kept_lines)
    write_text_with_parent(output_path, "\n".join(kept_by_line[lineno] for lineno in sorted(kept_by_line)) + "\n")


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


def keep_segment_smt(segment: WaypointSegment, smt_result: SmtResult) -> bool:
    if segment.waypoint_type == "target":
        return True
    if segment.line is None:
        return True
    return segment.line in smt_result.necessary_branches or segment.line in smt_result.unknown_branches


def strip_waypoint_block(lines: list[str], key: str) -> list[str]:
    out: list[str] = []
    idx = 0
    pattern = re.compile(rf"^(\s*){re.escape(key)}:\s*$")
    while idx < len(lines):
        match = pattern.match(lines[idx])
        if not match:
            out.append(lines[idx])
            idx += 1
            continue
        indent = len(match.group(1))
        idx += 1
        while idx < len(lines):
            stripped = lines[idx].strip()
            current_indent = len(lines[idx]) - len(lines[idx].lstrip(" "))
            if stripped and current_indent <= indent:
                break
            idx += 1
    return out


def reduce_segment_by_mode(segment: WaypointSegment, relevant: bool, mode: str) -> WaypointSegment | None:
    if segment.waypoint_type == "target":
        return segment
    if relevant or segment.line is None:
        return segment
    if mode == "all":
        return None
    lines = strip_waypoint_block(segment.lines, "constraint")
    if mode == "match":
        lines = strip_waypoint_block(lines, "location")
    reduced = WaypointSegment(lines=lines)
    reduced.waypoint_type = segment.waypoint_type
    reduced.action = segment.action
    reduced.line = segment.line
    reduced.function = segment.function
    return reduced


def reduce_witness_by_suspicious_edges(
    prefix: list[str],
    segments: list[WaypointSegment],
    suspicious_lines: set[int],
    output_path: Path,
    mode: str,
) -> list[WaypointSegment]:
    reduced: list[WaypointSegment] = []
    for segment in segments:
        relevant = segment.line in suspicious_lines
        new_segment = reduce_segment_by_mode(segment, relevant, mode)
        if new_segment is not None:
            reduced.append(new_segment)
    reduced = cleanup_segments(reduced)
    write_text_with_parent(output_path, "".join(prefix + [line for seg in reduced for line in seg.lines]))
    return reduced


def derived_reduction_output_path(base: Path, mode: str) -> Path:
    if base.suffix:
        return base.with_name(f"{base.stem}.{mode}{base.suffix}")
    return base.with_name(f"{base.name}.{mode}.yml")


def localization_debug_json(
    localization: LocalizationResult,
    suspicious_edges: list[CFAEdge],
    reduction_results: dict[str, dict[str, object]],
) -> dict[str, object]:
    pi_formulas = [item["formula"] for item in localization.pi]
    psi_formulas = list(localization.precondition)
    safe_formula = localization.safe_postcondition or "true"
    suspicious_pi = suspicious_pi_items(localization)
    return {
        "method": localization.method,
        "cfa_fault_localization": {
            "input_values": input_values_from_formulas(psi_formulas, localization.trace_formula),
            "postcondition": {
                "error_guard": localization.error_guard["formula"] if localization.error_guard else None,
                "error_guard_guards": localization.error_guard.get("guards", []) if isinstance(localization.error_guard, dict) else [],
                "safe_postcondition": safe_formula,
                "meaning": "safe_postcondition forbids reaching the target; error_guard is the path condition that reaches it",
            },
            "pi": [
                {
                    "index": item["index"],
                    "edge": item["edge"],
                    "formula": item["formula"],
                }
                for item in localization.pi
            ],
            "unsat_check": {
                "query": "input_values AND pi AND safe_postcondition",
                "solver_result": localization.solver_result,
                "why_suspicious": "Z3 returned UNSAT. The tracked pi formulas whose literals are in the unsat core are suspicious; their CFA edges are reported below.",
                "unsat_core_literals": localization.unsat_core_literals,
                "suspicious_pi": suspicious_pi,
            },
        },
        "algorithm": "CFA-based unsat-core localization. Witness is used only earlier to obtain the sliced CFA/path; this report explains the CFA formulas.",
        "solver_result": localization.solver_result,
        "fallback_used": localization.fallback_used,
        "fallback_reason": localization.fallback_reason,
        "suspicious_edges": [f"e{edge.edge_id}" for edge in suspicious_edges],
        "suspicious_locations": [
            edge_summary_json(edge)
            for edge in suspicious_edges
        ],
        "unknown_lines": sorted(localization.unknown_edges),
        "trace_formula_edges": localization.trace_formula,
        "reduction_algorithms": {
            "state": "For irrelevant waypoints, keep location but remove constraint.",
            "match": "For irrelevant waypoints, remove both location and constraint.",
            "all": "For irrelevant waypoints, delete the waypoint; always keep target/error waypoints.",
        },
        "reduction_results": reduction_results,
    }


def write_smt_report(
    localization: LocalizationResult,
    suspicious_edges: list[CFAEdge],
    reduction_results: dict[str, dict[str, object]],
    output_path: Path,
) -> None:
    loc = localization_debug_json(localization, suspicious_edges, reduction_results)
    cfa_loc = loc["cfa_fault_localization"]
    lines: list[str] = []

    lines.append("# SMT Fault Localization Report")
    lines.append("")
    lines.append(f"Method: `{localization.method}`")
    lines.append(f"Solver result: `{localization.solver_result}`")
    lines.append(f"Fallback used: `{str(localization.fallback_used).lower()}`")
    if localization.fallback_reason:
        lines.append(f"Fallback reason: {localization.fallback_reason}")
    lines.append("")

    def readable_statement_formula(edge: dict[str, object], formula: str) -> str:
        stmt = str(edge.get("statement", ""))
        if "__VERIFIER_nondet" in stmt and edge.get("line") is not None:
            assigned = None
            for item in cfa_loc["input_values"]:
                item_edge = item.get("edge") or {}
                if item_edge.get("line") == edge.get("line"):
                    name = re.sub(r"_\d+$", "", str(item.get("assigned_to", "")))
                    assigned = f"{name} = {item.get('decimal')}"
                    break
            return assigned or stmt
        if stmt.startswith("if "):
            cond = LineCParser._if_condition(stmt) or stmt
            if formula.lstrip().startswith("(not "):
                return f"!({cond})"
            return cond
        if stmt.endswith(";"):
            return stmt[:-1]
        return stmt or formula

    check = cfa_loc["unsat_check"]
    post = cfa_loc["postcondition"]
    guard_items = []
    error_guard_obj = localization.error_guard or {}
    if isinstance(error_guard_obj, dict):
        guard_items = error_guard_obj.get("guards", []) or []
    readable_guards = []
    for item in guard_items:
        edge = item.get("edge", {})
        readable_guards.append(
            {
                "index": item.get("index"),
                "line": edge.get("line", "?"),
                "condition": readable_statement_formula(edge, str(item.get("formula", ""))),
            }
        )
    readable_guard = " && ".join(item["condition"] for item in readable_guards) if readable_guards else str(post["error_guard"])

    lines.append("## 1. Evidence Trace")
    lines.append("")
    evidence_items: list[dict[str, object]] = []
    for item in check["suspicious_pi"]:
        edge = item["edge"]
        evidence_items.append(
            {
                "part": "SUSPICIOUS",
                "trace_index": item.get("trace_index", item.get("index")),
                "index": item.get("index"),
                "line": edge.get("line", "?"),
                "text": readable_statement_formula(edge, str(item["formula"])),
            }
        )
    for item in cfa_loc["input_values"]:
        symbol_name = str(item.get("symbol", ""))
        assigned_to = symbol_name if symbol_name.startswith("input_") else item.get("assigned_to", "<unknown>")
        clean_name = re.sub(r"_\d+$", "", str(assigned_to))
        edge = item.get("edge") or {}
        evidence_items.append(
            {
                "part": "PRE",
                "trace_index": item.get("trace_index", 10**9),
                "index": None,
                "line": edge.get("line", "?"),
                "text": f"{clean_name} = {item.get('decimal', '<unknown>')}",
            }
        )
    for item in readable_guards:
        evidence_items.append(
            {
                "part": "POST",
                "trace_index": item.get("index", 10**9),
                "index": None,
                "line": item.get("line", "?"),
                "text": item.get("condition", ""),
            }
        )
    if not evidence_items and suspicious_edges:
        for edge in suspicious_edges:
            evidence_items.append(
                {
                    "part": "SUSPICIOUS",
                    "trace_index": 10**9,
                    "index": None,
                    "line": edge.line,
                    "text": edge.text,
                }
            )
    for item in compact_evidence_items(evidence_items):
        count = int(item["count"])
        trace_summary = summarize_indexes(item.get("trace_indexes", []), "t")
        index_summary = summarize_report_indexes(item.get("indexes", []))
        suffix_parts = [trace_summary]
        if index_summary:
            suffix_parts.append(index_summary)
        suffix = ", ".join(part for part in suffix_parts if part)
        repeat = "" if count == 1 else f" x {count}"
        lines.append(f"- [{item['part']}] line {item['line']}: `{item['text']}`{repeat} [{suffix}]")
    lines.append("- [POST] target: `target/reach_error is not reached`")
    lines.append("")

    lines.append("## 2. Postcondition Detail")
    lines.append("")
    lines.append("Error guard:")
    lines.append("")
    if readable_guards:
        lines.append("All of these path guards must hold to reach the target:")
        lines.append("")
        lines.append("```text")
        for item in readable_guards:
            lines.append(f"line {item['line']}: {item['condition']}")
        lines.append("```")
    elif localization.error_guard is None:
        lines.append("```text")
        lines.append("unavailable: full error trace was not SAT")
        lines.append("```")
    else:
        lines.append(f"```text\n{readable_guard}\n```")
    lines.append("")
    lines.append("Safe postcondition:")
    lines.append("")
    if readable_guards:
        lines.append("```text")
        lines.append("target/reach_error is not reached")
        lines.append("equivalently: at least one path guard above is false in its SSA state")
        lines.append("```")
    elif localization.error_guard is None:
        lines.append("```text")
        lines.append("unavailable: full error trace was not SAT")
        lines.append("```")
    else:
        lines.append(f"```text\n!({readable_guard})\n```")
    lines.append("")

    lines.append("## 3. UNSAT Check")
    lines.append("")
    lines.append("Query:")
    lines.append("")
    lines.append("```text")
    lines.append(str(check["query"]))
    lines.append("```")
    lines.append("")
    lines.append(f"Result: `{check['solver_result']}`")
    lines.append("")
    lines.append("Why suspicious:")
    lines.append("")
    if localization.fallback_used:
        lines.append("The precise UNSAT-core localization was not available, so the report uses the fallback suspicious CFA edges listed below.")
    elif not check["suspicious_pi"] and localization.solver_result == "unsat":
        lines.append("No CFA transition in pi is suspicious: the contradiction is already between the fixed input values and the safe postcondition.")
    else:
        lines.append(str(check["why_suspicious"]))
    lines.append("")
    lines.append("UNSAT core literals:")
    lines.append("")
    lines.append("```text")
    lines.extend(str(lit) for lit in check["unsat_core_literals"])
    lines.append("```")
    lines.append("")

    lines.append("## 4. Pi Trace Formula")
    lines.append("")
    for item in cfa_loc["pi"]:
        edge = item["edge"]
        readable = readable_statement_formula(edge, str(item["formula"]))
        lines.append(f"pi_{item['index']}: line {edge['line']}: `{edge['statement']}` => `{readable}`")
    lines.append("")

    lines.append("## 5. Suspicious Pi Formulas")
    lines.append("")
    for item in check["suspicious_pi"]:
        edge = item["edge"]
        readable = readable_statement_formula(edge, str(item["formula"]))
        lines.append(f"- pi_{item['index']}: line {edge['line']}: `{edge['statement']}` => `{readable}`")
    lines.append("")

    lines.append("## 6. Reduction Outputs")
    lines.append("")
    for mode, result in reduction_results.items():
        lines.append(f"- `{mode}`: {result['waypoints']} waypoints -> `{result['output']}`")
    lines.append("")

    write_text_with_parent(output_path, "\n".join(lines))


def compute_sliced_cfa(c_path: Path, witness_path: Path) -> tuple[CFA, SlicedCFA, list[str], list[WaypointSegment]]:
    cfa = parse_c(c_path)
    prefix, segments = parse_witness(witness_path)
    target = find_target_segment(segments)
    initial_vars, initial_marked = initial_relevant_vars(segments, cfa, target)
    marked_lines, reachability_branches = backward_slice(cfa, initial_vars, initial_marked)
    target_lines = {target.line} if target and target.line is not None else set()
    sliced_cfa = build_sliced_cfa(cfa, marked_lines, reachability_branches, target_lines)
    return cfa, sliced_cfa, prefix, segments


def write_sliced_witness(
    prefix: list[str],
    segments: list[WaypointSegment],
    original_cfa: CFA,
    sliced_cfa: SlicedCFA,
    output_path: Path,
) -> list[WaypointSegment]:
    kept = [
        segment
        for segment in segments
        if keep_segment_for_sliced_cfa(segment, original_cfa, sliced_cfa)
    ]
    kept = cleanup_segments(kept)
    write_text_with_parent(output_path, "".join(prefix + [line for seg in kept for line in seg.lines]))
    return kept


def slice_witness(c_path: Path, witness_path: Path, output_path: Path) -> tuple[int, int, int, int]:
    cfa, sliced_cfa, prefix, segments = compute_sliced_cfa(c_path, witness_path)
    kept = write_sliced_witness(prefix, segments, cfa, sliced_cfa, output_path)
    return (
        len(segments),
        len(kept),
        len(sliced_cfa.data_relevant_lines),
        len(sliced_cfa.reachability_relevant_branches),
    )


def slice_witness_smt(c_path: Path, witness_path: Path, output_path: Path) -> tuple[int, int, int, int, int]:
    prefix, segments = parse_witness(witness_path)
    smt_result = smt_branch_prune(c_path, segments)
    kept = [segment for segment in segments if keep_segment_smt(segment, smt_result)]
    kept = cleanup_segments(kept)
    write_text_with_parent(output_path, "".join(prefix + [line for seg in kept for line in seg.lines]))
    return (
        len(segments),
        len(kept),
        len(smt_result.necessary_branches),
        len(smt_result.removable_branches),
        len(smt_result.unknown_branches),
    )


def run_sliced_then_smt(
    c_path: Path,
    witness_path: Path,
    sliced_witness_path: Path,
    reduced_witness_path: Path,
    reduction_mode: str,
    sliced_cfa_path: Path | None = None,
    sliced_c_path: Path | None = None,
    suspicious_cfa_path: Path | None = None,
    suspicious_edges_path: Path | None = None,
    smt_report_path: Path | None = None,
    stats_path: Path | None = None,
) -> dict[str, object]:
    cfa, sliced_cfa, prefix, segments = compute_sliced_cfa(c_path, witness_path)
    sliced_segments = write_sliced_witness(prefix, segments, cfa, sliced_cfa, sliced_witness_path)
    if sliced_cfa_path:
        write_sliced_cfa_json(sliced_cfa, sliced_cfa_path)
    if sliced_c_path:
        write_sliced_c(c_path, sliced_cfa, sliced_c_path)

    path, formula_branch_choices = build_witness_driven_path(c_path, sliced_cfa, sliced_segments)
    localization = localize_suspicious_edges_unsat_core(path, sliced_segments, formula_branch_choices)
    suspicious_edges = [edge for edge in sliced_cfa.edges if edge.line in localization.suspicious_edges]

    reduction_results: dict[str, dict[str, object]] = {}
    reduced_segments_by_mode: dict[str, list[WaypointSegment]] = {}
    for mode in ("state", "match", "all"):
        mode_output = reduced_witness_path if mode == reduction_mode else derived_reduction_output_path(reduced_witness_path, mode)
        reduced_segments = reduce_witness_by_suspicious_edges(
            prefix,
            sliced_segments,
            localization.suspicious_edges,
            mode_output,
            mode,
        )
        reduced_segments_by_mode[mode] = reduced_segments
        reduction_results[mode] = {
            "output": str(mode_output),
            "waypoints": len(reduced_segments),
        }

    if suspicious_cfa_path:
        write_edges_cfa_json(
            suspicious_edges,
            suspicious_cfa_path,
            {
                "kind": "suspicious_cfa",
                "fallback_used": localization.fallback_used,
                "unknown_lines": sorted(localization.unknown_edges),
            },
        )
    if suspicious_edges_path:
            write_text_with_parent(
                suspicious_edges_path,
                json.dumps(localization_debug_json(localization, suspicious_edges, reduction_results), indent=2),
            )
    if smt_report_path:
        write_smt_report(localization, suspicious_edges, reduction_results, smt_report_path)
    stats = {
        "original_cfa_edges": len(cfa.edges),
        "sliced_cfa_edges": len(sliced_cfa.edges),
        "suspicious_cfa_edges": len(suspicious_edges),
        "original_waypoints": len(segments),
        "sliced_waypoints": len(sliced_segments),
        "reduced_waypoints": len(reduced_segments_by_mode[reduction_mode]),
        "fault_localization": "unsat-core",
        "reduction_mode": reduction_mode,
        "reduction_results": reduction_results,
        "fallback_used": localization.fallback_used,
        "unknown_edges": len(localization.unknown_edges),
    }
    if stats_path:
        write_text_with_parent(stats_path, json.dumps(stats, indent=2))
    return stats


def write_cfa_dot(cfa: CFA, output_path: Path) -> None:
    lines = ["digraph CFA {\n", "  node [shape=circle];\n"]
    for node in cfa.nodes.values():
        lines.append(f'  n{node.node_id} [label="{node.node_id}\\n{node.function}:{node.line}"];\n')
    for edge in cfa.edges:
        label = edge.text.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'  n{edge.source} -> n{edge.target} [label="{edge.line}: {label}"];\n')
    lines.append("}\n")
    write_text_with_parent(output_path, "".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description="Slice a CPAchecker witness using C DEF/USE dependencies.")
    parser.add_argument("program", type=Path, help="C program P")
    parser.add_argument("witness", type=Path, help="CPAchecker witness W")
    parser.add_argument("-o", "--output", type=Path, help="Output sliced witness W'")
    parser.add_argument("--mode", choices=("cfa", "smt", "sliced-smt"), default="cfa", help="Slicing algorithm")
    parser.add_argument("--reduction-mode", choices=("state", "match", "all"), default="all", help="Witness reduction mode for sliced-smt")
    parser.add_argument("--reduced-output", type=Path, help="Reduced witness output for sliced-smt")
    parser.add_argument("--dump-cfa-dot", type=Path, help="Write the constructed CFA as Graphviz DOT")
    parser.add_argument("--dump-sliced-cfa", type=Path, help="Write the dependency-sliced CFA as JSON")
    parser.add_argument("--dump-sliced-c", type=Path, help="Write a line-stable sliced C program")
    parser.add_argument("--dump-suspicious-cfa", type=Path, help="Write suspicious CFA edges as JSON")
    parser.add_argument("--dump-suspicious-edges", type=Path, help="Write suspicious edge summary as JSON")
    parser.add_argument("--dump-smt-report", type=Path, help="Write a human-readable SMT fault localization report")
    parser.add_argument("--dump-stats", type=Path, help="Write pipeline stats as JSON")
    args = parser.parse_args()

    output = args.output
    if output is None:
        output = args.witness.with_name(args.witness.stem + ".sliced.yml")

    if args.dump_cfa_dot:
        write_cfa_dot(parse_c(args.program), args.dump_cfa_dot)

    if args.mode == "sliced-smt":
        reduced_output = args.reduced_output or args.witness.with_name(args.witness.stem + ".reduced.yml")
        stats = run_sliced_then_smt(
            args.program,
            args.witness,
            output,
            reduced_output,
            args.reduction_mode,
            sliced_cfa_path=args.dump_sliced_cfa,
            sliced_c_path=args.dump_sliced_c,
            suspicious_cfa_path=args.dump_suspicious_cfa,
            suspicious_edges_path=args.dump_suspicious_edges,
            smt_report_path=args.dump_smt_report,
            stats_path=args.dump_stats,
        )
        print(
            f"{args.witness.name}: sliced {stats['sliced_waypoints']}/{stats['original_waypoints']} waypoints, "
            f"reduced to {stats['reduced_waypoints']} waypoints, "
            f"{stats['suspicious_cfa_edges']} suspicious CFA edges -> {reduced_output}"
        )
    elif args.mode == "smt":
        before, after, necessary, removable, unknown = slice_witness_smt(args.program, args.witness, output)
        print(
            f"{args.witness.name}: kept {after}/{before} segments, "
            f"{necessary} SMT-necessary branches, "
            f"{removable} removable branches, "
            f"{unknown} unknown/conservative branches -> {output}"
        )
    else:
        cfa, sliced_cfa, prefix, segments = compute_sliced_cfa(args.program, args.witness)
        kept = write_sliced_witness(prefix, segments, cfa, sliced_cfa, output)
        if args.dump_sliced_cfa:
            write_sliced_cfa_json(sliced_cfa, args.dump_sliced_cfa)
        if args.dump_sliced_c:
            write_sliced_c(args.program, sliced_cfa, args.dump_sliced_c)
        print(
            f"{args.witness.name}: kept {len(kept)}/{len(segments)} segments, "
            f"marked {len(sliced_cfa.data_relevant_lines)} data/control C locations, "
            f"{len(sliced_cfa.reachability_relevant_branches)} reachability branches -> {output}"
        )
        if args.dump_sliced_cfa:
            print(f"sliced CFA JSON -> {args.dump_sliced_cfa}")
        if args.dump_sliced_c:
            print(f"sliced C -> {args.dump_sliced_c}")
    if args.dump_cfa_dot:
        print(f"CFA DOT -> {args.dump_cfa_dot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
