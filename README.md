# AI Agent Tournament — Team 06

IE University · AI: Reasoning & Problem Solving  
Group assignment: four Python agents for a knockout tournament (Road Trip, Chess, Battleship, Catan).

## Team

- Alex Garcia
- Alejandro Zapata
- Alesia Dako
- Kohana Rakipi
- Viktoriia Stepanenko
- Laura Somogyi

## Quick links

| Doc | What it is |
|---|---|
| [Team_06/README.md](Team_06/README.md) | **Submission README** — algorithms, tests, analysis, technical write-ups |
| [class_lessons.md](class_lessons.md) | Course methods from Sessions 01–26 |
| [docs/students/README.md](docs/students/README.md) | Official student guide |
| [docs/students/ASSIGNMENT.md](docs/students/ASSIGNMENT.md) | Required algorithms and what to explain |
| [Tournament.ipynb](Tournament.ipynb) | Judge notebook |

## Agent status

| Challenge | Status |
|---|---|
| Road Trip | Strong — UCS/A*/SA; beats demo & baseline |
| Chess | Strong — rich eval + αβ/ID/TT/quiescence |
| Battleship | Strong — CSP + Bayes + belief filter |
| Catan | Strong — heuristic competes; Q table kept for learning checks |

**`check_requirements("Team_06")`: 14/14 PASS.**  
Full match vs `demo_a` (seed 42): **Team_06 advances 4–0**, 0 incidents.

## What we changed

| Agent | Change |
|---|---|
| **Chess** | Rewritten eval/search; baseline vs improved |
| **Battleship** | Baseline hunt/target vs belief filter; docs/tests |
| **Road Trip** | Re-verified (already course-aligned) |
| **Catan** | Integrated teammate agent; `STRATEGY`; train markers; **500-game** heuristic vs Q (heuristic wins 276–224) → default `STRATEGY="baseline"` |

## Hand-in reminder

Zip `Team_06/` with the four agents + `README.md`. Still needed separately: generative-AI line in the README, presentation PDF on Blackboard.

## Run

```bash
pip install -r requirements.txt
```

```python
check_requirements("Team_06")
run_match(team_a="Team_06", team_b="demo_a", seed=42)
```
