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
| [Team_06/README.md](Team_06/README.md) | **Submission README** — algorithms, tests, analysis, class-informed plan, technical write-ups |
| [class_lessons.md](class_lessons.md) | Course methods from Sessions 01–26 |
| [docs/students/README.md](docs/students/README.md) | Official student guide |
| [docs/students/ASSIGNMENT.md](docs/students/ASSIGNMENT.md) | Required algorithms and what to explain |
| [docs/students/CHALLENGES.md](docs/students/CHALLENGES.md) | The four challenges in one page |
| [assignment_materials/](assignment_materials/) | Handbook PDF + group-assignment slides |
| [Tournament.ipynb](Tournament.ipynb) | Judge notebook (Colab / local) |

## Repo layout

```
Team_06/                  ← our four agents + hand-in README
  roadtrip_agent.py
  chess_agent.py
  battleship_agent.py
  catan_agent.py          ← teammate finishing this
  README.md
class_lessons.md
docs/students/
games/
examples/
tournament/
assignment_materials/
```

## Agent status (snapshot)

| Challenge | Status |
|---|---|
| Road Trip | Strong — UCS/A*/SA; 4/4 checks; beats demo & baseline |
| Chess | Strong — rich eval, αβ + ID + TT + quiescence; 3/3 checks; beats demo & baseline |
| Battleship | Strong — CSP + Bayes + belief filter; 3/3 checks; 12–0 vs demo, 11–1 vs baseline |
| Catan | In progress by another team member |

## What we changed (Road Trip, Chess, Battleship)

Full detail lives in [Team_06/README.md](Team_06/README.md). Short version:

| Agent | What we did |
|---|---|
| **Chess** | Full rewrite of the playing agent: richer linear eval, iterative deepening, transposition table, quiescence, safe clock use, `STRATEGY` baseline vs improved. Required `evaluate` / `minimax` / `alphabeta` pass 3/3. |
| **Battleship** | Kept the belief filter; added Team 06 / class mapping, `STRATEGY` hunt-target baseline vs filter, and measured matches (12–0 vs demo, 11–1 vs baseline). Required CSP/Bayes/predict pass 3/3. |
| **Road Trip** | No redesign — already matched class methods. Re-verified checks and races; refreshed README numbers (10–0 vs demo; 10–5–0 vs baseline on 15 seeds). |
| **Catan** | Untouched here — teammate finishing it. |

## Run / practise

```bash
pip install -r requirements.txt
# Or use Tournament.ipynb in Google Colab
```

```python
practice = run_game("chess", "Team_06/chess_agent.py", opponent="demo")
check_requirements("Team_06")
```
