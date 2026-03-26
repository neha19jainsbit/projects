import random
from env.models import *


class HospitalEnvironment:
    def __init__(self):
        self.state_obj = None
        self.current_time = 0
        self.max_time = 0
        self.metrics = {}

    # ---------------- RESET ----------------
    def reset(self, task_id: str, seed: int):
        random.seed(seed)

        if task_id == "easy":
            self.max_time = 24
            beds = {
                "icu": {"total": 12, "occupied": 5},
                "general": {"total": 60, "occupied": 25}
            }
            staff = {"nurses": 20, "doctors": 10}

        elif task_id == "medium":
            self.max_time = 48
            beds = {
                "icu": {"total": 10, "occupied": 8},
                "general": {"total": 50, "occupied": 40}
            }
            staff = {"nurses": 14, "doctors": 7}

        else:  # hard
            self.max_time = 72
            beds = {
                "icu": {"total": 8, "occupied": 7},
                "general": {"total": 45, "occupied": 38}
            }
            staff = {"nurses": 10, "doctors": 5}

        self.current_time = 0

        self.state_obj = HospitalState(
            time_hour=0,
            beds=beds,
            emergency_queue=[],
            pending_discharges=6,
            staff_levels=staff
        )

        self.metrics = {
            "arrivals": 0,
            "admitted": 0,
            "total_er_wait": 0.0,
            "idle_steps": 0
        }

    # ---------------- STATE ----------------
    def state(self):
        return self.state_obj

    # ---------------- STEP ----------------
    def step(self, action):
        print("\n--------------------------------------")
        print(f"⏰ Hour {self.current_time}")
        reward = 0.0

        # ---------- New ER arrivals ----------
        if random.random() < 0.7:
            new_patient = ERPatient(
                patient_id=self.metrics["arrivals"],
                acuity_level=random.randint(1, 5),
                wait_time_hours=0.0
            )
            self.state_obj.emergency_queue.append(new_patient)
            self.metrics["arrivals"] += 1

            print(
                f"🚑 New ER arrival | "
                f"ID={new_patient.patient_id}, "
                f"Acuity={new_patient.acuity_level}"
            )
        else:
            print("🚑 No ER arrivals this hour")

        # ---------- Action taken ----------
        print(f"🎯 Action taken: {action}")

        if isinstance(action, AdmitPatient):
            admitted = False
            for p in self.state_obj.emergency_queue:
                if p.patient_id == action.patient_id:
                    unit = action.target_unit
                    if self.state_obj.beds[unit]["occupied"] < self.state_obj.beds[unit]["total"]:
                        self.state_obj.beds[unit]["occupied"] += 1
                        self.state_obj.emergency_queue.remove(p)
                        self.metrics["admitted"] += 1
                        reward += 0.05
                        admitted = True
                        print(f"✅ Patient {p.patient_id} admitted to {unit.upper()}")
                    else:
                        reward -= 0.05
                        print(f"❌ No available {unit.upper()} beds")
                    break

            if not admitted:
                print("⚠️ Admission failed (patient not found)")

        elif isinstance(action, ExpediteDischarge):
            discharged = min(action.count, self.state_obj.pending_discharges)
            self.state_obj.pending_discharges -= discharged
            self.state_obj.beds["general"]["occupied"] -= discharged
            reward += 0.04 * discharged

            print(f"📤 Discharged {discharged} patients")

        elif isinstance(action, NoOp):
            self.metrics["idle_steps"] += 1
            reward -= 0.02
            print("⏸️ NoOp — agent did nothing")

        # ---------- Update waiting patients ----------
        if self.state_obj.emergency_queue:
            print("⌛ Updating ER wait times:")
        for p in self.state_obj.emergency_queue:
            p.wait_time_hours += 1
            self.metrics["total_er_wait"] += 1
            reward -= 0.03
            print(
                f"   Patient {p.patient_id} | "
                f"Wait={p.wait_time_hours}h | "
                f"Acuity={p.acuity_level}"
            )

        # ---------- Summary ----------
        print(
            f"🏥 ICU beds: {self.state_obj.beds['icu']['occupied']}/"
            f"{self.state_obj.beds['icu']['total']}"
        )
        print(
            f"🏥 General beds: {self.state_obj.beds['general']['occupied']}/"
            f"{self.state_obj.beds['general']['total']}"
        )
        print(f"🧍 ER queue size: {len(self.state_obj.emergency_queue)}")
        print(f"💰 Step reward: {round(reward, 3)}")

        # ---------- Advance time ----------
        self.current_time += 1
        self.state_obj.time_hour = self.current_time

        done = self.current_time >= self.max_time
        return self.state_obj, reward, done, {}

    # ---------------- METRICS ----------------
    def get_metrics(self):
        avg_wait = 0.0
        if self.metrics["arrivals"] > 0:
            avg_wait = self.metrics["total_er_wait"] / self.metrics["arrivals"]

        return {
            "arrivals": self.metrics["arrivals"],
            "admitted": self.metrics["admitted"],
            "avg_er_wait": avg_wait,
            "idle_frac": self.metrics["idle_steps"] / max(1, self.max_time)
        }