# Sliced-CFA Then SMT Fault Localization Pipeline

## Goal

Input:

```text
original.c
original.witness.yml
```

Output:

```text
sliced.c
sliced.witness.yml
sliced.cfa.json
reduced.witness.yml
suspicious.cfa.json
suspicious_edges.json
stats.json
```

The key idea is:

```text
First build a dependency-sliced CFA.
Then run SMT fault localization on the sliced CFA and sliced witness.
```

The final suspicious result must include a suspicious CFA, because the YAML
witness mostly records branch waypoints. Non-branch suspicious transitions may
not appear directly in the witness, so they must be represented in
`suspicious.cfa.json`.

---

## 1. Build Original CFA

Parse `original.c` with `pycparser`.

Build:

```python
@dataclass
class CFAEdge:
    id: str
    source: str
    target: str
    file: str | None
    line: int | None
    function: str | None
    statement: str
    kind: str
    defs: set[str]
    uses: set[str]
    controls: list[int]
```

The CFA contains:

```python
@dataclass
class CFA:
    edges: list[CFAEdge]
    edge_by_line: dict[int, CFAEdge]
    entry: str
    error: str
    branch_sides: dict[int, tuple[set[int], set[int]]]
    loop_headers: set[int]
```

Supported statement kinds:

```text
stmt
branch
return
break
continue
target
```

For each edge, compute:

```text
DEF(edge)
USE(edge)
control dependency
reachability behavior
```

---

## 2. Parse Original Witness

Read `original.witness.yml`.

Extract waypoint segments while preserving raw YAML text.

For each waypoint:

```python
@dataclass
class Waypoint:
    raw_segment: list[str]
    type: str | None
    action: str | None
    file: str | None
    line: int | None
    function: str | None
    constraint: str | None
```

Important waypoint kinds:

```text
branching
assumption
target
```

Target waypoint is always preserved.

---

## 3. Dependency Slicing

Run backward dependency slicing on the original CFA.

Maintain:

```text
RelevantVars
ReachabilityRelevantBranches
MarkedEdges
```

Initialize from target:

```text
assert(cond):
    RelevantVars = vars(cond)

reach_error() / __VERIFIER_error():
    RelevantVars = vars(nearest controlling branch condition)

otherwise:
    RelevantVars = {}
```

Backward rule for data dependency:

```text
for edge in reversed(CFA.edges):
    if DEF(edge) intersects RelevantVars:
        mark edge
        RelevantVars = RelevantVars - DEF(edge) + USE(edge)
```

Branch rule:

```text
if edge.kind == branch:
    if USE(edge) intersects RelevantVars:
        mark edge
        RelevantVars = RelevantVars union USE(edge)

    if edge controls a marked edge:
        mark edge
        RelevantVars = RelevantVars union USE(edge)
```

Reachability rule:

```text
if one branch side terminates / returns / aborts / exits / assumes false
and the other side can still reach target:
    mark branch as reachability-relevant
    RelevantVars = RelevantVars union USE(branch condition)
```

Loop-transfer rule:

```text
break / continue are path-affecting transfers.

if break or continue is controlled by branch b:
    mark b reachability-relevant

if continue is inside loop header h:
    mark h reachability-relevant
```

---

## 4. Build Sliced CFA

Create a new CFA:

```python
@dataclass
class SlicedCFA:
    original: CFA
    edges: list[CFAEdge]
    edge_by_line: dict[int, CFAEdge]
    kept_lines: set[int]
    data_relevant_lines: set[int]
    reachability_relevant_branches: set[int]
```

Keep an edge if:

```text
edge is marked data/control relevant
or edge is reachability-relevant branch
or edge is target edge
```

The sliced CFA is the main artifact for later SMT fault localization.

---

## 5. Generate Sliced C

Use `SlicedCFA.kept_lines`.

Output:

```text
sliced.c
```

Basic rule:

```text
keep original line if line in kept_lines
keep function declarations / braces needed for syntactic validity
keep target function, e.g. reach_error()
replace removed executable lines with blank lines or comments
```

Recommended conservative implementation:

```text
Do not renumber lines.
Keep line numbers stable so witness locations still match.
Removed statements become:
    /* sliced away */
```

This keeps CPAchecker witness line mappings valid.

---

## 6. Generate Sliced Witness

Use the original witness plus `SlicedCFA`.

Keep waypoint if:

```text
waypoint.type == target
or waypoint location matches an edge in SlicedCFA
or waypoint location cannot be mapped
```

Drop waypoint if:

```text
location maps to original CFA
but does not map to SlicedCFA
```

Cleanup:

```text
delete empty segments
delete avoid-only non-target segments
preserve original waypoint order
ensure final waypoint is target
```

Output:

```text
sliced.witness.yml
```

---

## 7. Build Witness-Guided Path on Sliced CFA

Input:

```text
SlicedCFA
sliced.witness.yml
```

Output:

```text
cex_W = [e0, e1, ..., en]
```

Algorithm:

```python
def find_witness_path(sliced_cfa, sliced_witness):
    waypoints = extract_waypoints(sliced_witness)
    path = []
    current = sliced_cfa.entry

    for wp in waypoints:
        if wp has no location:
            continue

        find a reachable CFA edge e from current such that:
            e.file == wp.location.file_name
            e.line == wp.location.line

        append BFS path from current to e.source
        append e
        current = e.target

        if current == sliced_cfa.error:
            break

    append BFS path from current to sliced_cfa.error
    return path
```

