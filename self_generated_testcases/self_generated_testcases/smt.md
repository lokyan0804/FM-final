對，這次我們把它**從 `CFA + witness.yml` 開始**明確寫清楚，並且分成：

1. **共同前處理**
2. **MaxSat 版本：移除哪些 formula 後，安全變成可能**
3. **Unsat / MinUnsat 版本：保留哪些 formula 就足以讓安全不可能**
4. **用 suspicious edges 去 reduce witness.yml**

論文裡的 fault localization 是：給定 feasible counterexample，找一組 CFA edges，它們的 operations 可能對這條 feasible counterexample 負責；之後把這組 edges 映射回 witness 裡要保留的資訊。論文也明確說 product automaton 的 accepting runs 是「witness 描述、program 中存在、且違反 property」的 counterexamples，然後從中選一條當 (cex_W)。([Sosy Lab][1])

---

# 0. Input / Output

Input:

```text
CFA
witness.yml
```

Output:

```text
reduced_witness.yml
```

中間可以另外 dump：

```text
cex_path.json
trace_formula.json
suspicious_edges.json
```

---

# 1. 從 CFA + witness.yml 找一條 feasible error path

你要做的是：

```text
CFA + witness.yml
  -> witness-guided path
  -> feasible error path cex_W
```

在論文裡，這一步是 product automaton。對 YAML prototype，可以簡化成：

```text
根據 witness.yml 的 waypoints，引導 BFS 在 CFA 裡找一條到 error 的 path。
```

具體步驟：

```text
1. 讀 CFA:
   nodes / locations / edges / entry / error

2. 讀 witness.yml:
   extract all waypoints

3. 每個 waypoint 有 location:
   file_name, line, function

4. CFA edge matches waypoint 如果:
   edge.file == waypoint.location.file_name
   edge.line == waypoint.location.line

5. 從 CFA entry 開始：
   按 witness waypoint 順序，
   用 BFS 找到下一個 matching edge。

6. 把中間 BFS path + matching edge 接起來。

7. 最後從 current location BFS 到 error location。

8. 得到:
   cex_W = [e_0, e_1, ..., e_{n-1}, e_error]
```

這條 `cex_W` 應該是一條 **feasible error path**。論文假設 feasible counterexample 的 trace-formula conjunction 是 satisfiable，並且會從這個 feasible trace 的 model 抽出 nondet assignment 作為 precondition (\psi)。([Sosy Lab][1])

---

# 2. 把 error path 轉成 trace formula

對每條 CFA edge (e_i)，產生 SMT formula：

[
TF(cex_W){i} = \phi_i
]

並保存 mapping：

```text
phi_i <-> e_i
```

例如：

```c
x = nondet();
assume(x > 0);
y = x + 1;
assume(y != 1);   // guards reach_error
reach_error();
```

轉成：

```text
phi_0: x0 = nondet0
phi_1: x0 > 0
phi_2: y0 = x0 + 1
phi_3: y0 != 1      // last assume before reach_error
```

論文把 trace formula 記為 (TF(cex))，並假設每個 operation 對應一個 formula。([Sosy Lab][1])

---

# 3. 切成 (\psi, \pi, \varphi)

論文切法是：

[
\psi = \text{precondition}
]

[
\pi = \text{faulty trace}
]

[
\varphi = \text{safe postcondition}
]

具體來說：

## 3.1 (\psi)：precondition

先解：

[
\bigwedge TF(cex_W)
]

因為 `cex_W` 是 feasible error path，所以它應該是 `sat`。

從 model 裡抽出 nondet values。

例如 model 有：

```text
nondet0 = 2
```

則：

[
\psi = (nondet0 = 2)
]

論文定義 (\psi) 就是從 (TF(cex)) 的 model 裡抽出所有 nondet 變數的 satisfying assignment。([Sosy Lab][1])

---

## 3.2 (\pi)：中間 trace formulas

假設最後一個 reach-error guard 是：

[
TF(cex_W){n-1}
]

那：

[
\pi = TF(cex_W){:n-2}
]

也就是排除最後那個 guarding `reach_error()` 的 assume。

