import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(
    page_title="Insurance Premium Analytics",
    layout="wide",
)

# ----------------------
# LOAD DATA
# ----------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    # Keep dataset lookup local to this standalone project for easy deployment.
    data_path = Path(__file__).resolve().parent / "insurance.csv"
    return pd.read_csv(data_path)


df = load_data()

# ----------------------
# FEATURE ENGINEERING
# ----------------------
df["BMI"] = df["Weight"] / ((df["Height"] / 100) ** 2)

df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[0, 25, 35, 45, 55, 65, 100],
    labels=["<25", "25-34", "35-44", "45-54", "55-64", "65+"],
)

binary_cols = [
    "Diabetes",
    "BloodPressureProblems",
    "AnyTransplants",
    "AnyChronicDiseases",
    "KnownAllergies",
    "HistoryOfCancerInFamily",
]

# ----------------------
# SIDEBAR FILTERS
# ----------------------
st.sidebar.title("Filters")

age_range = st.sidebar.slider(
    "Age",
    int(df.Age.min()),
    int(df.Age.max()),
    (18, 65),
)

bmi_range = st.sidebar.slider(
    "BMI",
    float(df.BMI.min()),
    float(df.BMI.max()),
    (15.0, 45.0),
)

filtered_df = df[(df.Age.between(*age_range)) & (df.BMI.between(*bmi_range))]

# ----------------------
# NAVIGATION
# ----------------------
st.sidebar.markdown("---")
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "",
    [
        "Summary Statistics",
        "Premium Pricing Analysis",
        "Risk Factors Analysis",
        "Demographic Insights",
    ],
)

# ======================================================
# SUMMARY STATISTICS
# ======================================================
if page == "Summary Statistics":
    st.title("Summary Statistics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Premium", f"Rs {filtered_df.PremiumPrice.mean():,.0f}")
    col2.metric("Average Age", round(filtered_df.Age.mean(), 1))
    col3.metric("Total Individuals", filtered_df.shape[0])

    st.subheader("Health Condition Distribution")

    fig = plt.figure(figsize=(10, 5))
    condition_counts = filtered_df[binary_cols].sum()
    sns.barplot(x=condition_counts.index, y=condition_counts.values)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ======================================================
# PREMIUM PRICING ANALYSIS
# ======================================================
elif page == "Premium Pricing Analysis":
    st.title("Premium Pricing Analysis")

    st.subheader("Premium Distribution")
    fig = px.histogram(
        filtered_df,
        x="PremiumPrice",
        nbins=30,
        color_discrete_sequence=["#2c3e50"],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average Premium by Age Group and Diabetes")
    fig = px.bar(
        filtered_df,
        x="AgeGroup",
        y="PremiumPrice",
        color="Diabetes",
        barmode="group",
        labels={"PremiumPrice": "Average Premium"},
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Correlation Heatmap")
    corr_cols = ["Age", "Height", "Weight", "BMI", "NumberOfMajorSurgeries", "PremiumPrice"]
    corr = filtered_df[corr_cols].corr()

    fig = plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    st.pyplot(fig)

# ======================================================
# RISK FACTORS ANALYSIS
# ======================================================
elif page == "Risk Factors Analysis":
    st.title("Risk Factors Analysis")

    st.subheader("Impact of Major Surgeries on Premium")
    fig = px.scatter(
        filtered_df,
        x="NumberOfMajorSurgeries",
        y="PremiumPrice",
        trendline="ols",
        size="BMI",
        hover_data=["Age"],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Premium by Chronic Conditions")
    fig = px.box(
        filtered_df,
        x="AnyChronicDiseases",
        y="PremiumPrice",
        color="AnyChronicDiseases",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Allergies and Family Cancer History")
    fig = px.bar(
        filtered_df,
        x="KnownAllergies",
        y="PremiumPrice",
        color="HistoryOfCancerInFamily",
        barmode="group",
    )
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# DEMOGRAPHIC INSIGHTS
# ======================================================
elif page == "Demographic Insights":
    st.title("Demographic Insights")

    st.subheader("Premium vs BMI")
    fig = px.scatter(
        filtered_df,
        x="BMI",
        y="PremiumPrice",
        color="Diabetes",
        size="NumberOfMajorSurgeries",
        hover_data=["Age", "Height", "Weight"],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("Geographical analysis not available (no region data in dataset).")
