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
| [Team_06/README.md](Team_06/README.md) | **Submission README** — algorithms, tests, full code analysis, class-informed plan, technical write-up |
| [class_lessons.md](class_lessons.md) | Course methods from Sessions 01–26 to keep agents aligned with class |
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
  catan_agent.py
  README.md
class_lessons.md          ← class takeaways for the assignment
docs/students/            ← assignment docs + sample observations
games/                   ← challenge rules and engines
examples/                 ← weak demo teams
tournament/               ← judge code
assignment_materials/     ← handbook + brief
```

## Agent status (snapshot)

| Challenge | Status |
|---|---|
| Road Trip | Strong — UCS, A*, SA/local search, checks + races documented |
| Chess | Partial — minimax / αβ / eval + iterative deepening; write-up/tests thin |
| Battleship | Strong code (CSP + Bayes + belief filter); README/tests missing |
| Catan | **Unfinished** — random `act`, required functions not implemented |

**Biggest risk:** Catan blocks `check_requirements` (14/14) and the academic core of the grade (60% code/work). Full analysis and the work plan live in [Team_06/README.md](Team_06/README.md).

## Run / practise

```bash
pip install -r requirements.txt
# Or use Tournament.ipynb in Google Colab with the project zip
```

```python
practice = run_game("chess", "Team_06/chess_agent.py", opponent="demo")
check_requirements("Team_06")
```

Deadline context: zip + presentation PDF on Blackboard; in-class tournament and 5-minute presentation after that.