論文也是這樣定義：(\pi) 是 prefix，包含 possible program faults，排除最後一個 assume operation。([Sosy Lab][1])

---

## 3.3 (\varphi)：safe postcondition

最後一個 error guard 是：

[
TF(cex_W){n-1}
]

它成立時會 reach error。

所以 safe postcondition 是它的反面：

[
\varphi = \neg TF(cex_W){n-1}
]

例如最後 guard 是：

```c
assume(num != 1);
reach_error();
```

那：

[
TF(cex_W){n-1} = (num \neq 1)
]

[
\varphi = (num = 1)
]

論文也說 (\varphi = \neg TF(cex){n-1})，而 (\neg\varphi) 成立時 reach_error 可達。([Sosy Lab][1])

---

# 4. 現在有兩種 localization 版本

現在我們有：

```text
ψ = 固定這次 counterexample 的 nondet input
π = error guard 之前的中間 operations
φ = safe condition，不進 error
```

原本 error path 是：

[
\psi \land \bigwedge \pi \land \neg\varphi
]

它應該是 `sat`。

而：

[
\psi \land \bigwedge \pi \land \varphi
]

通常是 `unsat`，因為在這次固定 input 下，完整 trace 會 forced 到 error。論文也明確說，在 (\psi) 固定 initial assignments 的前提下，可以假設 (\psi \land \bigwedge\pi \land \varphi) 是 unsat。([Sosy Lab][1])

---

# 5. MaxSat 版本：移除哪些 formula 後，安全變成可能？

MaxSat 找：

[
f \subseteq \pi
]

使得：

[
\psi \land \bigwedge(\pi \setminus f) \land \varphi
]

是 `sat`。

意思是：

> 如果把 (f) 這些中間 operations 拿掉，剩下的 trace 在同一個 precondition (\psi) 下，有可能滿足 safe condition (\varphi)。

所以 (f) 被認為 suspicious。

論文 Algorithm 1 就是檢查所有 (f \subseteq \pi)，找滿足 (\psi \land \bigwedge(\pi \setminus f) \land \varphi) sat 的最小 suspects。([Sosy Lab][1])

---

## MaxSat pseudo-code

```python
def localize_maxsat(psi, pi, safe_phi):
    # pi: list[(formula, edge)]
    suspects = []

    for size in range(1, len(pi) + 1):
        for f in combinations(pi, size):
            remaining = [item for item in pi if item not in f]

            solver = Solver()
            solver.add(psi)
            for formula, edge in remaining:
                solver.add(formula)
            solver.add(safe_phi)

            if solver.check() == sat:
                suspects.append(f)

        if suspects:
            break

    # return one smallest suspect set
    chosen = suspects[0]
    return {edge for formula, edge in chosen}
```

直覺：

```text
完整 π + φ 不可能。
拿掉 f 後，π\f + φ 變可能。
所以 f 是導致不安全的關鍵。
```

---

# 6. Unsat / MinUnsat 版本：哪些 formula 足以讓安全不可能？

Unsat / MinUnsat 找：

[
f \subseteq \pi
]

使得：

[
\psi \land \bigwedge f \land \varphi
]

是 `unsat`。

意思是：

> 光保留 (f) 這些 operations，就已經足以和 safe condition (\varphi) 矛盾。

所以 (f) 是一組足以解釋 error 的 suspicious formulas。

論文中 MinUnsat 找的是所有 minimal (f)，使 (\psi \land \bigwedge f \land \varphi) unsat；Unsat baseline 則是讓 SMT solver 找任意一個這樣的 subset，甚至可能是整個 (\pi)。([Sosy Lab][1])

---

## Unsat-core baseline pseudo-code

這個最容易實作。

```python
def localize_unsat_core(psi, pi, safe_phi):
    # pi: list[(formula, edge)]

    solver = Solver()
    solver.add(psi)
    solver.add(safe_phi)

    lit_to_edge = {}

    for i, (formula, edge) in enumerate(pi):
        lit = Bool(f"a_{i}")
        solver.assert_and_track(formula, lit)
        lit_to_edge[str(lit)] = edge

    result = solver.check()

    if result == unsat:
        core = solver.unsat_core()
        return {
            lit_to_edge[str(lit)]
            for lit in core
            if str(lit) in lit_to_edge
        }

    # fallback: localization failed
    return set()
```

