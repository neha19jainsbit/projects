OpenEnv Compliance and Validation Scope

This project builds a realistic US Hospital Patient Flow OpenEnv environment that simulates non‑clinical hospital operations such as emergency department intake, bed allocation across ICU and general wards, and discharge coordination under staffing and capacity constraints. The environment exposes a standard OpenEnv interface with typed Pydantic observations and actions, supports reset, step, and state APIs, and includes three progressively harder tasks (easy, medium, hard) that model increasing congestion and resource scarcity. Agent performance is evaluated using deterministic graders that score outcomes on a normalized 0.0–1.0 scale based on throughput efficiency, ER wait times, and operational idleness, while a dense reward function provides partial progress signals throughout each episode. A reproducible baseline inference script demonstrates end‑to‑end interaction with the environment, making this a complete, real‑world benchmark for studying agent behavior in healthcare operations and capacity management.

This project implements a complete, real‑world OpenEnv environment for agent learning using the standard OpenEnv API:

Typed Observation and Action models using Pydantic
reset(), step(action) → (obs, reward, done, info), and state() methods
openenv.yaml metadata with three tasks of increasing difficulty
Deterministic graders scoring agent performance from 0.0 to 1.0
A dense reward function that penalizes undesirable behavior and rewards partial progress