# Insurance Cost Prediction

## Problem Statement

Insurance companies need an accurate and transparent method to estimate health insurance premiums based on individual risk profiles. Manual underwriting is time-consuming, inconsistent, and does not scale. The goal of this project is to build a machine learning model that predicts insurance premium prices using demographic and health-related features, and deploy it as an interactive web application for real-time premium estimation.

## Target Metric

- **Primary Metric:** R² Score (coefficient of determination) — measures how well the model explains variance in premium prices
- **Supporting Metrics:** MAE (Mean Absolute Error) and RMSE (Root Mean Squared Error) on log-transformed premium prices

## Dataset

- **Records:** 986 individuals
- **Features (11):** Age, Diabetes, BloodPressureProblems, AnyTransplants, AnyChronicDiseases, Height, Weight, KnownAllergies, HistoryOfCancerInFamily, NumberOfMajorSurgeries, PremiumPrice (target)
- **Engineered Feature:** BMI (computed from Height and Weight)

---

## Steps Taken

### 1. Exploratory Data Analysis (EDA)

- **Distribution Analysis:** Premium prices are right-skewed and multi-modal, indicating distinct pricing tiers. Age is evenly distributed; BMI exhibits positive skew with extreme values representing high-risk individuals.
- **Correlation Analysis:** Age is the strongest linear predictor of premium price, followed by number of major surgeries. BMI and weight show weaker linear relationships but contribute through non-linear interactions. Strong multicollinearity exists between weight, height, and BMI.
- **Outlier Detection:** Both IQR and Z-score methods identified extreme premium and BMI values. These correspond to valid high-risk cases, not data errors. Log transformation (log1p) was applied to the target variable to reduce skewness while preserving risk information.

### 2. Hypothesis Testing

- **Welch's T-Tests:** Statistically significant differences (p < 0.05) in log-premiums were confirmed between individuals with and without diabetes, blood pressure problems, chronic diseases, transplants, allergies, and family cancer history.
- **One-Way ANOVA:** Premiums differ significantly across surgery groups, confirming surgical history as a critical cost driver.
- **Chi-Square Tests:**
  - Significant association between diabetes and blood pressure problems (co-occurring conditions)
  - Significant association between chronic diseases and number of major surgeries

### 3. Regression Analysis (OLS)

A multiple linear regression model (statsmodels OLS) confirmed that age, surgeries, diabetes, chronic diseases, and transplant history have statistically significant positive effects on log-premiums. This guided feature selection for ML models.

### 4. Machine Learning Modelling

**Features used (9):** Age, BMI, NumberOfMajorSurgeries, Diabetes, BloodPressureProblems, AnyChronicDiseases, AnyTransplants, KnownAllergies, HistoryOfCancerInFamily

**Target:** LogPremiumPrice (log1p-transformed)

#### Train-Test Split Results (80/20 split)

| Model               | R² Score | MAE   | RMSE  |
|----------------------|----------|-------|-------|
| Linear Regression    | 0.717    | 0.117 | 0.150 |
| Decision Tree        | 0.854    | 0.066 | 0.108 |
| Random Forest        | 0.897    | 0.055 | 0.091 |
| Gradient Boosting    | 0.887    | 0.063 | 0.095 |

#### 5-Fold Cross-Validation

Cross-validation confirmed that Random Forest achieves the highest R² with lowest variance across folds, making it the most stable and accurate model.

#### Final Model: Random Forest Regressor

- `n_estimators=200`, `max_depth=10`, `min_samples_split=10`
- **R² = 0.897** on test set
- Bootstrap prediction intervals (500 iterations) demonstrated well-calibrated uncertainty estimates

### 5. Feature Importance (Permutation Importance)

| Rank | Feature                    | Impact     |
|------|----------------------------|------------|
| 1    | Age                        | Dominant   |
| 2    | AnyTransplants             | High       |
| 3    | AnyChronicDiseases         | High       |
| 4    | BMI                        | Moderate   |
| 5    | NumberOfMajorSurgeries     | Moderate   |
| 6    | HistoryOfCancerInFamily    | Low        |
| 7    | Diabetes                   | Negligible |
| 8    | BloodPressureProblems      | Negligible |
| 9    | KnownAllergies             | Negligible |

---

## Final Scores

| Metric    | Value  |
|-----------|--------|
| **R²**    | 0.897  |
| **MAE**   | 0.055  |
| **RMSE**  | 0.091  |

The Random Forest model explains ~90% of the variance in log-transformed insurance premiums, with low average prediction error.

---

## Key Insights & Recommendations

1. **Age is the primary cost driver** — refine age-based pricing tiers and introduce preventive wellness programs for mid-age customers.
2. **Severe health conditions (transplants, chronic diseases) drive disproportionate premium increases** — apply appropriate risk loadings and offer care-management programs.
3. **BMI is a modifiable risk factor** — incentivize wellness and fitness programs; offer premium discounts for documented BMI improvement.
4. **Family cancer history provides a long-term risk signal** — use for enhanced screening, not aggressive pricing penalties.
5. **Diabetes, BP, and allergies have negligible standalone impact** — avoid over-penalizing isolated manageable conditions.
6. **Risk is best assessed holistically** — move from rule-based to risk-profile-based pricing using model-driven decisions.

---

## Deployment

### Architecture

```
insurance.csv → insurance.ipynb (EDA + Training) → model.pkl → app.py (Streamlit Prediction UI)
                                                              → app1.py (Streamlit Analytics Dashboard)
```

### Steps

1. **Model Training & Export:** The Random Forest model is trained in `insurance.ipynb` and serialized using `joblib` as `model.pkl`.
2. **Prediction Application (`app.py`):** A Streamlit application that:
   - Loads `model.pkl` at startup
   - Presents a user-friendly input form (age, height, weight, surgeries, health conditions)
   - Computes BMI from height/weight (matching the training pipeline)
   - Predicts log-premium using the model and converts back to actual premium via `expm1`
   - Displays the predicted premium, BMI, and identified risk factors
3. **Analytics Dashboard (`app1.py`):** A standalone Streamlit application with interactive filters and four analysis pages — Summary Statistics, Premium Pricing Analysis, Risk Factors Analysis, and Demographic Insights.

### Running the Applications

```bash
# Prediction App
python -m streamlit run app.py

# Analytics Dashboard
python -m streamlit run app1.py
```

---

## Project Structure

```
├── insurance.csv          # Raw dataset (986 records)
├── insurance.ipynb        # EDA, hypothesis testing, model training
├── model.pkl              # Serialized Random Forest model
├── app.py                 # Streamlit prediction application
├── app1.py                # Streamlit analytics dashboard
└── README.md              # Project documentation
```

## Tech Stack

- **Language:** Python
- **EDA & Stats:** pandas, numpy, scipy, seaborn, matplotlib, statsmodels
- **ML:** scikit-learn (RandomForestRegressor)
- **Deployment:** Streamlit, joblib
