import streamlit as st
import numpy as np
import joblib

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(
    page_title="Predict Insurance Premium",
    layout="wide"
)

# ----------------------
# LOAD MODEL
# ----------------------
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# ----------------------
# HEADER
# ----------------------
st.title("🔮 Insurance Premium Prediction")
st.markdown("Enter your details below to get an estimated insurance premium.")

# ----------------------
# INPUT FORM
# ----------------------
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Personal Info")
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        height = st.number_input("Height (cm)", min_value=100, max_value=220, value=170)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        surgeries = st.selectbox("Number of Major Surgeries", [0, 1, 2, 3])

    with col2:
        st.subheader("Health Conditions")
        diabetes = st.selectbox("Diabetes", ["No", "Yes"])
        bp = st.selectbox("Blood Pressure Problems", ["No", "Yes"])
        chronic = st.selectbox("Any Chronic Diseases", ["No", "Yes"])

    with col3:
        st.subheader("Medical History")
        transplant = st.selectbox("Any Transplants", ["No", "Yes"])
        allergies = st.selectbox("Known Allergies", ["No", "Yes"])
        cancer_history = st.selectbox("Family History of Cancer", ["No", "Yes"])

    submitted = st.form_submit_button(
        "💰 Predict Premium",
        use_container_width=True
    )

# ----------------------
# PREDICTION
# ----------------------
if submitted:
    # Convert Yes/No to 1/0
    diabetes_val = 1 if diabetes == "Yes" else 0
    bp_val = 1 if bp == "Yes" else 0
    chronic_val = 1 if chronic == "Yes" else 0
    transplant_val = 1 if transplant == "Yes" else 0
    allergies_val = 1 if allergies == "Yes" else 0
    cancer_val = 1 if cancer_history == "Yes" else 0

    # Feature engineering (must match training)
    bmi = weight / ((height / 100) ** 2)

    # Prepare features (order must match training)
    features = np.array([[
        age, bmi, surgeries,
        diabetes_val, bp_val, chronic_val,
        transplant_val, allergies_val, cancer_val
    ]])

    # Predict (log scale) and convert back
    log_premium = model.predict(features)[0]
    premium = np.expm1(log_premium)

    # ----------------------
    # DISPLAY RESULTS
    # ----------------------
    st.markdown("---")
    st.subheader("Prediction Result")

    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted Premium", f"₹{premium:,.0f}")
    col2.metric("Your BMI", f"{bmi:.1f}")
    col3.metric("Age", age)

    # Risk summary
    risk_factors = []
    if diabetes_val:
        risk_factors.append("Diabetes")
    if bp_val:
        risk_factors.append("Blood Pressure")
    if chronic_val:
        risk_factors.append("Chronic Disease")
    if transplant_val:
        risk_factors.append("Transplant History")
    if cancer_val:
        risk_factors.append("Family Cancer History")
    if allergies_val:
        risk_factors.append("Allergies")

    if risk_factors:
        st.warning(f"⚠️ Risk factors identified: {', '.join(risk_factors)}")
    else:
        st.success("✅ No major risk factors identified.")