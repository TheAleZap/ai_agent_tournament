# Team 06

## Members

- Alex Garcia
- Alejandro Zapata
- Alesia Dako
- Kohana Rakipi
- Viktoriia Stepanenko
- Laura Somogyi

## Algorithms implemented

| Challenge | Algorithms | Where in the file | Status |
|---|---|---|---|
| Road Trip | UCS, A* (Haversine), conflict repair with A*, hill climbing (2-opt, Or-opt), simulated annealing + restarts, anytime `submit` | `roadtrip_agent.py` §§4–10 | Strong — checks + races documented |
| Chess | Material+positional `evaluate`, minimax, alpha-beta with move ordering, iterative deepening to depth 4 with clock budget | `chess_agent.py` | Partial — required fns look real; README/tests incomplete |
| Battleship | CSP-style `consistent_placements`, Bayes `sonar_posterior`, transition `predict_ship_belief`, multi-rate belief filter, hit targeting, sonar heuristic, placement with spacing | `battleship_agent.py` | Strong code; README/tests missing |
| Catan | Placeholder random `act`; required fns raise `NotImplementedError` | `catan_agent.py` | **Broken / unfinished** |

## Training

Road Trip: no training.  
Chess / Battleship: no offline training.  
Catan: **none yet** — must train Q-values offline (see `docs/students/TRAINING.md`) and embed the table in `catan_agent.py`.

## Tests

**Road Trip** — `check_requirements()`:

```
PASS  Road Trip  Uniform-cost search / Dijkstra     optimal on 8 city pairs, 384 nodes expanded
PASS  Road Trip  A* with a geographic heuristic     optimal on 8 city pairs, 176 nodes expanded
PASS  Road Trip  A* expands no more nodes than UCS  A* 176 vs UCS 384
PASS  Road Trip  Local search / optimization        tour improved from 16810 to 7480
```

| Test | Result |
|---|---|
| 30 races vs `demo` | 30 wins. Mean 12,917 km vs 15,919 km |
| 30 races vs first strategy | 18 wins, 12 draws, 0 losses. Mean 12,918 vs 14,303 km |
| 1,000 random draws | Legal route every time, ≤ 0.05 s |
| Best-route recovery | 79/80 at 5 s; 40/40 at 1.5 s |

**Chess / Battleship / Catan:** no `check_requirements` output or head-to-head numbers in this README yet. A full `check_requirements("Team_06.zip")` will fail until Catan’s four functions exist.

## Dependencies and known limitations

- Road Trip: stdlib only.
- Chess: `chess`.
- Battleship: `numpy`.
- Catan: currently none beyond stdlib; will need learned table embedded in-file.
- Limitations: Catan unplayable as submitted; Chess README empty; Battleship undocumented; team-level presentation PDF not drafted here.

## Use of generative AI

*(To complete before hand-in: name tools used and how, or state none.)*

---

# Submission analysis (current code)

Code reviewed against `assignment_materials/` (Group assignment + Student Handbook), `docs/students/*`, and game READMEs. Class alignment is summarised after [`../class_lessons.md`](../class_lessons.md); the plan below was updated once those lessons were written.

## Overall verdict

Road Trip is submission-ready in spirit (algorithms, comparison, write-up). Battleship is algorithmically advanced but invisible to graders without README/tests. Chess has a working search loop but thin evaluation and no evidence pack. **Catan is a hard blocker**: random play + unimplemented required functions → automatic check failures and a near-certain challenge loss. Grading weight is **60% code/work**, **30% presentation**, **10% tournament** — unfinished Catan and incomplete README hurt the 60% and the presentation story more than a slightly weaker Road Trip route.

## What is good

### Road Trip (`roadtrip_agent.py`) — reference quality for the course

- Explicit PEAS / environment properties / utility-based anytime agent (Sessions 2–3).
- Shared `best_first_search` with Node / expand / reached; goal tested on pop (Session 4).
- UCS + A* with Haversine; admissibility/consistency argued in comments and README (Session 5).
- Local search: 2-opt, Or-opt, double-bridge, SA, restarts; `local_search` for the judge (Session 6).
- Conflict repair of complete-but-illegal tours via A* with blocked cities (Session 10 spirit).
- Optimises **legal** km, not table km; baseline vs improved with numbers; 0.5 s Colab reserve; early valid submit.
- Required checks documented as passing; strong demo and self-play results.

### Battleship (`battleship_agent.py`) — strong hidden-info agent, under-documented