Why CFA is needed:

```text
The witness may only contain branch waypoints.
Assignments and assumptions may be absent from the witness.
The CFA supplies the missing non-branch transitions.
```

---

## 8. Encode Path as SMT Trace Formula

For each edge:

```text
edge_i -> phi_i
```

Keep mapping:

```text
phi_i <-> edge_i
```

Use SSA variables.

Examples:

```c
x = x + 1;
```

becomes:

```text
x_1 = x_0 + 1
```

```c
assume(x > 0);
```

becomes:

```text
x_0 > 0
```

```c
if (x > 0) followed as true
```

becomes:

```text
x_0 > 0
```

```c
if (x > 0) followed as false
```

becomes:

```text
not (x_0 > 0)
```

Unsupported expressions:

```text
encode as True
or mark the edge as unknown/conservative
```

---

## 9. Build Fault-Localization Formula

Let:

```text
TF(cex_W) = phi_0 and phi_1 and ... and phi_n
```

First check:

```text
TF(cex_W) is SAT
```

Use the SAT model to fix nondet/input assignments:

```text
psi = precondition from model
```

Find the final error guard:

```text
error_guard = last condition / assume / branch before target
```

Then:

```text
pi = all formulas before error_guard
safe_phi = not error_guard
```

The suspicious-edge search works over:

```text
psi
pi
safe_phi
```

---

## 10. Find Suspicious Edges

### 10.1 Unsat-Core Baseline

Use:

```text
psi and pi and safe_phi
```

Track each formula in `pi`:

```python
solver.add(psi)
solver.add(safe_phi)

for i, (phi_i, edge_i) in enumerate(pi):
    lit_i = Bool(f"a_{i}")
    solver.assert_and_track(phi_i, lit_i)
```

If:

```text
solver.check() == unsat
```

then:

```python
core = solver.unsat_core()
suspicious_edges = {
    edge_i
    for lit_i in core
}
```

If SAT or unknown:

```text
fallback to last 1 to 3 edges before target
```

### 10.2 MinUnsat Version

Find a minimal subset `f`:

```text
f subset pi
psi and f and safe_phi is UNSAT
```

Then:

```text
suspicious_edges = edges(f)
```

This is more precise but more expensive.

### 10.3 MaxSat Version

Find a minimal subset `f`:

```text
f subset pi
psi and (pi - f) and safe_phi is SAT
```

Then:

```text
suspicious_edges = edges(f)
```

This means removing `f` allows the same input to satisfy the safe condition.

---

## 11. Build Suspicious CFA

This output is required.

Reason:

```text
The witness usually records branch waypoints only.
Suspicious operations may be assignments, assumes, returns, or other CFA edges.
They might not appear in the YAML witness.
```

Therefore generate:

```text
suspicious.cfa.json
```

Containing:

```json
{
  "entry": "l1",
  "error": "l_err",
  "edges": [
    {
      "id": "e42",
      "source": "l41",
      "target": "l42",
      "file": "sliced.c",
      "line": 120,
      "function": "main",
      "statement": "x = x + 1;",
      "kind": "stmt",
      "defs": ["x"],
      "uses": ["x"]
    }
  ]
}
```

Also output:

```text
suspicious_edges.json
```

Example:

```json
{
  "suspicious_edges": ["e42", "e51"],
  "suspicious_locations": [
    {"file": "sliced.c", "line": 120},
    {"file": "sliced.c", "line": 133}
  ]
}
```

---

## 12. Reduce Witness Using Suspicious CFA

A waypoint is relevant if:

```text
waypoint location matches some edge in suspicious CFA
```

But because witness may only contain branches:

```text
If a suspicious edge has no matching witness waypoint,
it still remains visible in suspicious.cfa.json.
```

Reduction modes:

### state

For irrelevant waypoints:

```text
keep location
remove constraint
```

### match

For irrelevant waypoints:

```text
remove location
remove constraint
```

### all

For irrelevant waypoints:

```text
delete waypoint
```

Always keep:

```text
target
violation
error
unmapped waypoint, if conservative mode is enabled
```

Output:

```text
reduced.witness.yml
```

---

## 13. Final Outputs

Required:

```text
sliced.c
sliced.witness.yml
sliced.cfa.json
reduced.witness.yml
suspicious.cfa.json
suspicious_edges.json
stats.json
```

`stats.json` should include:

```json
{
  "original_cfa_edges": 1000,
  "sliced_cfa_edges": 120,
  "suspicious_cfa_edges": 3,
  "original_waypoints": 100,
  "sliced_waypoints": 20,
  "reduced_waypoints": 5,
  "fault_localization": "unsat-core",
  "reduction_mode": "all"
}
```

---

## 14. End-to-End Summary

```text
original.c
original.witness.yml
        |
        v
build original CFA
        |
        v
dependency slicing
        |
        +--> sliced.c
        +--> sliced.cfa.json
        +--> sliced.witness.yml
        |
        v
find witness-guided path on sliced CFA
        |
        v
encode path as SSA SMT trace formula
        |
        v
fault localization
        |
        +--> suspicious_edges.json
        +--> suspicious.cfa.json
        |
        v
reduce sliced witness by suspicious CFA
        |
        v
reduced.witness.yml
```