直覺：

```text
ψ + φ 本來也許可以成立。
但加上某些 tracked formulas 後變 unsat。
unsat core 裡的 formula 就是 suspicious。
```

注意：這裡不是檢查 error path 本身是否 unsat。error path 本身是：

[
\psi \land \bigwedge \pi \land \neg\varphi
]

應該是 `sat`。

這裡檢查的是：

[
\psi \land \bigwedge \pi \land \varphi
]

或它的 subset 版本是否 `unsat`。

---

# 7. MinUnsat 版本 pseudo-code

MinUnsat 是比較精確但比較慢的版本。

```python
def localize_minunsat(psi, pi, safe_phi):
    suspects = []

    for size in range(1, len(pi) + 1):
        for f in combinations(pi, size):
            solver = Solver()
            solver.add(psi)
            solver.add(safe_phi)

            for formula, edge in f:
                solver.add(formula)

            if solver.check() == unsat:
                suspects.append(f)

        if suspects:
            break

    chosen = suspects[0]
    return {edge for formula, edge in chosen}
```

這跟 Unsat-core baseline 的差別是：

```text
Unsat:
  solver 給任意 unsat core，可能不是最小。

MinUnsat:
  主動枚舉 subset，找最小 unsat subset。
```

---

# 8. 把 suspicious formulas 映射回 CFA edges

無論 MaxSat 還是 Unsat，最後都會得到：

[
f \subseteq \pi
]

每個 formula 本來都有 mapping：

```text
formula -> CFA edge
```

所以得到：

[
f_G \subseteq G
]

也就是 suspicious CFA edges。

論文也描述：fault localization 回傳 suspects 後，選一個 suspect (f)，再把其中的 trace formulas 映射到對應 CFA edges (f_G)，接著用 (f_G) reduce witness。([Sosy Lab][1])

---

# 9. 用 suspicious CFA edges reduce witness.yml

對 YAML witness 的每個 waypoint：

```text
waypoint.location matches some edge in f_G
```

如果 match，保留。

如果不 match，就是 irrelevant。

三種 reduction：

```text
state:
  irrelevant waypoint 保留 location，刪 constraint

match:
  irrelevant waypoint 刪 location，刪 constraint

all:
  irrelevant waypoint 直接刪掉
  但保留 violation/error waypoint
```

最後輸出：

```text
reduced_witness.yml
```

---

# 10. 全流程總結

```text
Input:
  CFA
  witness.yml

Step 1:
  用 witness waypoints 在 CFA 裡找 witness-guided error path cex_W

Step 2:
  把 cex_W 轉成 trace formulas TF(cex_W)

Step 3:
  check ∧TF(cex_W) is sat
  從 model 抽 nondet assignment，得到 ψ

Step 4:
  π = error guard 前面的 formulas
  φ = 最後 error guard 的 negation，也就是 safe postcondition

Step 5A: MaxSat version
  找最小 f ⊆ π，使得:
    ψ ∧ (π \ f) ∧ φ is sat
  f 是 suspicious formulas

Step 5B: Unsat version
  找 f ⊆ π，使得:
    ψ ∧ f ∧ φ is unsat
  f 是 suspicious formulas

Step 6:
  suspicious formulas -> suspicious CFA edges f_G

Step 7:
  用 f_G reduce witness.yml

Output:
  reduced_witness.yml
```

最短一句話：

```text
先從 CFA + witness.yml 找一條 feasible error trace；
從這條 trace 抽出 ψ、π、φ；
MaxSat 問「拿掉哪些 π 後安全變可能」；
Unsat 問「保留哪些 π 就讓安全不可能」；
最後把這些 formulas 對應的 CFA edges 保留在 witness，其他資訊弱化或刪掉。
```

[1]: https://www.sosy-lab.org/research/pub/2024-SPIN.Fault_Localization_on_Verification_Witnesses.pdf "Fault Localization on Verification Witnesses"
