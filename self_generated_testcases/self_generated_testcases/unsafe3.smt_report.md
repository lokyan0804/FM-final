# SMT Fault Localization Report

Method: `unsat-core`
Solver result: `unsat`
Fallback used: `true`
Fallback reason: unsat core did not map to any edge

## 1. Input Values

line 1765: `nondet_1_fresh = 28`
line 1771: `nondet_1_fresh = 43`
line 1777: `nondet_1_fresh = 35`
line 1783: `nondet_1_fresh = 210`
line 1789: `nondet_1_fresh = 121`
line 1795: `nondet_1_fresh = 59`
line 1801: `nondet_1_fresh = 159`
line 1807: `nondet_1_fresh = 238`
line 1813: `nondet_1_fresh = 117`
line 1819: `nondet_1_fresh = 26`
line 1825: `nondet_1_fresh = 152`
line 1831: `nondet_1_fresh = 170`
line 1837: `nondet_1_fresh = 70`
line 1843: `nondet_1_fresh = 64`
line 1849: `nondet_1_fresh = 191`
line 1855: `nondet_1_fresh = 1`
line 1861: `nondet_1_fresh = 16`
line 1867: `nondet_1_fresh = 218`
line 1873: `nondet_1_fresh = 75`
line 1879: `nondet_1_fresh = 183`

## 2. Postcondition

Error guard:

```text
(input_0 ^ 53) == 41 && (input_1 ^ 44) == 7 && (input_2 ^ 99) == 64 && (input_3 ^ 129) == 83 && (input_4 ^ 96) == 25 && (input_5 ^ 57) == 2 && (input_6 ^ 201) == 86 && (input_7 ^ 189) == 83 && (input_8 ^ 87) == 34 && (input_9 ^ 87) == 77 && (input_10 ^ 135) == 31 && (input_11 ^ 138) == 32 && (input_12 ^ 253) == 187 && (input_13 ^ 79) == 15 && (input_14 ^ 233) == 86 && (input_15 ^ 33) == 32 && (input_16 ^ 147) == 131 && (input_17 ^ 158) == 68 && (input_18 ^ 90) == 17 && (input_19 ^ 153) == 46
```

Safe postcondition, i.e. negated error guard:

```text
!((input_0 ^ 53) == 41 && (input_1 ^ 44) == 7 && (input_2 ^ 99) == 64 && (input_3 ^ 129) == 83 && (input_4 ^ 96) == 25 && (input_5 ^ 57) == 2 && (input_6 ^ 201) == 86 && (input_7 ^ 189) == 83 && (input_8 ^ 87) == 34 && (input_9 ^ 87) == 77 && (input_10 ^ 135) == 31 && (input_11 ^ 138) == 32 && (input_12 ^ 253) == 187 && (input_13 ^ 79) == 15 && (input_14 ^ 233) == 86 && (input_15 ^ 33) == 32 && (input_16 ^ 147) == 131 && (input_17 ^ 158) == 68 && (input_18 ^ 90) == 17 && (input_19 ^ 153) == 46)
```

## 3. Pi Trace Formula

pi_0: line 1767: `input_0 = input_0 ^ 9577;` => `input_0 = input_0 ^ 9577`
pi_1: line 1773: `input_1 = input_1 ^ 8112;` => `input_1 = input_1 ^ 8112`
pi_2: line 1779: `input_2 = input_2 ^ 5422;` => `input_2 = input_2 ^ 5422`
pi_3: line 1785: `input_3 = input_3 ^ 6210;` => `input_3 = input_3 ^ 6210`
pi_4: line 1791: `input_4 = input_4 ^ 6412;` => `input_4 = input_4 ^ 6412`
pi_5: line 1797: `input_5 = input_5 ^ 1280;` => `input_5 = input_5 ^ 1280`
pi_6: line 1803: `input_6 = input_6 ^ 7705;` => `input_6 = input_6 ^ 7705`
pi_7: line 1809: `input_7 = input_7 ^ 6176;` => `input_7 = input_7 ^ 6176`
pi_8: line 1815: `input_8 = input_8 ^ 4002;` => `input_8 = input_8 ^ 4002`
pi_9: line 1821: `input_9 = input_9 ^ 882;` => `input_9 = input_9 ^ 882`
pi_10: line 1827: `input_10 = input_10 ^ 7695;` => `input_10 = input_10 ^ 7695`
pi_11: line 1833: `input_11 = input_11 ^ 3143;` => `input_11 = input_11 ^ 3143`
pi_12: line 1839: `input_12 = input_12 ^ 8437;` => `input_12 = input_12 ^ 8437`
pi_13: line 1845: `input_13 = input_13 ^ 7170;` => `input_13 = input_13 ^ 7170`
pi_14: line 1851: `input_14 = input_14 ^ 8432;` => `input_14 = input_14 ^ 8432`
pi_15: line 1857: `input_15 = input_15 ^ 3884;` => `input_15 = input_15 ^ 3884`
pi_16: line 1863: `input_16 = input_16 ^ 1630;` => `input_16 = input_16 ^ 1630`
pi_17: line 1869: `input_17 = input_17 ^ 6205;` => `input_17 = input_17 ^ 6205`
pi_18: line 1875: `input_18 = input_18 ^ 6793;` => `input_18 = input_18 ^ 6793`
pi_19: line 1881: `input_19 = input_19 ^ 6630;` => `input_19 = input_19 ^ 6630`

## 4. UNSAT Check

Query:

```text
input_values AND pi AND safe_postcondition
```

Result: `unsat`

Why suspicious:

The UNSAT-core query was not UNSAT, so the report uses the fallback suspicious CFA edges listed below.

UNSAT core literals:

```text
```

## 5. Suspicious Pi Formulas

## 6. Suspicious CFA Edges


## 7. Reduction Outputs

- `state`: 41 waypoints -> `unsafe3.reduced.witness.state.yml`
- `match`: 41 waypoints -> `unsafe3.reduced.witness.match.yml`
- `all`: 1 waypoints -> `unsafe3.reduced.witness.yml`
