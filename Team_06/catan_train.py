
import argparse
import os
import random
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from games.catan.engine import SIDE_OF, adjudicate, legal_actions, new_game, observation_for, victory_points  # noqa: E402

import catan_agent as agent  

GAMMA = 0.97
WIN_BONUS = 2.0
MIN_VISITS = 30


def choose(observation, epsilon, rng):
    """Heuristic action, or with probability epsilon the best action of a random type."""
    scores = agent.heuristic_scores(observation)
    actions = observation["actions"]
    if rng.random() < epsilon:
        kind = rng.choice(sorted({a["type"] for a in actions}))
        actions = [a for a in actions if a["type"] == kind]
    best = max(actions, key=lambda a: (scores[a["id"]], -a["id"]))
    return best


def best_q(q, features, kinds):
    return max(q.get(agent.q_key(features, kind), 0.0) for kind in kinds)


def train(games, seed, epsilon_start, epsilon_end):
    rng = random.Random(seed)
    q, visits = {}, {}

    def update(key, reward, next_best):
        visits[key] = visits.get(key, 0) + 1
        alpha = max(0.01, 1.0 / visits[key])
        q[key] = agent.q_update(q.get(key, 0.0), reward, next_best, alpha, GAMMA)

    started = time.time()
    results = {"A": 0, "B": 0, None: 0}
    for episode in range(games):
        epsilon = epsilon_start + (epsilon_end - epsilon_start) * episode / max(games - 1, 1)
        game = new_game(seed * 1_000_003 + episode + 1, vps_to_win=7)
        pending = {"A": None, "B": None}  # side -> (key, vp at that decision)
        while game.winning_color() is None and game.state.num_turns // 2 < 100:
            actions = legal_actions(game)
            if len(actions) == 1:
                game.execute(actions[0])
                continue
            side = SIDE_OF[game.state.current_color()]
            observation = observation_for(game, side, actions, None, {"max_rounds": 100})
            features = agent.state_features(observation)
            vp = observation["me"]["victory_points"]
            if pending[side] is not None:
                key, vp_before = pending[side]
                kinds = {a["type"] for a in observation["actions"]}
                update(key, vp - vp_before, best_q(q, features, kinds))
            action = choose(observation, epsilon, rng)
            pending[side] = (agent.q_key(features, action["type"]), vp)
            game.execute(actions[action["id"]])
        champion = game.winning_color()
        winner = SIDE_OF[champion] if champion is not None else adjudicate(game)[0]
        results[winner] += 1
        final = victory_points(game)
        for side, item in pending.items():
            if item is None:
                continue
            key, vp_before = item
            bonus = 0.0 if winner is None else (WIN_BONUS if winner == side else -WIN_BONUS)
            update(key, final[side] - vp_before + bonus, 0.0)
        if (episode + 1) % 2000 == 0:
            trusted = sum(1 for n in visits.values() if n >= MIN_VISITS)
            print(f"{episode + 1} games, {len(q)} entries, {trusted} trusted, "
                  f"epsilon {epsilon:.3f}, {time.time() - started:.0f}s", flush=True)
    return q, visits


def write_table(q, visits, path):
    table = {key: round(value, 3) for key, value in sorted(q.items()) if visits[key] >= MIN_VISITS}
    with open(path) as f:
        source = f.read()
    block = "# BEGIN LEARNED TABLE\nQ_TABLE = " + repr(table) + "\n# END LEARNED TABLE"
    source = re.sub(r"# BEGIN LEARNED TABLE\n.*?# END LEARNED TABLE", lambda _: block, source, flags=re.S)
    with open(path, "w") as f:
        f.write(source)
    return len(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=30000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--epsilon-start", type=float, default=0.2)
    parser.add_argument("--epsilon-end", type=float, default=0.05)
    parser.add_argument("--workers", type=int, default=1, help="independent learners, merged at the end")
    parser.add_argument("--out", default=os.path.join(HERE, "catan_agent.py"))
    args = parser.parse_args()
    if args.workers <= 1:
        q, visits = train(args.games, args.seed, args.epsilon_start, args.epsilon_end)
    else:
        from multiprocessing import Pool
        jobs = [(args.games // args.workers, args.seed + i, args.epsilon_start, args.epsilon_end)
                for i in range(args.workers)]
        with Pool(args.workers) as pool:
            parts = pool.starmap(train, jobs)
        # Merge: visit-weighted average of each learner's estimate.
        q, visits = {}, {}
        for part_q, part_visits in parts:
            for key, value in part_q.items():
                n = part_visits[key]
                total = visits.get(key, 0) + n
                q[key] = (q.get(key, 0.0) * visits.get(key, 0) + value * n) / total
                visits[key] = total
    kept = write_table(q, visits, args.out)
    print(f"wrote {kept} trusted entries (of {len(q)}) to {args.out}")
