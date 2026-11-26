# Team 06

## Members

- Alex Garcia
- Alejandro Zapata
- Alesia Dako
- Kohana Rakipi
- Viktoriia Stepanenko
- Laura Somogyi

## What changed in the three agents (this pass)

Earlier pass on Road Trip / Chess / Battleship:

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

## What changed recently

### Chess / Battleship / Road Trip
See earlier notes below the algorithms table history: Chess rewritten; Battleship baseline added; Road Trip re-verified.

### Catan (`catan_agent.py`) — integrated and measured

- Teammate landed a full heuristic + offline Q-table (`Q_TABLE`, 3310 trusted entries) with required `state_features`, `action_value`, `q_update`, `heuristic_policy`.
- We added Team 06 / session header, `STRATEGY` (`baseline` = heuristic only, `improved` = heuristic + Q advantage), and `# BEGIN/END LEARNED TABLE` markers so `catan_train.py` can rewrite the table.
- **500-game comparison** (colours swapped by seed parity): Q-blend **224** vs pure heuristic **276**. Handbook says compete with whichever is better → default `STRATEGY = "baseline"`.
- Full match vs `demo_a` (seed 42): **Team_06 advances 4–0** (all four challenges, 0 incidents).
- `check_requirements("Team_06")`: **14/14 PASS**.

## Algorithms implemented

| Challenge | Algorithms | Where in the file | Status |
|---|---|---|---|
| Road Trip | UCS, A*, conflict repair, SA / hill climbing, anytime `submit` | `roadtrip_agent.py` | Strong |
| Chess | Linear eval, minimax, αβ, ID, TT, quiescence; `STRATEGY` | `chess_agent.py` | Strong |
| Battleship | CSP, Bayes, belief filter; `STRATEGY` | `battleship_agent.py` | Strong |
| Catan | Heuristic planning utilities, MDP abstraction, Q-learning table; `STRATEGY` | `catan_agent.py` | Strong — compete with heuristic |

## Training

Road Trip / Chess / Battleship: no offline training.  
Catan: offline Q-learning via `catan_train.py` (ε from 0.2→0.05, γ=0.97, keep entries with ≥30 visits). Table embedded in `catan_agent.py`. Do not train during a match.

## Tests

**Whole team** — `check_requirements("Team_06")`:

```
PASS  Road Trip     Uniform-cost search / Dijkstra
PASS  Road Trip     A* with a geographic heuristic
PASS  Road Trip     A* expands no more nodes than UCS
PASS  Road Trip     Local search / optimization
PASS  Chess         Heuristic evaluation function
PASS  Chess         Minimax with alpha-beta pruning
PASS  Chess         Depth-limited search
PASS  Battleship    Constraints over hidden ship positions
PASS  Battleship    Bayesian update from noisy sonar
PASS  Battleship    Transition model / belief prediction
PASS  Catan         State abstraction
PASS  Catan         Value estimate for actions
PASS  Catan         Q-learning update
PASS  Catan         Baseline heuristic policy
14/14 requirements pass.
```

**Road Trip**

| Test | Result |
|---|---|
| vs `demo` | 10–0 (re-run); earlier 30–0 |
| improved vs baseline | 10–5–0 on 15 seeds |

**Chess**

| Test | Result |
|---|---|
| vs `demo` | 6–0 |
| improved vs baseline | 10–0 |

**Battleship**

| Test | Result |
|---|---|
| vs `demo` | 12–0 |
| improved vs baseline | 11–1 |

**Catan**

| Test | Result |
|---|---|
| vs `demo` / `demo_b` | 17–3 / 20 (demo); 20–0 / 20 (`demo_b`) |
| Q-blend (`improved`) vs heuristic (`baseline`), 500 games | **224–276** (heuristic better) |
| Full match vs `demo_a`, seed 42 | **4–0**, Team_06 advances, 0 incidents |

## Dependencies and known limitations

- Road Trip: stdlib. Chess: `chess`. Battleship: `numpy`. Catan: stdlib (+ embedded `Q_TABLE`).
- `catan_train.py` is a repo helper for offline training; the Blackboard zip only needs the four agents + this README (judge ignores extra files).
- Limitations: Catan Q-table did not beat the hand heuristic at 500 games (we ship heuristic); Chess has no opening book; Battleship transition model is an estimate; presentation PDF still needed for Blackboard.

