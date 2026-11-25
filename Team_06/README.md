# Team 06

## Members

- Alex Garcia
- Alejandro Zapata
- Alesia Dako
- Kohana Rakipi
- Viktoriia Stepanenko
- Laura Somogyi

## What changed in the three agents (this pass)

We left Catan to another teammate. Below is what we did on Road Trip, Chess and Battleship after aligning with the handbook and `class_lessons.md`.

### Chess (`chess_agent.py`) — rewritten

- Replaced the thin material+light positional eval with a **linear evaluation** (Session 15): material, piece-square tables, bishop pair, castling rights, doubled/isolated/passed pawns, king pawn shield, mobility.
- Kept required **`evaluate` / `minimax` / `alphabeta`**; αβ uses capture/promotion/check ordering so it visits fewer nodes for the same value.
- Playing agent now uses **iterative deepening** (depth ≤ 6), a real **transposition table**, **quiescence** (captures/promotions), and a clock budget that never spends more than `time_remaining_s` (flag-fall safe).
- Added `STRATEGY = "baseline"|"improved"`: baseline = material-only 1-ply; improved = full search. Measured **10–0** head-to-head and **6–0** vs `demo`.
- Team 06 header + session comments; removed the unused empty TT stub from the old file.

### Battleship (`battleship_agent.py`) — polished + comparable

- Core filter was already strong; we did **not** rewrite the belief math.
- Added Team 06 header mapping Sessions 8–9 / 17 / 23–26.
- Added `STRATEGY = "baseline"|"improved"`: baseline = hunt/target (adjacent to hits, sparse shots, no Bayes/filter/sonar); improved = multi-rate belief filter + CSP targeting + sonar after miss streaks.
- Documented and re-tested: **3/3** checks, **12–0** vs `demo`, **11–1** improved vs baseline.

### Road Trip (`roadtrip_agent.py`) — verified, not redesigned

- Algorithms were already course-correct (UCS, A*, SA/local search, conflict repair, anytime `submit`).
- This pass **re-ran checks and matches** and refreshed the README numbers: **4/4** PASS, **10–0** vs `demo`, **10–5–0** improved vs baseline on 15 seeds.
- No behavioural rewrite; kept as the reference agent.

### Shared packaging

- Root + Team READMEs updated with status, tests, technical explanations for all three.
- Catan left as teammate work (required for full zip 14/14).

## Algorithms implemented

| Challenge | Algorithms | Where in the file | Status |
|---|---|---|---|
| Road Trip | UCS, A* (Haversine), conflict repair with A*, hill climbing (2-opt, Or-opt), simulated annealing + restarts, anytime `submit` | `roadtrip_agent.py` §§4–10 | Strong — checks + races documented |
| Chess | Linear eval (material, PST, pawns, king safety, mobility), minimax, alpha-beta + move ordering, iterative deepening, TT, quiescence; `STRATEGY` baseline vs improved | `chess_agent.py` | Strong — 3/3 checks; beats demo and baseline |
| Battleship | CSP `consistent_placements`, Bayes `sonar_posterior`, `predict_ship_belief`, multi-rate belief filter, hit targeting, sonar VoI heuristic, spaced placement; `STRATEGY` baseline vs improved | `battleship_agent.py` | Strong — 3/3 checks; beats demo and baseline |
| Catan | *(teammate)* | `catan_agent.py` | In progress by another team member |

## Training

Road Trip: no training.  
Chess: no offline training (search + hand-written eval).  
Battleship: no offline training.  
Catan: handled by another teammate (offline Q-learning expected; see `docs/students/TRAINING.md`).

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
| 10 races vs `demo` (re-run) | **10–0**, 0 incidents (e.g. 13,129 vs 16,018 km) |
| 15 races improved vs baseline (`STRATEGY`) | **10 wins, 5 draws, 0 losses** |
| Earlier pack | 30–0 vs demo; 18–12–0 vs first strategy; legal on 1,000 draws; best-route 79/80 at 5 s |

**Chess** — `check_requirements()`:

```
PASS  Chess  Heuristic evaluation function      ranks material correctly from White's point of view
PASS  Chess  Minimax with alpha-beta pruning    same value as minimax with fewer nodes on 4 positions
PASS  Chess  Depth-limited search               depth 1 visits 32 nodes, depth 2 visits 128
```

| Test | Result |
|---|---|
| 6 matches vs `demo` (real 5 s clocks) | 6–0. No incidents. Typical scores 2–0 or 1.5–0.5 |
| 10 matches improved vs baseline (`STRATEGY`) | 10–0 (20–0 on game points). No incidents |

**Battleship** — `check_requirements()`:

```
PASS  Battleship  Constraints over hidden ship positions  all placements found on 4 constraint sets
PASS  Battleship  Bayesian update from noisy sonar        Bayes update exact on 3 cases
PASS  Battleship  Transition model / belief prediction    belief correctly propagated through the transition model
```

