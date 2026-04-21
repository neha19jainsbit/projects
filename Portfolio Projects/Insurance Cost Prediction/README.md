# EDA, Hypothesis Testing, and Premium Prediction for Insurance Dataset using Regression Models

---

## Contents

1. Introduction
2. Exploratory Data Analysis
3. Hypothesis Testing
4. Pre-Processing of Data before Modelling
5. Modelling
6. Comparison of Model Performance and Conclusions
7. Deployment
8. Business Insights and Recommendations
9. Further Studies

---

## 1. Introduction

### 1.1 About the Domain

Health insurance is a critical financial product that protects individuals from high medical costs. Insurance companies determine premium prices based on the risk profile of each policyholder. Traditionally, premium pricing relies on manual underwriting — a process that is time-consuming, inconsistent, and does not scale well with growing customer bases.

With the rise of data-driven decision-making, machine learning offers a way to automate and improve the accuracy and fairness of insurance pricing. By learning patterns from historical data, predictive models can estimate premiums in real time, reduce human bias, and provide transparent, explainable pricing.

### 1.2 Objective

a. Using the Insurance dataset, perform thorough EDA to draw meaningful conclusions and gain insights about the factors that drive insurance premium pricing.

b. Using the concepts of hypothesis testing and statistics, validate the EDA observations for the population data.

c. Predict insurance premium prices using regression models and deploy the best-performing model as a Streamlit web application.

### 1.3 Concepts Used

