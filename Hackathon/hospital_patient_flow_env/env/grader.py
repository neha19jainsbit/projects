def compute_score(metrics):
    admit_rate = metrics["admitted"] / max(1, metrics["arrivals"])
    wait_score = min(metrics["avg_er_wait"] / 20.0, 1.0)
    idle_penalty = metrics["idle_frac"]

    score = (
        0.4 * admit_rate +
        0.3 * (1 - wait_score) +
        0.3 * (1 - idle_penalty)
    )

    return max(0.0, min(1.0, score))