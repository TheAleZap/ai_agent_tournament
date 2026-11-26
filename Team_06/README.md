# Team 06

## Members

- Alex Garcia
- Alejandro Zapata
- Alesia Dako
- Kohana Rakipi
- Viktoriia Stepanenko
- Laura Somogyi

## This submission

This folder is our tournament submission. It contains four agents and this README:

```
Team_06/
  roadtrip_agent.py
  chess_agent.py
  battleship_agent.py
  catan_agent.py
  README.md
```

Each challenge follows methods from the course. We compare a baseline strategy with the strategy we compete with, and we report the results below.

## How to run

The agents are meant to be run with the course judge, **`Tournament.ipynb`**, together with the provided `ai_agent_tournament` package (as distributed for the assignment).

1. Open `Tournament.ipynb` in Google Colab (or locally with Python 3.10+ and `pip install -r requirements.txt`).
2. Upload or place this `Team_06` folder (or `Team_06.zip`) where the notebook can see it.
3. Point the judge at our team, for example:

```python
TEAM_A = "Team_06.zip"   # or the Team_06 folder / path
TEAM_B = "demo_a"        # or another team

check_requirements("Team_06")           # expected: 14/14 PASS
run_match(team_a=TEAM_A, team_b=TEAM_B, seed=42)
```

Single-challenge practice uses the same notebook helpers, for example `run_game("chess", "Team_06/chess_agent.py", opponent="demo")`. Clocks and rules are those of the handbook; our agents read `time_limit_s` / `time_remaining_s` from the judge.

## Algorithms implemented

| Challenge | Strategy we compete with | Algorithms | File |
|---|---|---|---|
| Road Trip | Simulated annealing on legal km, with UCS/A* and conflict repair | UCS, A* (Haversine), 2-opt / Or-opt / SA, anytime `submit` | `roadtrip_agent.py` |
| Chess | Iterative-deepening alpha-beta with a linear evaluation | `evaluate`, minimax, alpha-beta, move ordering, TT, quiescence | `chess_agent.py` |
| Battleship | Belief filter + CSP targeting after hits | `consistent_placements`, `sonar_posterior`, `predict_ship_belief`, Bayes updates | `battleship_agent.py` |
| Catan | Hand heuristic (planning-style action scores) | `state_features`, `action_value`, `q_update`, `heuristic_policy`; Q-table kept for learning | `catan_agent.py` |

## Training

Road Trip, Chess and Battleship have no offline training.  
Catan was trained offline with Q-learning (ε from 0.2 to 0.05, γ = 0.97; entries kept after ≥ 30 visits). The learned table (`Q_TABLE`, 3310 entries) is embedded in `catan_agent.py`. We do not train during a match.

## Tests