- Data Cleaning and Feature Engineering (BMI computation, log transformation)
- Exploratory Data Analysis (univariate, bivariate, correlation analysis)
- Outlier Detection (IQR method, Z-score method)
- Hypothesis Testing (Welch's t-test, One-Way ANOVA, Chi-Square test using scipy)
- Regression Analysis (OLS using statsmodels)
- Predictions using Regression Models (using scikit-learn)
- Model Validation (5-Fold Cross-Validation, Bootstrap Prediction Intervals)
- Feature Importance (Permutation Importance)
- Deployment (Streamlit, joblib)

### 1.4 Data Source

The dataset contains health and demographic information for 986 individuals along with their insurance premium prices. It includes both continuous features (Age, Height, Weight) and binary health indicators (Diabetes, Blood Pressure Problems, Transplants, Chronic Diseases, Allergies, Family Cancer History).

### 1.5 Column Profile

Before proceeding with the analysis, it is important to understand each column:

| Column | Description | Type |
|--------|-------------|------|
| `Age` | Age of the individual | Continuous |
| `Diabetes` | Whether the individual has diabetes (0: No, 1: Yes) | Binary |
| `BloodPressureProblems` | Whether the individual has blood pressure issues (0: No, 1: Yes) | Binary |
| `AnyTransplants` | Whether the individual has had any organ transplants (0: No, 1: Yes) | Binary |
| `AnyChronicDiseases` | Whether the individual has any chronic diseases (0: No, 1: Yes) | Binary |
| `Height` | Height in centimeters | Continuous |
| `Weight` | Weight in kilograms | Continuous |
| `KnownAllergies` | Whether the individual has known allergies (0: No, 1: Yes) | Binary |
| `HistoryOfCancerInFamily` | Whether there is a history of cancer in the family (0: No, 1: Yes) | Binary |
| `NumberOfMajorSurgeries` | Count of major surgeries undergone (0, 1, 2, 3) | Discrete |
| `PremiumPrice` | Insurance premium price in ₹ (target variable) | Continuous |

**Engineered Feature:**

| Column | Description | Derivation |
|--------|-------------|------------|
| `BMI` | Body Mass Index | `Weight / (Height / 100)²` |

---

## 2. Exploratory Data Analysis

This is the most critical phase of any data science project. EDA helps us understand the data, uncover hidden patterns, and identify key factors that influence the target variable. It also guides feature engineering and model selection.

We begin by importing the required libraries: pandas, numpy, matplotlib, seaborn, and scipy. Then we read the dataset and compute the BMI feature.

### 2.1 Univariate Analysis

**a. Premium Price (Target Variable)**

We first check the distribution of Premium Price since this is the feature we want to predict.

The distribution appears to be **right-skewed and multi-modal**, indicating distinct pricing tiers driven by varying health risk profiles. Since most statistical tests and regression algorithms perform better with normally distributed data, we apply a **log transformation** (`log1p`) to the target variable.

A violin plot reveals the density concentration across different premium ranges, while the KDE plot confirms non-linear pricing behavior — premium costs are influenced by combinations of demographic and health factors rather than isolated variables.

**b. Age**

Age is **evenly distributed** across the customer base, with individuals spread across all age brackets from 18 to 66. This uniform spread ensures that the model receives adequate representation from all age groups during training.

**c. BMI**

BMI exhibits a **positive skew** with extreme values at the upper end representing high-risk individuals. The majority of individuals fall within the normal to slightly overweight BMI range, but the tail contains clinically significant cases.

> **Key Insight:** Observed outliers in premium prices and BMI appear to represent valid high-risk cases and should be handled through transformation or robust modeling techniques instead of removal.

### 2.2 Bivariate / Correlation Analysis

We compute the correlation matrix for all numerical features and visualize it using a heatmap.

**Findings:**

- **Age** has the strongest linear correlation with Premium Price, confirming it as the most influential numerical predictor.
- **NumberOfMajorSurgeries** shows the second-strongest correlation, linking surgical history to higher costs.
- **BMI and Weight** show weaker linear relationships, suggesting their influence on premium pricing becomes significant only at extreme values through non-linear interactions.
- **Height** exhibits negligible correlation and offers little predictive value on its own.
- **Strong multicollinearity** exists between Weight, Height, and BMI — this highlights the need for careful feature selection, particularly when using linear models. We retain BMI (an engineered feature combining both) and drop raw Height and Weight from the model.

### 2.3 Outlier Detection

We apply two standard methods for outlier detection:

**IQR Method:**
We compute the interquartile range (Q1, Q3) and identify values beyond 1.5 × IQR from the quartiles. Outliers were detected in both PremiumPrice and BMI.

**Z-Score Method:**
Using scipy's zscore function, we flag records where the absolute Z-score exceeds 3. This method identified fewer outliers — confirming that only the most extreme values deviate significantly from the population mean.

**Visual Assessment:**
Box plots and KDE plots (with and without outliers) show that while outliers increase distribution skewness, they preserve critical risk information — these are genuine high-risk insurance cases, not data errors.

**Outlier Handling Strategy:**
Rather than removing outliers, we apply **logarithmic transformation** (`log1p`) to the target variable. Post-transformation box plots confirm that log scaling effectively compresses extreme values while retaining risk signals.

> **Key Insight:** Transformation-based techniques such as logarithmic scaling are preferred over outright removal, as the outliers represent valid high-risk cases critical for accurate premium prediction.

---

## 3. Hypothesis Testing

To validate the observations drawn from EDA for the population data, we conduct formal statistical tests using scipy's stats module. All tests are performed on the **log-transformed premium price** to satisfy normality and variance assumptions.

### 3.1 Do health conditions affect insurance premiums?

**Null Hypothesis (H₀):** Mean log-premium is similar for individuals with and without a given health condition.

**Alternative Hypothesis (Hₐ):** Mean log-premium differs between the two groups.

We run **Welch's t-test** (independent samples, unequal variance) at the 5% significance level for each binary health variable:

| Health Condition | p-value | Result |
|------------------|---------|--------|
| Diabetes | < 0.05 | Significant ✅ |
| BloodPressureProblems | < 0.05 | Significant ✅ |
| AnyChronicDiseases | < 0.05 | Significant ✅ |
| AnyTransplants | < 0.05 | Significant ✅ |
| KnownAllergies | < 0.05 | Significant ✅ |
| HistoryOfCancerInFamily | < 0.05 | Significant ✅ |

**Conclusion:** All six health conditions show statistically significant differences in premiums. This confirms that each health factor materially influences insurance pricing.

### 3.2 Does the number of major surgeries affect premiums?

**H₀:** Premiums are similar across all surgery groups (0, 1, 2, 3).

**Hₐ:** Premiums differ across surgery groups.

We use **One-Way ANOVA** since we are comparing more than two groups.

**Result:** p-value < 0.05 — we reject the null hypothesis. Premiums differ significantly across surgery groups, confirming that surgical history is a strong predictive feature.

### 3.3 Are health conditions associated with each other?

We run **Chi-Square tests of independence** to check if categorical health variables are related:

**a. Diabetes vs Blood Pressure Problems**

**H₀:** Diabetes and Blood Pressure Problems are independent.

**Result:** p-value < 0.05 — Significant association ✅. These conditions frequently co-occur, suggesting shared underlying risk factors.

**b. Chronic Diseases vs Transplants**

**H₀:** Chronic Diseases and Transplants are independent.

**Result:** p-value < 0.05 — Significant association ✅.

**c. Chronic Diseases vs Surgery Groups**

**H₀:** Chronic Diseases and Number of Major Surgeries are independent.

**Result:** p-value < 0.05 — Significant association ✅. This highlights that individuals with chronic diseases tend to undergo more surgeries, reflecting underlying health severity patterns.

> **Key Insight:** Hypothesis testing confirms that all health features are statistically relevant to premium pricing. Additionally, certain conditions co-occur (diabetes & blood pressure, chronic diseases & surgeries), which the model must capture through interaction effects or non-linear learning.

---

## 4. Pre-Processing of Data before Modelling

### 4.1 Feature Engineering

- **BMI:** Computed from Height and Weight as `Weight / (Height / 100)²`. This replaces the raw Height and Weight columns, reducing multicollinearity while preserving the health-relevant information.
- **LogPremiumPrice:** Log transformation (`log1p`) applied to the target variable to normalize the distribution and reduce the impact of extreme values.

### 4.2 Feature Selection

Based on EDA, correlation analysis, hypothesis testing, and OLS regression results, the following 9 features were selected as predictors:

1. Age
2. BMI
3. NumberOfMajorSurgeries
4. Diabetes
5. BloodPressureProblems
6. AnyChronicDiseases
7. AnyTransplants
8. KnownAllergies
9. HistoryOfCancerInFamily

### 4.3 OLS Regression Analysis (Statsmodels)

Before building ML models, a multiple linear regression model was fitted using statsmodels OLS to understand the statistical significance of each predictor.

**Findings:**
- Age, NumberOfMajorSurgeries, Diabetes, AnyChronicDiseases, and AnyTransplants have **statistically significant positive effects** on premiums (p < 0.05).
- BMI shows a **weaker but meaningful contribution**.
- The model confirms that insurance pricing is strongly driven by health severity and age-related risk factors.
- This analysis guided the final feature set for ML models.

### 4.4 Train-Test Split

The data was split into **80% training** and **20% testing** sets using `train_test_split` with `random_state=42` for reproducibility.

### 4.5 Scaling

For Linear Regression, `StandardScaler` was applied to normalize feature magnitudes. Tree-based models (Decision Tree, Random Forest, Gradient Boosting) do not require scaling due to their split-based decision logic.

---

## 5. Modelling

We need to predict insurance premiums — this is a **regression problem**. We train multiple regression models and compare their performance using **R² Score**, **MAE** (Mean Absolute Error), and **RMSE** (Root Mean Squared Error) on log-transformed premiums.

### 5.1 Linear Regression (Baseline)

The baseline Linear Regression model was trained on scaled features.

**Results:**
| Metric | Value |
|--------|-------|
| R² Score | 0.717 |
| MAE | 0.117 |
| RMSE | 0.150 |

The model accounts for approximately 72% of the variance in log-premiums. Age emerges as the most influential predictor, followed by transplant history and chronic diseases. However, the model struggles to capture non-linear interactions between features, motivating the use of tree-based models.

### 5.2 Decision Tree Regressor

A Decision Tree with `max_depth=5` was trained on unscaled features.

**Results:**
| Metric | Value |
|--------|-------|
| R² Score | 0.854 |
| MAE | 0.066 |
| RMSE | 0.108 |

Significant improvement over Linear Regression. The tree structure naturally captures feature interactions and non-linear patterns. However, single decision trees are prone to overfitting and high variance.

### 5.3 Random Forest Regressor

An ensemble of 200 decision trees with `max_depth=10` and `min_samples_split=10`.

**Results:**
| Metric | Value |
|--------|-------|
| R² Score | 0.897 |
| MAE | 0.055 |
| RMSE | 0.091 |

The best-performing model. Random Forest reduces the variance problem of individual trees through bagging (bootstrap aggregation), while maintaining the ability to capture complex non-linear relationships.

### 5.4 Gradient Boosting Regressor

A sequential boosting ensemble with 200 estimators, `learning_rate=0.05`, and `max_depth=3`.

**Results:**
| Metric | Value |
|--------|-------|
| R² Score | 0.887 |
| MAE | 0.063 |
| RMSE | 0.095 |

Strong performance, very close to Random Forest. Gradient Boosting builds trees sequentially to correct previous errors, but with this dataset size, Random Forest achieves slightly better generalization.

---

## 6. Comparison of Model Performance and Conclusions

### 6.1 Train-Test Split Summary

| Model | R² Score | MAE | RMSE |
|-------|----------|-----|------|
| Linear Regression | 0.717 | 0.117 | 0.150 |
| Decision Tree | 0.854 | 0.066 | 0.108 |
| **Random Forest** | **0.897** | **0.055** | **0.091** |
| Gradient Boosting | 0.887 | 0.063 | 0.095 |

### 6.2 5-Fold Cross-Validation

To ensure the results are not an artifact of a single train-test split, we performed 5-Fold Cross-Validation using `KFold` with `shuffle=True`. Three models were compared: Linear Regression (with StandardScaler pipeline), Random Forest, and Gradient Boosting.

Cross-validation confirmed that **Random Forest achieves the highest R² with the lowest variance** across folds, indicating superior generalization and model stability. While Gradient Boosting delivers comparable performance, **Random Forest exhibits more consistent accuracy, making it the preferred model for final deployment.**

### 6.3 Final Model Selection: Random Forest Regressor

**Configuration:**
- `n_estimators=200`
- `max_depth=10`
- `min_samples_split=10`
- `random_state=42`

**Final Test Scores:**

| Metric | Value |
|--------|-------|
| **R²** | **0.897** |
| **MAE** | **0.055** |
| **RMSE** | **0.091** |

The Random Forest model explains **~90% of the variance** in log-transformed insurance premiums with low average prediction error.

### 6.4 Bootstrap Prediction Intervals

To quantify prediction uncertainty, 500 bootstrap iterations were performed. For each iteration, the model was retrained on a resampled training set and predictions were generated on the test set. The 5th and 95th percentiles across all iterations define the **90% prediction interval**.

The relatively narrow and well-calibrated intervals indicate high confidence for most predictions. Slightly wider intervals for complex risk profiles reflect appropriate caution. This uncertainty-aware approach enhances reliability and transparency, making the model suitable for real-world deployment.

### 6.5 Permutation Feature Importance

To understand which features drive the model's predictions, Permutation Importance was computed (10 repeats, RMSE-based scoring):

| Rank | Feature | Impact |
|------|---------|--------|
| 1 | Age | Dominant |
| 2 | AnyTransplants | High |
| 3 | AnyChronicDiseases | High |
| 4 | BMI | Moderate |
| 5 | NumberOfMajorSurgeries | Moderate |
| 6 | HistoryOfCancerInFamily | Low |
| 7 | Diabetes | Negligible |
| 8 | BloodPressureProblems | Negligible |
| 9 | KnownAllergies | Negligible |

**Key observations:**
- **Age** is the dominant predictor, confirming its central role in risk assessment.
- **Transplant history and chronic diseases** are the next most important drivers, reflecting long-term, high-severity medical risk.
- **BMI** contributes meaningfully through non-linear interactions, even though its linear correlation appears moderate.
- **Diabetes, blood pressure, and allergies** show negligible standalone importance — their effects are absorbed by more severe overlapping health features.
- The feature importance structure aligns with clinical and actuarial expectations, reinforcing confidence in the model's interpretability.

---

## 7. Deployment

### 7.1 Architecture

```
insurance.csv → insurance.ipynb (EDA + Training) → model.pkl
                                                      ↓
                                              app.py (Streamlit Prediction UI)
                                              app1.py (Streamlit Analytics Dashboard)
```

### 7.2 Model Serialization

The final Random Forest model is serialized using `joblib` and saved as `model.pkl`. The saved model is verified by loading it back and generating predictions on sample data.

### 7.3 Prediction Application (`app.py`)

A **Streamlit** web application that provides real-time premium prediction:

- Loads `model.pkl` at startup using `st.cache_resource` for efficient caching
- Presents a user-friendly input form organized in three columns:
  - **Personal Info:** Age, Height (cm), Weight (kg), Number of Major Surgeries
  - **Health Conditions:** Diabetes, Blood Pressure Problems, Chronic Diseases
  - **Medical History:** Transplants, Allergies, Family Cancer History
- Computes BMI from height and weight (matching the training pipeline)
- Predicts log-premium using the model and converts back to actual premium using `expm1`
- Displays the predicted premium (₹), computed BMI, and a summary of identified risk factors

### 7.4 Analytics Dashboard (`app1.py`)

A standalone Streamlit application with interactive sidebar filters (Age range, BMI range) and four analysis pages:

1. **Summary Statistics** — Key metrics (average premium, average age, total individuals) and health condition distributions
2. **Premium Pricing Analysis** — Premium histograms, age group comparisons, and correlation heatmaps
3. **Risk Factors Analysis** — Surgery impact scatter plots, chronic condition box plots, allergy and cancer history comparisons
4. **Demographic Insights** — Premium vs BMI scatter plots with diabetes and surgery overlays

### 7.5 Running the Applications

```bash
# Prediction App
python -m streamlit run app.py

# Analytics Dashboard
python -m streamlit run app1.py
```

---

## 8. Business Insights and Recommendations

### 8.1 Age Is the Primary Cost Driver

Insurance premiums increase significantly with age, making it the single strongest determinant of cost.

**Actionable use:**
- Refine age-based pricing tiers
- Introduce preventive health programs and wellness incentives for mid-age customers to delay risk escalation
- Forecast long-term liabilities more accurately for aging customer segments

### 8.2 Severe Health Conditions Drive Disproportionate Premium Increases

Transplant history and chronic diseases substantially increase insurance costs, even after accounting for age and other factors. These conditions reflect persistent, high-severity medical risk.

**Actionable use:**
- Apply risk loadings or specialized plans for high-severity cases
- Design targeted care-management or disease-monitoring programs
- Flag these customers for proactive medical coordination to reduce long-term claims

### 8.3 BMI Is a Modifiable Risk Factor with Non-Linear Impact

BMI meaningfully influences premiums through non-linear interactions, especially at higher ranges. Unlike age or transplant history, BMI is potentially controllable.

**Actionable use:**
- Offer wellness, nutrition, and fitness incentives
- Create premium discounts or rebates for documented BMI improvement
- Shift part of risk management from pricing to prevention

### 8.4 Family Cancer History Adds Long-Term Risk Signal

Family history of cancer raises premiums modestly, indicating future risk rather than immediate cost.

**Actionable use:**
- Introduce enhanced screening programs for high-risk individuals
- Use this feature for early risk detection, not aggressive pricing penalties
- Improve long-term cost planning and reserve estimation

### 8.5 Minor Health Indicators Do Not Independently Drive Costs

Diabetes, blood pressure problems, and known allergies show negligible standalone importance once severe conditions are considered. Their impact is largely absorbed through more serious health features.

**Actionable use:**
- Avoid over-penalizing customers for isolated or manageable conditions
- Use these variables primarily for monitoring and interaction effects, not direct premium hikes
- Improve fairness and customer trust in pricing decisions

### 8.6 Risk Is Best Assessed Holistically

The model confirms that insurance risk compounds rather than adding linearly. High premiums emerge from combinations of age, severity, and cumulative health burden.

**Actionable use:**
- Move from rule-based pricing to risk-profile-based pricing
- Support underwriting decisions with model-driven explanations
- Enable personalized pricing strategies rather than blanket adjustments

### 8.7 The Pricing Model Is Transparent and Defensible

Feature importance aligns with clinical logic and actuarial practice, increasing confidence in adoption. The model supports explainable pricing, which is critical for regulatory review, internal governance, and customer communication.

**Summary:** Age and severe medical history dominate insurance cost predictions. Preventive and wellness-focused interventions offer genuine cost-control opportunities. The model enables accurate, fair, and transparent pricing — supporting both profitability and customer trust.

---

## 9. Further Studies

a. **Advanced Models:** Experiment with XGBoost, LightGBM, and neural networks to explore further performance gains.

b. **Feature Interactions:** Build polynomial or interaction features to explicitly model non-linear relationships between BMI, age, and surgery count.

c. **Additional Data:** Incorporate geographic region, income level, smoking status, and claim history for richer risk profiling.

d. **Model Explainability:** Integrate SHAP (SHapley Additive exPlanations) values for individual-level prediction explanations.

e. **Production Deployment:** Containerize the application using Docker, deploy to a cloud platform (AWS/GCP/Azure), and add CI/CD pipelines for automated retraining.

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
- **EDA & Statistics:** pandas, numpy, scipy, seaborn, matplotlib, statsmodels
- **Machine Learning:** scikit-learn (LinearRegression, DecisionTreeRegressor, RandomForestRegressor, GradientBoostingRegressor)
- **Deployment:** Streamlit, joblib

- **Language:** Python
- **EDA & Stats:** pandas, numpy, scipy, seaborn, matplotlib, statsmodels
- **ML:** scikit-learn (RandomForestRegressor)
- **Deployment:** Streamlit, joblib
