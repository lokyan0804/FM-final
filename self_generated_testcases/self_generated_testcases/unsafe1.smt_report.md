# SMT Fault Localization Report

Method: `unsat-core`
Solver result: `unsat`
Fallback used: `false`

## 1. Input Values


## 2. Postcondition

Error guard:

All of these path guards must hold to reach the target:

```text
line 1944: trigger == 55
```

Safe postcondition:

```text
target/reach_error is not reached
equivalently: at least one path guard above is false in its SSA state
```

## 3. Pi Trace Formula

pi_0: line 1933: `int trigger = 0;` => `int trigger = 0`
pi_1: line 1934: `trigger += 1;` => `trigger += 1`
pi_2: line 1935: `trigger += 2;` => `trigger += 2`
pi_3: line 1936: `trigger += 3;` => `trigger += 3`
pi_4: line 1937: `trigger += 4;` => `trigger += 4`
pi_5: line 1938: `trigger += 5;` => `trigger += 5`
pi_6: line 1939: `trigger += 6;` => `trigger += 6`
pi_7: line 1940: `trigger += 7;` => `trigger += 7`
pi_8: line 1941: `trigger += 8;` => `trigger += 8`
pi_9: line 1942: `trigger += 9;` => `trigger += 9`
pi_10: line 1943: `trigger += 10;` => `trigger += 10`

## 4. UNSAT Check

Query:

```text
input_values AND pi AND safe_postcondition
```

Result: `unsat`

Why suspicious:

Z3 returned UNSAT. The tracked pi formulas whose literals are in the unsat core are suspicious; their CFA edges are reported below.

UNSAT core literals:

```text
a_1
a_0
a_2
a_3
a_4
a_5
a_6
a_7
a_8
a_9
a_10
```

## 5. Suspicious Pi Formulas

- pi_0: line 1933: `int trigger = 0;` => `int trigger = 0`
- pi_1: line 1934: `trigger += 1;` => `trigger += 1`
- pi_2: line 1935: `trigger += 2;` => `trigger += 2`
- pi_3: line 1936: `trigger += 3;` => `trigger += 3`
- pi_4: line 1937: `trigger += 4;` => `trigger += 4`
- pi_5: line 1938: `trigger += 5;` => `trigger += 5`
- pi_6: line 1939: `trigger += 6;` => `trigger += 6`
- pi_7: line 1940: `trigger += 7;` => `trigger += 7`
- pi_8: line 1941: `trigger += 8;` => `trigger += 8`
- pi_9: line 1942: `trigger += 9;` => `trigger += 9`
- pi_10: line 1943: `trigger += 10;` => `trigger += 10`
## 6. Suspicious CFA Edges

- line 1933: `int trigger = 0;`
- line 1934: `trigger += 1;`
- line 1935: `trigger += 2;`
- line 1936: `trigger += 3;`
- line 1937: `trigger += 4;`
- line 1938: `trigger += 5;`
- line 1939: `trigger += 6;`
- line 1940: `trigger += 7;`
- line 1941: `trigger += 8;`
- line 1942: `trigger += 9;`
- line 1943: `trigger += 10;`

## 7. Reduction Outputs

- `state`: 2 waypoints -> `unsafe1.reduced.witness.state.yml`
- `match`: 2 waypoints -> `unsafe1.reduced.witness.match.yml`
- `all`: 1 waypoints -> `unsafe1.reduced.witness.yml`