- Required trio implemented: `consistent_placements`, `sonar_posterior` (+ sensor renormalisation), `predict_ship_belief`.
- Playing agent goes far beyond the template: belief grids, shot/sonar Bayes updates, multi-hypothesis rival move rates, occupancy targeting, post-hit line following, spaced placement, defensive moves, time fallback.
- Matches Sessions 8–9 (CSP placements), 17 (beliefs), 23–25 (Bayes), 26 (predict step / filter).

### Chess (`chess_agent.py`) — solid skeleton

- `evaluate`, `minimax`, `alphabeta` present with finite White-centric scores and pruning that should visit fewer nodes.
- Move ordering (MVV-LVA-ish, promotions, checks) + iterative deepening (1…4) + per-move time budget from `time_remaining_s`.
- Uses `python-chess` only (no engine) — allowed.

### Process / packaging

- Correct four filenames under `Team_06/`.
- Road Trip README section already follows the handbook template closely.

## What is bad or incomplete

### Catan (`catan_agent.py`) — critical

- `act` is random.
- `state_features`, `action_value`, `q_update`, `heuristic_policy` all `NotImplementedError` → Catan checks fail; zip-level requirements fail.
- No planning language, no MDP abstraction, no Q-table, no baseline comparison — contradicts Sessions 13 / 18–21 and ASSIGNMENT.md.

### Chess — soft but important gaps

- Evaluation is shallow (material + light positional); no pawn structure / king safety depth / passed pawns.
- `_TT = {}` is unused (transposition tables advertised nowhere and not implemented).
- Depth capped at 4; with 5 s/game and ordering, often fine, but no evidence vs `demo` / self-play.
- Header still says individual author, not Team 06; algorithms table empty; no baseline-vs-improved write-up.

### Battleship — code ahead of story

- No technical explanation, tests, or baseline comparison in README.
- Template team name still in the docstring.
- Model assumptions (independent ships, discrete move rates) are fine if explained as approximations (Session 17: transition model ≠ rival’s true strategy).

### README / hand-in hygiene

- Algorithms table incomplete for 3/4 challenges.
- No full `check_requirements("Team_06.zip")` log.
- Generative-AI section empty.
- Presentation PDF not part of this folder (required separately on Blackboard).

## What must change (priority)

| Priority | Item | Why |
|---|---|---|
| P0 | Implement Catan required functions + non-random `act` | Otherwise 14/14 checks impossible |
| P0 | Offline Q-learning + embed Q-table; `heuristic_policy` baseline; ≥500-game comparison | Handbook + Sessions 20–21 |
| P0 | Fill README for Chess, Battleship, Catan (formulation / algorithms / baseline / time / limits) | 60% grading + presentation |
| P1 | Run and paste full `check_requirements` + Colab match vs `demo_a` | Pre-hand-in checklist |
| P1 | Chess: richer eval or documented depth/time policy; baseline (e.g. material-only depth 1) vs current | ASSIGNMENT “what to explain” |
| P1 | Battleship: document CSP/Bayes/filter; baseline (hunt/target) vs filter; include check output | Same |
| P2 | Clean headers/team names; remove dead `_TT` or implement TT; optional MCTS/particles only if time | Polish |

---

# Plan updated with class lessons

After writing [`../class_lessons.md`](../class_lessons.md), the plan below is what we should actually build — not generic “make agents better”, but **course methods mapped to each file**.

## Guiding rule

Every challenge’s README must name the session ideas (PEAS, UCS/A*, SA, CSP, Bayes, minimax/αβ, planning, MDP, Q-learning) and point to the functions that implement them. Tournament strength is secondary to showing that mapping clearly.

## 1. Catan — build from class, not from random

**Class anchors:** Session 13 (preconditions/effects), 18–19 (MDP / values), 20–21 (Q-learning, ε-greedy, features), logic 11–12 for public deductions.

**Change / why:**

1. **`heuristic_policy`** — priority list: city > settlement > meaningful road > knight/robber > maritime trade > end turn. This is the Session-style baseline and the fallback when Q is cold.
2. **`state_features(observation)`** — small deterministic abstraction, e.g. `(phase, my_vp, opp_visible_vp, resource_bucket, can_city, can_settlement, knight_gap)`. Keeps tabular Q feasible (Session 21: tables need small state).
3. **`q_update`** — exact TD update from Session 20:  
   `q + α * (reward + γ * best_next_q − q)`.
4. **Offline training** (TRAINING.md loop): thousands of games, reward = Δ victory points (+ win bonus); ε-greedy decaying; store `Q = {...}` inside the `.py`.
5. **`action_value` / `act`** — look up Q[features|action_type] (and/or action id scheme you train with); if missing, use heuristic. Never train during the match.
6. **Explain planning:** for the actions you care about, write preconditions/effects (e.g. BUILD_CITY: have cost + own settlement node → −resources, +city, +VP).
7. **Measure:** heuristic vs Q over ≥ 500 held-out seeds; compete with whichever wins; report both.

