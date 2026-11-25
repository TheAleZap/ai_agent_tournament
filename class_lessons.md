# Class lessons for the AI Agent Tournament

Notes distilled from Sessions 01–21 and 23–26 (slides) and the Session 03–05 / 08–09 notebooks.  
Purpose: keep every agent decision tied to methods actually taught in class.  
Source slides/notebooks stay outside this repo; this file is the working checklist.

---

## How grading pushes us (from the group-assignment brief)

- **10%** tournament position, **30%** 5-minute presentation, **60%** code + work quality.
- Winning alone is not enough: required functions must pass `check_requirements`, and the README must show we applied **course methods**.
- Methods named on the brief: UCS / A* / local search (Road Trip); minimax / alpha-beta / evaluation (Chess); constraints / Bayes / belief filtering (Battleship); heuristics / planning / MDPs / Q-learning (Catan).

---

## Cross-cutting agent ideas (Sessions 1–3)

### Agents and PEAS (Session 2)

- An agent is judged by a **performance measure** in a specified **task environment**, not “intelligence in the abstract”.
- Always write **PEAS**: Performance, Environment, Actuators, Sensors.
- Environment axes we must name for each challenge:
  - fully / partially observable
  - single / multi-agent
  - deterministic / stochastic
  - episodic / sequential
  - static / dynamic / semi-dynamic
  - discrete / continuous
  - known / unknown
- Agent types: simple reflex → model-based → goal-based → **utility-based**. Tournament agents should usually be utility-based (or learned policies that approximate that).
- Rational ≠ omniscient: choose the action that maximises expected performance given what we know and the time left.

### Problem formulation (Session 3)

Before coding search, lock:

1. **Goal formulation** — what counts as success.
2. **Problem formulation** — states, initial state, actions, transition model, goal test, path cost.
3. **Search** — explore the state space.
4. **Execution** — apply the plan (or keep re-planning under a clock).

Abstraction matters: leave out detail that does not change the optimal decision.

---

## Road Trip map: search + local search (Sessions 3–6, 10)

### Uninformed search (Session 4)

- Distinguish **state-space graph** vs **search tree**.
- Node fields: state, parent, action, path-cost, depth.
- **Frontier** = generated, not yet expanded. **Reached** = best node found for a state.
- Expand = pop from frontier and generate children.
- **UCS / Dijkstra**: priority = `g(n)`. Optimal when step costs are positive. Goal test when a node is **popped**, not when generated.
- Completeness / optimality / complexity trade-offs among BFS, DFS, UCS.

### Informed search (Session 5)

- Heuristic `h(n)` estimates remaining cost to goal.
- Greedy best-first: expand min `h(n)` — can be suboptimal.
- **A\***: expand min `f(n) = g(n) + h(n)`.
- **Admissible**: never overestimates → A\* optimal (tree / graph search under the usual conditions).
- **Consistent** (monotone): `h(n) ≤ c(n,a,n') + h(n')` → with a reached table, A\* is optimally efficient among that class.
- For roads: **straight-line distance** is admissible and consistent if edge costs are real road km (≥ great-circle).

### Local search (Session 6)

Use when we care about the **quality of a complete configuration**, not the path that built it.

- Neighbourhood + objective function.
- **Hill climbing**: move to a better neighbour until stuck (local optimum / plateau / ridge).
- Escapes: random restarts, sideways moves, **simulated annealing** (`P(accept worse) = e^(−ΔE/T)`, cool T), evolutionary / genetic ideas.
- Road Trip visiting order is a classic local-search / TSP-style landscape; 2-opt / Or-opt / double-bridge are valid neighbourhoods.

### CSP repair mindset (Session 10) — also useful for routes

- Backtracking builds a **partial** assignment; local search can start from a **complete but inconsistent** assignment and **repair conflicts** (min-conflicts).
- Road Trip: joining shortest legs can give a complete tour that violates “no city twice”; repair by re-planning blocked legs (A\* with blocked cities), same spirit as conflict repair.

### Notebook practice (Sessions 3–5)

- Implement expand / frontier / reached carefully.
- Count expansions the same way the judge does (goal popped ≠ expanded in their definition for required checks).
- Compare UCS vs A\* node counts on the same map.

**Apply to Road Trip:** UCS for all-pairs among required cities; A\* for conflict re-planning; SA + hill climbing on the legal-route objective; submit early and keep improving (anytime).

---

## Battleship map: CSPs + logic + belief (Sessions 8–12, 17, 23–26)

### CSPs (Sessions 8–9 + code notebooks)

- Factored state: **Variables, Domains, Constraints**.
- Partial / complete / consistent assignments.
- Backtracking + ordering: **MRV**, degree heuristic, **LCV**.
- Inference: forward checking, **arc consistency / AC-3**, MAC.
- Ship placement given hits/misses is a CSP: variables = ship positions/orientations; domains = legal top-lefts; constraints = cover required cells, avoid blocked cells, non-overlap (when modelling the whole fleet).

### Logic (Sessions 11–12)

- Knowledge base + entailment: what **must** be true given evidence.
- Propositional vs first-order: objects and relations (cells, ships, hits).
- For Battleship / Catan: separate **certain deductions** (a hit freezes that ship; a post-hit miss permanently blocks placements covering that miss for that ship) from probabilistic guesses.

### Hidden information (Session 17)

- Actual state vs observation vs **belief state**.
- Observation model `O`: what an action reveals.
- Moving ships: a past miss is **not** a permanent empty cell → belief must be updated over time.

### Probability and Bayes (Sessions 23–25)