`check_requirements` on this folder: **14/14 PASS**.

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
```

| Challenge | Comparison / practice | Result |
|---|---|---|
| Road Trip | Competing strategy vs baseline (15 seeds) | 10 wins, 5 draws, 0 losses |
| Road Trip | vs `demo` | 10–0 (also 30–0 in a larger pack) |
| Chess | Competing strategy vs material 1-ply baseline (10 seeds) | 10–0 (20–0 game points) |
| Chess | vs `demo` | 6–0 |
| Battleship | Belief filter vs hunt/target baseline (12 seeds) | 11–1 |
| Battleship | vs `demo` | 12–0 |
| Catan | Heuristic vs Q-blend (500 games, sides swapped) | Heuristic 276 – Q-blend 224 → we compete with the heuristic |
| Catan | vs `demo` / `demo_b` | 17–3 / 20; 20–0 / 20 |
| Full match | vs `demo_a`, seed 42 | **4–0**, 0 incidents |
| Full match | vs `demo_b`, seeds 7 and 99 | **4–0**, 0 incidents |

## Dependencies and limitations

- Road Trip: Python standard library. Chess: `chess`. Battleship: `numpy`. Catan: standard library and the embedded `Q_TABLE`.
- Local search on Road Trip does not prove optimality. Chess has no opening book. The Battleship transition model estimates rival motion; it need not match their true policy. Catan’s Q-table did not beat the heuristic at 500 games, so the competing policy is the heuristic while `action_value` still exposes the learned values.

## Use of generative AI

We acknowledge the use of generative AI (Claude) to improve the quality and clarity of our code and documentation. The choice of algorithms, problem formulations, baselines, and overall design for each challenge are our own and follow what was taught in class. We limited AI use mainly to translating ideas and pseudocode into working Python, refactoring, debugging, and polishing explanations.

## Course methods used

| Course topic | Challenge |
|---|---|
| PEAS and problem formulation | All four |
| UCS, A*, admissible heuristics | Road Trip |
| Local search / simulated annealing | Road Trip |
| CSPs | Battleship |
| Logic / certain deductions | Battleship, Catan |
| Classical planning (preconditions / effects) | Catan |
| Minimax, alpha-beta, evaluation functions | Chess |
| Hidden information and belief states | Battleship |
| MDPs and value functions | Catan |
| Q-learning | Catan |
| Bayes’ rule and sensor models | Battleship |
| Belief prediction step | Battleship |

Optional topics we did not rely on for the competing agents: MCTS; full expectiminimax over Catan dice; particle filtering over the whole Battleship fleet (we use a grid filter with the required prediction step).

---

# Technical explanation

## European Road Trip

### Problem formulation

**Graph.** 105 cities are nodes and 262 two-way roads are edges, weighted by km, stored as `{city: {neighbour: km}}` (`build_graph`).

**PEAS.** Performance: kilometres of our best legal route before the time limit (no legal route loses). Environment: the map, the 25 required cities, the judge and its clock. Actuator: `submit(route)`. Sensors: the problem dictionary.

The environment is fully observable, deterministic, discrete and known; sequential (each leg consumes cities); semi-dynamic because of the clock; single-agent for constructing our own route. We use a utility-based anytime agent: we submit an early legal route and keep improving it.

| | Path between two cities | Order of the required cities |
|---|---|---|
| State | Current city | Tour of the 25 required cities (Madrid first) |
| Actions | Drive to an unblocked neighbour | 2-opt, Or-opt (1–3 cities), double-bridge |
| Goal / objective | Reach the target | Minimise km of the **legal** repaired route |
| Cost | Road km | — |

No city may appear twice, including transit cities. Joining shortest legs can create conflicts; we repair them.

### Algorithms

**UCS and A\*** share `best_first_search` with `Node`, `expand` and a `reached` table. The goal is tested when a node is **popped**, not when generated.

- UCS orders by g(n); optimal with positive road costs.
- A* orders by g(n) + h(n) with Haversine straight-line km. The heuristic is *admissible* (roads are at least as long as the great-circle) and *consistent*. Checks: A* 176 expansions vs UCS 384, same optimal distances.

UCS from every required city builds a 25 × 25 distance/path table. When a leg conflicts with used or still-to-visit cities, A* re-plans with those cities blocked (`legal_route`).

**Local search** on the visiting order (far too many tours to enumerate):

- Neighbourhood: 2-opt, Or-opt, double-bridge.
- Objective: legal repaired km (not table km alone).
- Simulated annealing: accept improvements always; worse moves with e^(−ΔE/T); cool with α = 0.9993; restart and reheat after long plateaus; polish legs with A*.

We compete with this improved strategy (`STRATEGY = "improved"`). The baseline is nearest-neighbour + hill climbing on table km with a single repair.

### Baseline against improved version

| Test | Result |
|---|---|
| Improved vs baseline (15 seeds) | 10 wins, 5 draws, 0 losses |
| Larger pack vs first strategy | 18 wins, 12 draws, 0 losses; mean 12,918 km vs 14,303 km |
| vs `demo` | 10–0 (and 30–0 in an earlier pack) |

### Time and memory

We stop by min(0.9 × `time_limit_s`, limit − 0.5 s). A legal route is submitted within about 0.05 s; every improvement is submitted immediately. Memory is a 25 × 25 table plus a tour cache capped at 200,000 entries.

### Limits

Local search does not prove optimality. With more time we would add branch-and-bound on small instances.

---

## Chess

### Problem formulation

**PEAS.** Performance: points over two games with colours swapped. Environment: standard chess, rival, 5 s clock per game. Actuator: `{"move": uci}`. Sensors: FEN, legal moves, clocks, history.

Fully observable, deterministic, discrete, sequential, multi-agent adversarial, semi-dynamic (clock), known rules. Utility-based game-playing agent.

| | Formal game |
|---|---|
| State | Position (`chess.Board` / FEN) |
| Actions | Legal moves |
| Terminal utility | Mate / draw → ±MATE or 0 |
| Heuristic | Linear evaluation from White’s point of view |

### Algorithms

- **`evaluate`**: material, piece-square tables, bishop pair, castling rights, doubled/isolated/passed pawns, king pawn shield, mobility (linear evaluation as in class).
- **`minimax` / `alphabeta`**: depth-limited search. Alpha-beta preserves the minimax value: a cut happens only when a branch cannot change the forced decision (`α ≥ β`). Move ordering (captures, promotions, checks) only makes cuts earlier.
- **Competing agent**: iterative deepening (depth ≤ 6), alpha-beta, transposition table, quiescence on captures/promotions, clock budget from `time_remaining_s`. If the chosen move would claim threefold while we stand better, we pick another legal move.
- **Baseline**: material-only one-ply lookahead.

### Baseline against improved version

| Test | Result |
|---|---|
| Improved vs baseline, 10 seeds | 10–0 (20–0 game points), 0 incidents |
| vs `demo`, 6 seeds | 6–0, 0 incidents |

### Time and memory

Budget ≈ min(0.85 s, 16% of usable clock) after a reserve, never more than remaining time minus a small overhead. Incomplete depths are discarded; the last finished depth stands. TT capped at 200,000 entries.

### Limits

No opening book; repetition handling is greedy. With more time: richer endgames, null-move pruning, or MCTS.

---

## Battleship

### Problem formulation

**PEAS.** Performance: destroy the enemy fleet (or win on adjudication). Environment: 10×10 board, ships that move until first hit, noisy sonar (2 uses), 5 s clock. Actuators: placement, optional move, shot or sonar. Sensors: own fleet and histories — not current enemy positions.

Partially observable, multi-agent, stochastic, sequential, semi-dynamic, discrete. Belief-state / utility-based agent.

| | CSP (one ship) | Filter |
|---|---|---|
| Variables | Top-left + orientation | Belief over placements |
| Domains | Legal cells | Soft probabilities |
| Constraints | Cover `required`, avoid `blocked` | Shot / sonar likelihoods |

**Certain deductions.** A hit freezes that ship. Misses after a hit permanently block placements for that ship. A sunk length resolves hit cells. A miss before any hit is not permanent emptiness (ships move).

### Algorithms

- **`consistent_placements`**: every (row, col, H/V) consistent with blocked/required cells (CSP enumeration).
- **`sonar_posterior`**: Bayes update with the published ±1 sensor model and bound renormalisation.
- **`predict_ship_belief`**: with probability p move one legal step, else stay.
- **Competing agent**: belief grids under rival move-rate hypotheses (0, 0.25, 1); update on evidence; predict between turns; shoot max occupancy or follow open hits via CSP scoring; sonar after a streak of misses; spaced placement; defensive moves when damaged.
- **Baseline**: hunt next to hits / sparse random shots, no filter or sonar.

### Baseline against improved version

| Test | Result |
|---|---|
| Filter vs hunt/target, 12 seeds | 11–1, 0 incidents |
| vs `demo`, 12 seeds | 12–0, all fleet destroyed, 0 incidents |

### Time and memory

If `time_remaining_s < 0.5`, fall back to a cheap adjacent or random shot. Updates are vectorised with numpy.

### Limits

Ships are treated as independent in the occupancy sum; the transition model is an estimate. With more time: particle filtering over the joint fleet or a tighter value-of-information rule for sonar.

---

## Catan

### Problem formulation

**PEAS.** Performance: first to 7 victory points (or win adjudication). Environment: 1v1 Catan, dice, robber, no player trading, 5 s clock. Actuator: `{"action": id}`. Sensors: legal actions, `me`, public `opponent`, board, log.

Partially observable, multi-agent, stochastic, sequential, semi-dynamic, discrete.

| | Abstraction |
|---|---|
| State | `state_features`: phase, my VP, rival visible VP, affordance, hand-size bucket, round bucket |
| Actions | Legal ids; Q keys use action type |
| Reward (training) | Δ VP between decisions + win/loss bonus |
| Competing policy | Heuristic action scores |

**Certain public facts.** Settlements, cities, roads, visible VP, played knights, and that building implies the opponent had the cost. We do not claim to know hidden hands or VP cards.

**Planning view (preconditions / effects):**

| Action | Preconditions (approx.) | Effects |
|---|---|---|
| `BUILD_CITY` | Own settlement; pay wheat/ore | −resources; city; +1 VP; more production |
| `BUILD_SETTLEMENT` | Afford cost; legal node | −resources; settlement; +1 VP |
| `BUILD_ROAD` | Afford cost or free-roads; legal edge | −resources; road; longest-road race |
| `BUY_DEVELOPMENT_CARD` | Afford cost; cards left | −resources; +hidden card |
| `PLAY_KNIGHT_CARD` | Knight in hand | Robber; army race |
| `MARITIME_TRADE` | Enough to give | −give; +receive |
| `END_TURN` / `ROLL` | Phase allows | Pass / dice |

### Algorithms

- **Heuristic (`heuristic_policy`)**: one-step utilities from the table above — this is the strategy we compete with.
- **`state_features` / `action_value` / `q_update`**: small MDP abstraction and tabular Q-learning. `q_update` implements q + α(r + γ max Q′ − q).
- Offline training produced `Q_TABLE`. An `"improved"` blend adds a learned type-advantage on top of the heuristic; after measurement we do **not** use that blend in competition.
- We do not run expectiminimax over dice under the 5 s clock; chance is reflected in heuristic terms and in training rewards.

### Baseline against improved version

| Test | Result |
|---|---|
| Heuristic vs Q-blend, **500** games | Heuristic **276** – Q-blend **224** |
| Competing choice | Heuristic (`STRATEGY = "baseline"`) |
| vs demos / full match | Strong (see Tests) |

`action_value` still returns learned Q values when present, so the required learning interface is real; the measured winner for play is the heuristic.

### Time and memory

Each decision is a cheap heuristic pass. Load time is about 1 ms; no training at import.

### Limits

Q keys are by action type, not full arguments. With more time: richer features, longer training against stronger rivals, or shallow expectiminimax.
