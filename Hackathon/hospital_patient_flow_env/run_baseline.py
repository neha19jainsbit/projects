import argparse
import random

from env.environment import HospitalEnvironment
from baseline.policy import baseline_policy
from env.grader import compute_score


def main(task, seed):
    random.seed(seed)

    env = HospitalEnvironment()
    env.reset(task_id=task, seed=seed)

    done = False
    total_reward = 0.0
    steps = 0

    while not done:
        state = env.state()
        action = baseline_policy(state)
        _, reward, done, _ = env.step(action)
        total_reward += reward
        steps += 1

    metrics = env.get_metrics()
    score = compute_score(metrics)

    print("===== BASELINE RESULT =====")
    print(f"Task  : {task}")
    print(f"Total steps executed : {steps}")
    print(f"Reward: {round(total_reward, 3)}")
    print(f"Score : {round(score, 3)}")
    print("===========================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["easy", "medium", "hard"], default="easy")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    main(args.task, args.seed)