## Use of generative AI

*(To complete before hand-in: name tools used and how, or state none.)*

---

# Submission analysis (current code)

## Overall verdict

All four agents pass academic checks (**14/14**). Road Trip, Chess and Battleship have strong play + write-ups. Catan’s heuristic is competitive; the learned Q blend is kept for `action_value` / explanation but is **not** used in `act` by default. Remaining hand-in items: generative-AI line, presentation PDF, zip upload.

## What is good

### Road Trip / Chess / Battleship
Unchanged assessment: course-aligned algorithms, baselines, clocks, documented tests.

### Catan (`catan_agent.py`)
- Explicit heuristic with action preconditions/effects in scoring (build city/settlement/road, trades, knights, …).
- Small MDP abstraction in `state_features`; tabular Q from offline play; `q_update` is the standard TD rule.
- Honest comparison: learning did not beat the heuristic → compete with `STRATEGY="baseline"`.

## What is still open

| Item | Notes |
|---|---|
| Generative-AI acknowledgement | Still empty on purpose for now |
| Presentation PDF | Blackboard, separate file |
| Zip for Blackboard | `Team_06/` with four `.py` + `README.md` |

## Suggested remaining work order

```
1. Fill generative-AI section when ready
2. Export 5-minute presentation PDF
3. Zip Team_06 (four agents + README) and upload
4. Optional: more Catan training / retune BETA if you want Q to win
```

---

# Plan updated with class lessons

Guiding rule unchanged: every challenge names session methods. Road Trip (2–6, 10), Chess (14–15), Battleship (8–9, 17, 23–26), Catan (13, 18–21) are now covered in code + technical explanations below.

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

#### Problem formulation

**PEAS.** Performance: be first to 7 VP (or win adjudication). Environment: 1v1 Catan, dice, robber, no player trading, 5 s clock. Actuator: `{"action": id}`. Sensors: legal actions, `me` / public `opponent`, board, log.

Environment: partially observable (hidden cards), multi-agent, stochastic (dice / steals), sequential, semi-dynamic (clock), discrete, known rules. Agent: utility-based with a learned action-type advantage over a hand heuristic.

| | Abstraction |
|---|---|
| State | `state_features`: (phase, my VP, rival visible VP, affordance bucket, hand-size bucket, round bucket) |
| Actions | Legal action ids; Q keys use action **type** |
| Reward (training) | Δ victory points between decisions + win/loss bonus |
| Policy | Heuristic scores actions; optional Q type-advantage (`STRATEGY="improved"`) |

#### Algorithms

- **Heuristic (`heuristic_policy` / `score_action`)**: one-step utilities for settlement/city/road placement, robber, trades, development cards — encodes rough **preconditions** (can afford / legal list) and **effects** (VP, production, army/road races). Session 13 spirit.
- **`state_features` / `action_value` / `q_update`**: small MDP + Q-learning (Sessions 18–21). `q_update`: `q + α(r + γ max Q' − q)`.
- **Offline training** (`catan_train.py`): many self-play games, ε-greedy over action types, keep entries with ≥30 visits into `Q_TABLE` (3310 entries).
- **`act`**: by default `STRATEGY="baseline"` (heuristic only). `"improved"` adds `BETA *` learned type-advantage.

#### Baseline against improved version

| Test | Result |
|---|---|
| Q-blend vs pure heuristic, **500** games (sides swapped) | Heuristic **276** – Q-blend **224** |
| Decision | **Compete with heuristic** (`STRATEGY="baseline"`) |
| vs `demo_a` in full match | Catan game won 7–5 VP |

Learning is still required academically (`action_value` reads `Q_TABLE`); it just does not win the head-to-head, which we report honestly.

#### Time and memory

Decisions are one heuristic pass (+ tiny Q lookup). No training at import (~1 ms load). `time_remaining_s` is not searched away; work is cheap vs the 5 s clock.

#### Limits

- Q keys only by action **type**, not full action args → coarse.
- Table trained against self-play heuristics, not diverse rivals.
- With more time: richer features, longer training, or SARSA / expectiminimax over dice.