Without this block, the submission fails the academic core of the Catan column in ASSIGNMENT.md.

## 2. Chess — keep search, deepen the story and the eval

**Class anchors:** Sessions 14–15 (minimax, αβ, evaluation, cutoff); optional 16 (MCTS).

**Change / why:**

1. Keep iterative deepening + αβ + ordering — already correct course shape.
2. Extend `evaluate` with a few **linear features** (Session 15): king safety / pawn advancement already partly there; add doubled/isolated pawns or simple king-zone attacks so the write-up is not “material only”.
3. Document clock policy: budget ≈ min(1.25, max(0.15, 0.12 × remaining)); stop mid-depth; return best completed depth (anytime).
4. Baseline: material-only depth-1 (or greedy capture) vs current agent over ≥ 50 games (colours swapped via seeds).
5. Implement TT properly or delete `_TT` so we do not claim an unused extension.
6. Ensure `minimax`/`alphabeta` values match within tolerance and αβ expands fewer nodes (required checks).

## 3. Battleship — keep filter; write it in course vocabulary

**Class anchors:** Sessions 8–9 (CSP), 17 (belief/observation), 23–25 (Bayes), 26 (predict / optional particles).

**Change / why:**

1. Code is largely fine — **do not rewrite** the filter for its own sake.
2. README must state: variables/domains/constraints for `consistent_placements`; prior/likelihood/posterior for sonar; transition model for `predict_ship_belief` and the in-game predict step; what is deduced with certainty after a hit.
3. Baseline: random/hunt-target without belief update vs current filter; report sink rate / rounds over many seeds.
4. Optionally clarify value of information: sonar after `SONAR_AFTER_MISSES` when occupancy is diffuse (Session decision-theory optional topic).
5. Confirm required checks pass; keep `TIME_RESERVE_S = 0.5`.

## 4. Road Trip — freeze algorithms; only tighten hand-in

**Class anchors:** Sessions 2–6, 10 — already matched.

**Change / why:**

1. Treat as done unless a Colab regression appears.
2. Re-run checks on the final zip so node counts stay in the README.
3. Optional only if spare time: light branch-and-bound on tiny instances for the “limits / future work” paragraph (not required).

## 5. README, checks, presentation (all challenges)

1. Complete algorithms table, Training, Tests (`check_requirements` full dump), Dependencies, Generative AI.
2. One technical block per challenge using the handbook headings.
3. Blackboard: `Team_06.zip` + presentation PDF; 5-minute talk that walks Session → algorithm → result for each game.
4. Pre-hand-in ticks from handbook p.26–27: exact filenames, 14/14, Colab match vs `demo_a`, no forbidden imports, clocks, no debug files, baseline numbers present.

## Suggested work order

```
1. Catan required fns + heuristic_policy + act wired to heuristic
2. Catan offline Q train → embed table → action_value → compare ≥500 games
3. Battleship README + baseline numbers + check_requirements
4. Chess eval polish + baseline numbers + check_requirements
5. Full zip check + Colab demo_a match + finish README AI section
6. Presentation PDF from the four technical blocks
```

## Risk if we ignore class content

- Fancy engineering that does not mention PEAS / admissibility / CSP / Bayes / Q-learning will score poorly on the **60%** even if it wins games.
- Conversely, thin agents that clearly implement and explain the required methods can still score well on work quality.
- Current asymmetry (excellent Road Trip write-up, empty Catan) is the largest grade risk in the repo today.

---

# Technical explanation

### European Road Trip

#### Problem formulation

**Graph.** 105 cities are nodes and 262 two-way roads are edges, weighted by km. We store them as an adjacency dictionary `{city: {neighbour: km}}` (`build_graph`).

**Agent and environment.** Performance is the km of our best legal route submitted before the limit; no legal route means the challenge is lost. The environment is the map, the 25 required cities, the judge and its clock. The actuator is `submit(route)`, and the sensors are the problem dictionary.

The environment is fully observable, deterministic, discrete and known. It is sequential: each leg uses up cities that later legs cannot use. It is semi-dynamic: the map is fixed, but the clock runs. For the route itself it is single-agent, since the rival cannot change our route.

Ours is a utility-based agent. It does not stop at the first legal route; it keeps searching for a shorter one and submits every improvement.

**Formulation, at two levels:**

| | Path between two cities | Order of the required cities |
|---|---|---|
| State | Current city | A complete tour of the 25 required cities, starting at Madrid |
| Actions / neighbours | Drive to a neighbouring city that is not blocked | 2-opt, Or-opt (move 1–3 cities), double-bridge |
| Goal / objective | Reach the target city | Minimise the km of the **legal** route the tour produces |
| Cost | Road km | — |