| Test | Result |
|---|---|
| 12 matches vs `demo` | **12–0**, all by `fleet_destroyed`, 0 incidents |
| 12 matches improved vs baseline (`STRATEGY`) | **11–1**, 0 incidents |

**Catan:** teammate ownership. Zip-level 14/14 waits on their required functions.

## Dependencies and known limitations

- Road Trip: stdlib only.
- Chess: `chess` (board + move gen only; no engine).
- Battleship: `numpy`.
- Catan: teammate (likely embedded Q-table + stdlib / allowed libs).
- Limitations: Battleship transition model is an estimate of rival motion; Chess has no opening book; Catan not finished here; presentation PDF still needed for Blackboard.

## Use of generative AI

*(To complete before hand-in: name tools used and how, or state none.)*

---

# Submission analysis (current code)

Code reviewed against `assignment_materials/` (Group assignment + Student Handbook), `docs/students/*`, and game READMEs. Class alignment is summarised after [`../class_lessons.md`](../class_lessons.md); the plan below was updated once those lessons were written.

## Overall verdict

Road Trip, Chess and Battleship are submission-ready on our side (algorithms, checks, baseline comparisons, write-ups). **Catan is owned by another teammate** and is the remaining zip-level dependency for 14/14 `check_requirements`. Grading weight is **60% code/work**, **30% presentation**, **10% tournament**.

## What is good

### Road Trip (`roadtrip_agent.py`) — reference quality for the course

- Explicit PEAS / environment properties / utility-based anytime agent (Sessions 2–3).
- Shared `best_first_search` with Node / expand / reached; goal tested on pop (Session 4).
- UCS + A* with Haversine; admissibility/consistency argued in comments and README (Session 5).
- Local search: 2-opt, Or-opt, double-bridge, SA, restarts; `local_search` for the judge (Session 6).
- Conflict repair of complete-but-illegal tours via A* with blocked cities (Session 10 spirit).
- Optimises **legal** km, not table km; baseline vs improved with numbers; 0.5 s Colab reserve; early valid submit.
- Required checks documented as passing; strong demo and self-play results.

### Battleship (`battleship_agent.py`) — done for course purposes

- Required trio: `consistent_placements`, `sonar_posterior`, `predict_ship_belief` (3/3 PASS).
- Belief filter over multiple rival-move-rate hypotheses; CSP targeting after hits; sonar after miss streaks; spaced placement; defensive ship moves.
- `STRATEGY` baseline (hunt/target) vs improved filter: **11–1** on 12 seeds; **12–0** vs `demo`.

### Chess (`chess_agent.py`) — done for course purposes

- Rich linear `evaluate` (material, PST, bishop pair, castling, doubled/isolated/passed pawns, king pawn shield, mobility).
- Required `minimax` / `alphabeta` pass with fewer nodes under pruning.
- Playing agent: iterative deepening to depth 6, move ordering, transposition table, quiescence, clock budget that never exceeds `time_remaining_s`.
- `STRATEGY = "baseline"|"improved"` with measured 10–0 head-to-head.

### Process / packaging

- Correct four filenames under `Team_06/`.
- Road Trip README section already follows the handbook template closely.

## What is bad or incomplete

### Catan (`catan_agent.py`) — teammate

- Still a template here until their branch lands. Zip-level 14/14 and the Catan technical block depend on them (Sessions 13 / 18–21).

### Hand-in hygiene left

- Full `check_requirements("Team_06.zip")` after Catan merge.
- Generative-AI acknowledgement.
- Presentation PDF for Blackboard.
- Colab match vs `demo_a` with the final zip.

## What must change (priority)

| Priority | Item | Owner |
|---|---|---|
| P0 | Finish Catan required fns, Q-table, heuristic, README block, ≥500-game comparison | Teammate |
| P1 | Merge Catan → full zip checks + Colab vs `demo_a` | Whole team |
| P1 | Generative-AI section + presentation PDF | Whole team |
| P2 | Optional polish (Chess openings, Battleship particles) | Optional |

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

## 2. Chess — completed

Implemented and measured (see technical explanation below). Next optional only: opening variety to avoid some threefold draws.

## 3. Battleship — completed

Filter kept; baseline hunt/target added; checks + matches documented (see technical explanation).

## 4. Road Trip — completed

Re-checked; still beats demo and baseline. No algorithm change needed.

## 5. Remaining hand-in (team)

1. Land Catan from teammate → 14/14 checks.
2. Colab match vs `demo_a` with final zip.
3. Generative-AI line + presentation PDF.

## Suggested work order

```
1. Teammate finishes Catan (required fns + Q + README block)
2. Merge → check_requirements on Team_06.zip → Colab vs demo_a
3. Presentation PDF from the four technical blocks
```

## Risk if we ignore class content

- Fancy engineering that does not mention PEAS / admissibility / CSP / Bayes / Q-learning will score poorly on the **60%** even if it wins games.
- Conversely, thin agents that clearly implement and explain the required methods can still score well on work quality.
- On our side Road Trip / Chess / Battleship now carry that mapping; **Catan is the remaining academic gap**.

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