- Prior → likelihood → **posterior** (Bayes’ rule).
- Sensor model for sonar: reading equals truth with probability `p`, else ±1 with renormalisation at bounds — exactly what `sonar_posterior` encodes.
- Exact inference by enumeration / variable elimination when the model is small.

### Approximate inference (Session 26)

- Sampling: prior, rejection, likelihood weighting, Gibbs.
- Optional extension for moving ships: **particle filtering** / HMM-style predict–update (assignment lists HMM + particles as optional; required check covers the **prediction step** via `predict_ship_belief`).

**Apply to Battleship:** `consistent_placements` = CSP enumeration; belief grids + Bayes updates on shots/sonar; transition model for mobile ships; decide shot vs sonar with value-of-information intuition; keep a time reserve.

---

## Chess map: games + evaluation (Sessions 14–16)

### Adversarial search (Session 14)

- Zero-sum, perfect information, deterministic → **game tree**.
- **Minimax**: MAX maxes, MIN mins; optimal against a rational opponent.
- Formalise: players, actions, terminal test, utility.

### Evaluation and pruning (Session 15)

- Cannot search to leaves with 5 s/game → **depth-limited** search + **heuristic evaluation**.
- Evaluation features (material, mobility, king safety, pawn structure, …) usually combined **linearly**.
- **Alpha-beta** pruning preserves the minimax value; move ordering (captures, checks, promotions) makes pruning effective.
- Iterative deepening + clock awareness; optional quiescence / expectiminimax (expectiminimax is more Catan/dice than chess).

### MCTS (Session 16) — optional

- Selection (UCB), expansion, simulation/rollout, backpropagation.
- Useful when branching is huge or evaluation is weak; optional for Chess/Catan.

**Apply to Chess:** real `evaluate` / `minimax` / `alphabeta` for checks; playing agent uses iterative deepening + alpha-beta + move ordering + hard deadline from `time_remaining_s`.

---

## Catan map: planning + MDPs + RL (Sessions 13, 15, 18–21)

### Classical planning (Session 13)

- States as sets of fluents / predicates.
- Actions with **preconditions** and **effects** (STRIPS-style).
- Plan = sequence transforming initial state toward a goal (e.g. 7 VP).
- Even a simplified action model (build city if resources + spot; play knight if…) satisfies the assignment’s “explicit planning” explanation.

### Stochastic games (Session 15)

- Dice and hidden cards → chance nodes; optional **expectiminimax**.
- Still need a heuristic when depth is shallow.

### MDPs (Sessions 18–19)

- States, actions, transition `P(s'|s,a)`, reward `R`, discount `γ`.
- **Policy** π(s) → a; value functions V(s), action values Q(s,a).
- Bellman optimality; value iteration / policy iteration.
- Catan full game is huge → **abstraction**: few features as the state (`state_features`), small action types, learn Q offline.

### Reinforcement learning (Sessions 20–21)

- Model-free **Q-learning**:  
  `Q(s,a) ← Q(s,a) + α [ r + γ max_{a'} Q(s',a') − Q(s,a) ]`  
  (exactly what `q_update` must implement).
- Exploration vs exploitation: **ε-greedy**; decay ε over training.
- Tabular Q needs a small discrete state; if too big, linear / feature approximation (Session 21).
- Train offline for thousands of games (handbook / TRAINING.md); store the table inside `catan_agent.py`; do **not** train at import or during the match.
- Compare learned policy vs **heuristic_policy** baseline (≥ 500 games for Catan).

### Logic / deduction in Catan

- From the public log, deduce what is certain about the opponent’s resources when possible (Session 11–12 spirit): e.g. they built a city ⇒ they had the cost at that moment.

**Apply to Catan:** hand-written heuristic baseline; feature abstraction; offline Q-learning; `action_value` reads the stored table; `act` uses Q when confident else heuristic; explain planning + MDP abstraction in the README.

---

## Session → challenge cheat sheet

| Session | Core idea | Primary challenge |
|---|---|---|
| 2 | PEAS, environment properties | All |
| 3 | Problem formulation | All (esp. Road Trip) |
| 4 | UCS, frontier/reached | Road Trip |
| 5 | A*, admissible/consistent h | Road Trip |
| 6 | Hill climbing, SA, restarts | Road Trip |
| 8–9 | CSP, backtracking, AC-3 | Battleship |
| 10 | Min-conflicts / repair | Road Trip, Battleship |
| 11–12 | Logic, entailment | Battleship, Catan |
| 13 | Planning, precond/effects | Catan |
| 14 | Minimax | Chess |
| 15 | Eval fn, alpha-beta, cutoff | Chess (Catan optional) |
| 16 | MCTS | Chess/Catan optional |
| 17 | Belief states, hidden info | Battleship |
| 18–19 | MDP, Bellman, values | Catan |
| 20–21 | Q-learning, ε-greedy, features | Catan |
| 23–25 | Bayes, exact inference | Battleship |
| 26 | Sampling / particles | Battleship optional |

---

## Non-negotiables for submission (handbook + brief)

1. Four agent files + README; exact names; one file per agent (helpers + Q-table inside).
2. All **14** `check_requirements` checks pass.
3. Full Colab match vs `demo_a` with real clocks, **no incidents**.
4. Baseline vs improved comparison with numbers in the README (Catan: ≥ 500 games).
5. Watch `time_remaining_s` / `time_limit_s`; keep ~0.5 s Colab reserve.
6. No forbidden imports; no training during the match; acknowledge generative AI.
7. Technical explanation ≈ one page per challenge (formulation, algorithms, baseline comparison, time/memory, limits).
8. Presentations 3 Dec; zip deadline Thu 26 Nov 2026 23:59; final exam 10 Dec.
