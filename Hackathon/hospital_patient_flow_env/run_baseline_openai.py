import argparse
import json
import os
import random

from openai import OpenAI

from env.environment import HospitalEnvironment
from env.models import AdmitPatient, ExpediteDischarge, NoOp
from env.grader import compute_score


# -------------------------
# OpenAI client
# -------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------
# LLM-based policy
# -------------------------
def llm_policy(state):
    """
    Uses OpenAI to decide the next action.
    Deterministic via temperature=0.
    """

    prompt = f"""
You are a hospital operations coordinator.

Current hospital state:
- ICU beds: {state.beds['icu']['occupied']} / {state.beds['icu']['total']}
- General beds: {state.beds['general']['occupied']} / {state.beds['general']['total']}
- ER queue size: {len(state.emergency_queue)}
- Pending discharges: {state.pending_discharges}

ER patients:
{[
    {'id': p.patient_id, 'acuity': p.acuity_level, 'wait': p.wait_time_hours}
    for p in state.emergency_queue
]}

Choose ONE action.

Allowed actions (respond in JSON only):
1. AdmitPatient {{ "patient_id": int, "target_unit": "icu" | "general" }}
2. ExpediteDischarge {{ "count": int }}
3. NoOp {{ "reason": string }}

Rules:
- Prefer higher-acuity patients
- Do not invent patient IDs
- Be conservative

Respond ONLY with valid JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # small, fast, stable
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=150,
    )

    content = response.choices[0].message.content.strip()

    action_json = json.loads(content)

    # -------------------------
    # Parse into action objects
    # -------------------------
    if "AdmitPatient" in action_json:
        a = action_json["AdmitPatient"]
        return AdmitPatient(
            patient_id=a["patient_id"],
            target_unit=a["target_unit"]
        )

    if "ExpediteDischarge" in action_json:
        a = action_json["ExpediteDischarge"]
        return ExpediteDischarge(count=a["count"])

    return NoOp(reason=action_json.get("NoOp", {}).get("reason", "llm_default"))


# -------------------------
# Main runner
# -------------------------
def main(task, seed):
    random.seed(seed)

    env = HospitalEnvironment()
    env.reset(task_id=task, seed=seed)

    done = False
    total_reward = 0.0
    steps = 0

    while not done:
        state = env.state()
        action = llm_policy(state)
        _, reward, done, _ = env.step(action)
        total_reward += reward
        steps += 1

    metrics = env.get_metrics()
    score = compute_score(metrics)

    print("===== OPENAI BASELINE RESULT =====")
    print(f"Task  : {task}")
    print(f"Steps : {steps}")
    print(f"Reward: {round(total_reward, 3)}")
    print(f"Score : {round(score, 3)}")
    print("==================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["easy", "medium", "hard"], default="easy")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    main(args.task, args.seed)