#### Problem formulation

**PEAS.** Performance: game points over two colours (win 1, draw 0.5). Environment: standard chess, rival agent, 5 s decision clock per game. Actuator: `{"move": uci}`. Sensors: FEN, legal moves, clocks, history.

The environment is fully observable, deterministic, discrete, sequential, multi-agent and adversarial, semi-dynamic (clock), known rules. Agent type: utility-based game-playing agent (Session 14–15).

| | Formal game |
|---|---|
| State | Position (FEN / `chess.Board`) |
| Actions | Legal moves |
| Transition | Standard chess rules |
| Terminal utility | Mate / draw → ±MATE or 0 |
| Heuristic | Linear evaluation from White’s point of view |

#### Algorithms

- **`evaluate`**: material + piece-square tables + bishop pair + castling rights + doubled/isolated/passed pawns + king pawn shield + small mobility term (Session 15 linear evaluation).
- **`minimax` / `alphabeta`**: depth-limited search; αβ with capture/promotion/check ordering visits fewer nodes for the same value (Sessions 14–15).
- **Playing agent (`STRATEGY="improved"`)**: iterative deepening (depth 1…6), αβ, transposition table, quiescence (captures/promotions to depth 4), deadline from `time_remaining_s`.
- **Baseline (`STRATEGY="baseline"`)**: material-only one-ply lookahead.

#### Baseline against improved version

| Test | Result |
|---|---|
| Improved vs baseline, 10 seeds, real clocks | **10–0** challenge wins (20–0 game points), 0 incidents |
| Improved vs `demo`, 6 seeds | **6–0**, 0 incidents |

#### Time and memory

Budget = min(0.85 s, 16% of usable clock) after a Colab-style reserve, and never more than the remaining clock minus ~30 ms overhead. If almost no time is left, return the best ordered legal move with no search. Incomplete depths are discarded; the last finished depth stands. TT capped at 200k entries.

#### Limits

- No opening book → occasional threefold draws against weak opponents.
- Evaluation is hand-tuned, not learned.
- With more time: better endgame knowledge, null-move pruning, or MCTS (Session 16).

### Battleship

#### Problem formulation

**PEAS.** Performance: sink the enemy fleet (17 segments) before they sink ours / before adjudication. Environment: 10×10 board, moving ships until first hit, noisy sonar (2 uses), rival agent, 5 s clock. Actuators: placements, optional ship move, shot or sonar. Sensors: own fleet, shot/sonar history, legal moves, clocks — **not** the enemy’s current positions.

Environment: partially observable, multi-agent, stochastic (rival motion + sonar noise), sequential, semi-dynamic (clock), discrete, known rules. Agent type: belief-state / utility-based (Session 17).

| | CSP view (one ship) | Filter view |
|---|---|---|
| Variables | Top-left cell + orientation | Belief mass over placements |
| Domains | Cells where the ship fits | Soft probabilities |
| Constraints | Cover `required`, avoid `blocked` | Likelihood of shots/sonar |
| Dynamics | — | Transition: may move one cell |

**Certain deductions.** A HIT freezes that ship. Misses fired *after* that hit permanently block placements covering those cells for that ship. A past miss before any hit is **not** permanent emptiness (ships move).

#### Algorithms

- **`consistent_placements`** (Sessions 8–9): enumerate every (row, col, H/V) consistent with blocked/required cells.
- **`sonar_posterior`** (Sessions 23–25): Bayes update with the published ±1 sensor model and renormalisation at bounds.
- **`predict_ship_belief`** (Session 26 prediction step): with probability `p` move one legal cardinal step, else stay.
- **Playing filter (`STRATEGY="improved"`)**: per remaining ship length, maintain H/V belief grids under three rival move-rate hypotheses (0, 0.25, 1); update on shots/sonar; predict between our turns; shoot max occupancy, or follow open hits via CSP scoring; sonar after `SONAR_AFTER_MISSES` consecutive misses; spaced non-touching placement; move ships away from damage when hit.
- **Baseline (`STRATEGY="baseline"`)**: same placement/moves, but hunt adjacent to hits / sparse random shots — no filter, no sonar.

#### Baseline against improved version

| Test | Result |
|---|---|
| Improved vs baseline, 12 seeds | **11–1**, 0 incidents |
| Improved vs `demo`, 12 seeds | **12–0**, all `fleet_destroyed`, 0 incidents |

#### Time and memory

If `time_remaining_s < 0.5`, fall back to a cheap adjacent/random shot. Belief updates are numpy vectorised; no heavy work at import.

#### Limits

- Ships treated as independent in the occupancy sum; rival strategy ≠ our transition rates (we only *estimate*).
- Optional extension not used: particle filtering / full HMM over the joint fleet.
- With more time: learn rival move rate online more tightly, or value-of-information for sonar vs shot every turn.

### Catan

*(Owned by another teammate — planning / MDP abstraction / Q-learning / heuristic comparison to be filled when their agent lands.)*
