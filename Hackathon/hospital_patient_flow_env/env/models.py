from pydantic import BaseModel
from typing import List, Dict, Literal


# ---------------- STATE ----------------

class ERPatient(BaseModel):
    patient_id: int
    acuity_level: int
    wait_time_hours: float


class HospitalState(BaseModel):
    time_hour: int
    beds: Dict[str, Dict[str, int]]
    emergency_queue: List[ERPatient]
    pending_discharges: int
    staff_levels: Dict[str, int]


# ---------------- ACTIONS ----------------

class AdmitPatient(BaseModel):
    patient_id: int
    target_unit: Literal["icu", "general"]

class TransferPatient(BaseModel):
    from_unit: Literal["icu", "general"]
    to_unit: Literal["icu", "general"]
    count: int


class ExpediteDischarge(BaseModel):
    count: int


class DelayAdmission(BaseModel):
    patient_id: int


class NoOp(BaseModel):
    reason: str