**Constraint.** No city may appear twice, including cities we only drive through. Joining a tour by shortest paths gives a complete route that may be inconsistent, because two legs can pass through the same city. The agent repairs these conflicts.

#### Algorithms

**UCS and A\*** (sections 4–6). Both run the same `best_first_search` over a `RouteProblem`, with `Node`, `expand` and a `reached` table. The goal is tested when a node is popped from the frontier, not when it is generated.

- UCS orders the frontier by g(n). It is optimal because every road has positive km.
- A* orders the frontier by g(n) + h(n), where h(n) is the straight-line (Haversine) km to the goal.
- **Why straight-line distance is valid.** Every road is at least as long as the straight line between its two ends. By the triangle inequality, any road path from n to the goal is therefore at least h(n), so h never overestimates: it is *admissible*.
- It is also *consistent*: h(n) ≤ c(n, n') + h(n'). So A* returns the same optimal km as UCS while expanding fewer nodes: 176 vs 384 in the checks.

**How the agent uses them.** UCS without a goal, run from each required city, gives a 25 × 25 table of shortest distances and their paths. A* re-plans a leg when it must avoid cities.

**Valid route with no city twice** (section 8, `legal_route`). The route is built one leg at a time. A leg keeps its shortest path unless that path passes through a city already used, or a required city still to come. If it does, A* re-plans the leg with those cities blocked: they are removed from the actions. Both directions of the tour are tried. Every route is checked against the judge's rules (`is_legal`) before it is submitted.

**Optimisation of the visiting order** (sections 7 and 10). There are 24!/2 possible tours, far too many to enumerate, so we use local search.

- **Neighbourhood:** 2-opt (reverse a segment), Or-opt (move a block of 1–3 cities) and double-bridge (a large jump that 2-opt cannot undo).
- **Objective:** the km of the *legal* route, not the km on the distance table.
- **Acceptance rule (simulated annealing):** a better neighbour is always accepted; a worse one with probability e^(−ΔE/T). T starts at 400 and is multiplied by 0.9993 each step.
- **Escaping local optima:** besides annealing, after 1,500 steps without improvement we restart from the best route, run hill climbing on legal km (2-opt and Or-opt) down to a local minimum, and reheat.
- **Polishing:** every new best route has each leg re-planned with A* while avoiding the other legs (`improve_legs`).
- **Fallback:** adapted from the provided template. It inserts cities one by one with breadth-first detours, and guarantees a legal route on every draw.

**Why we chose this.** Local search gives a good route within milliseconds and keeps improving it, which suits a time limit. Optimising the *legal* km mattered most. A tour that is short on the table can become long once its conflicts are repaired: on one draw, a 13,091 km table tour became 13,410 legal km, while a 13,252 km table tour became only 13,275.

#### Baseline against improved version

- **First strategy** (`STRATEGY = "baseline"`): nearest-neighbour tour, hill climbing on table km, then one repair into a legal route.
- **Improved strategy:** the local search above, scored on legal km.

In 30 head-to-head races, the improved strategy won 18 and drew 12, with no losses. Its mean route was 12,918 km against 14,303 km. The draws are maps where the table route is already legal and optimal.

Tuning on 40 draws showed the same lesson. Measured as how often the agent reached the best route we ever found:

| Setting | Best route reached |
|---|---|
| Table hill climbing on 70% of steps | 35 of 40 draws |
| Table hill climbing on 10% of steps | 38 of 40 draws |
| 10%, plus hill climbing on legal km at each restart (final) | 79 of 80 runs |

#### Time and memory

The agent reads `time_limit_s` and stops at min(0.9 × limit, limit − 0.5 s), keeping the half-second reserve recommended for Colab.

A legal route is submitted within 0.05 s, and every improvement is submitted at once. If time runs short, the best route is already with the judge and nothing is lost. Each search step is short, and hill climbing on legal km checks the clock, so the agent never overruns. On every test draw the final route was found within 2 s.

Memory is small: a 25 × 25 table, and a cache of evaluated tours capped at 200,000 entries.

#### Limits

- Local search does not prove that the route is optimal.
- With more time, we would add an exact method (branch and bound) to prove optimality.

### Chess

*(To write after P1 work: PEAS; features in `evaluate`; depth/ID + αβ; baseline numbers; clock policy; limits.)*

### Battleship

*(To write after P1 work: partial observability / belief state; CSP for placements; Bayes for sonar; transition + filter; baseline numbers; time; limits.)*

### Catan

*(To write after P0 work: planning actions; state abstraction; heuristic vs Q; training procedure; baseline ≥500 games; time; limits.)*
