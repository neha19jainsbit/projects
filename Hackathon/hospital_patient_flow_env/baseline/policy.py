from env.models import AdmitPatient, ExpediteDischarge, NoOp


def baseline_policy(state):
    # Admit highest acuity patient first
    if state.emergency_queue:
        patient = max(
            state.emergency_queue,
            key=lambda p: p.acuity_level
        )

        if state.beds["icu"]["occupied"] < state.beds["icu"]["total"]:
            return AdmitPatient(
                patient_id=patient.patient_id,
                target_unit="icu"
            )

        if state.beds["general"]["occupied"] < state.beds["general"]["total"]:
            return AdmitPatient(
                patient_id=patient.patient_id,
                target_unit="general"
            )

    # Try to free beds
    if state.pending_discharges > 0:
        return ExpediteDischarge(count=1)

    return NoOp(reason="no_safe_action")