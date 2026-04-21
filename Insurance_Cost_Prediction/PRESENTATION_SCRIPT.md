# Insurance Cost Prediction — Business Presentation Script

**Audience:** Business Stakeholders  
**Duration:** ~30–35 minutes  
**Tools Needed:** Laptop, Jupyter Notebook (`insurance.ipynb`), Streamlit apps (`app.py`, `app1.py`), this script

---

## PRE-PRESENTATION SETUP CHECKLIST
*(Do these 10–15 minutes before the presentation starts)*

- [ ] Open a terminal and run: `python -m streamlit run app.py` — keep this browser tab ready
- [ ] Open a second terminal and run: `python -m streamlit run app1.py --server.port 8502` — keep the dashboard tab ready
- [ ] Open `insurance.ipynb` in Jupyter or VS Code — scroll to the top, ready to walk through
- [ ] Set browser zoom to ~110% so charts and text are clearly visible on the projector
- [ ] Have this script open on your phone or a secondary device for reference
- [ ] Close all unrelated tabs and applications

---

## SECTION 1 — OPENING & PROBLEM FRAMING
**[~3 minutes]**

**SAY:**
> "Good [morning/afternoon]. Today I'm going to walk you through an end-to-end data science project focused on insurance premium pricing.
>
> The central business problem is this: how do we determine what a customer should pay for health insurance in a way that is accurate, fair, and fast?
>
> Traditionally, this relies on manual underwriting — which is slow, inconsistent, and difficult to scale. Our goal was to replace that with a data-driven model.
>
> I'll cover three things today:
> 1. What the data tells us — the insights from our analysis
> 2. Statistical proof that those insights are real — not just patterns in this sample
> 3. A live demonstration of the deployed prediction tool "

**DO:** Show the first cell of `insurance.ipynb` — the dataset preview showing the 11 columns and sample rows.

**SAY:**
> "We worked with 986 customer records. Each record contains demographic data — age, height, weight — and health history flags like diabetes, blood pressure problems, transplants, chronic diseases, and more. The target variable is the insurance premium price in rupees."

---

## SECTION 2 — EXPLORATORY DATA ANALYSIS (EDA)
**[~10 minutes]**

### 2a. Premium Price Distribution
**DO:** Scroll to the `PremiumPrice` distribution plots (histogram + violin plot + KDE) in the notebook.

**SAY:**
> "The first thing we examined was how premium prices are distributed. The distribution is right-skewed and multi-modal — meaning prices cluster around a few distinct tiers rather than following a smooth bell curve. This is a clear signal that there are specific risk profiles driving these pricing bands, not a single continuous scale."
>
> "To work with this mathematically, we applied a log transformation to normalize the distribution. This is important for accurate modelling."

---

### 2b. Age Distribution
**DO:** Point to the Age histogram.

**SAY:**
> "Our customer base is well-distributed across all age groups from 18 to 66. That's good news — it means the model sees enough examples at every age to learn reliably, not just for the most common age brackets."

---

### 2c. BMI
**DO:** Show the BMI distribution plot.

**SAY:**
> "BMI — Body Mass Index — was an engineered feature we derived from height and weight. The distribution is slightly skewed upward, with a small but meaningful tail of high-BMI individuals. These are typically the higher-risk, higher-cost cases."

---

### 2d. Correlation Heatmap — The Key Slide
**DO:** Navigate to the correlation heatmap in the notebook.

**SAY:**
> "Now this is where things get interesting. This correlation heatmap shows how strongly each variable relates to premium price.
>
> Three key takeaways:
>
> **First** — Age has the highest correlation with premium. All else equal, older customers cost more to insure. This is expected and validates our data.
>
> **Second** — Number of major surgeries is the next strongest predictor. Surgical history reflects compounding health risk.
>
> **Third** — Height, weight, and BMI are highly correlated with each other — which makes sense, because BMI is derived from height and weight. To avoid feeding redundant information into the model, we will be focusing on only BMI."

---

### 2e. Outlier Analysis
**DO:** Show the box plots for PremiumPrice and BMI.

**SAY:**
> "We also checked for outliers. There are a few extreme values in both premium price and BMI. The important decision we made here was NOT to remove them. These aren't data errors — they represent genuinely high-risk individuals. Removing them would make our model blind to exactly the customers who matter most for risk pricing.
>
> Instead, we handled them through the log transformation, which compresses the extreme values without discarding them."

---

## SECTION 3 — HYPOTHESIS TESTING
**[~7 minutes]**

**SAY:**
> "EDA gives us patterns. But patterns in a sample don't automatically tell us what's true for the full population. That's where hypothesis testing comes in — it lets us formally validate whether what we're seeing is statistically real."

---

### 3a. Do Health Conditions Affect Premiums? — Welch's t-test
**DO:** Navigate to the hypothesis testing section of the notebook. Show the t-test results table.

**SAY:**
> "For each binary health condition — diabetes, blood pressure problems, chronic diseases, transplants, allergies, and family cancer history — we ran a Welch's t-test. The question: do individuals WITH the condition pay significantly different premiums than those WITHOUT?
>
> The result: all six conditions are statistically significant at the 95% confidence level. Every one of these health flags genuinely impacts what a customer pays.
>
> This is not just noise — these are real, measurable cost drivers."

---

### 3b. Does Surgery Count Affect Premiums? — One-Way ANOVA
**DO:** Show the ANOVA result for NumberOfMajorSurgeries.

**SAY:**
> "For surgery count — which is a category with four levels: 0, 1, 2, or 3 surgeries — we used ANOVA, which compares multiple groups at once.
>
> The result: p-value below 0.05. Premiums differ significantly across surgery groups. Each additional surgery corresponds to a real increase in insurance cost."

---

### 3c. Are Health Conditions Linked to Each Other? — Chi-Square Tests
**DO:** Show the Chi-Square test results.

**SAY:**
> "We also tested whether certain health conditions tend to appear together. This matters for pricing, because co-occurring conditions compound risk.
>
> Key findings:
> - Diabetes and blood pressure problems are statistically associated — they frequently co-occur.
> - Chronic diseases and transplant history are linked.
> - Chronic diseases and higher surgery counts are linked — patients with chronic conditions tend to undergo more procedures.
>
> Bottom line: risk is not isolated. It accumulates and compounds. Our model needs to, and does, account for this."

---

## SECTION 4 — MODELLING RESULTS
**[~5 minutes]**

**SAY:**
> "With a clear picture of the data and validated insights, we trained four regression models to predict premium prices."

**DO:** Show the model comparison table from the notebook (or the README).

**SAY:**
> "Here's how they compare:

| Model | R² Score | Description |
|---|---|---|
| Linear Regression | 0.717 | Baseline — explains 72% of variance |
| Decision Tree | 0.854 | Captures non-linear patterns |
| **Random Forest** | **0.897** | **Best performer — 90% accuracy** |
| Gradient Boosting | 0.887 | Close second |

> Random Forest performed best — it explains approximately 90% of the variance in insurance premiums. We validated this through 5-fold cross-validation, which confirmed the result wasn't a lucky split — it's consistent across different subsets of the data."

---

### 4a. Feature Importance
**DO:** Show the Permutation Importance chart.

**SAY:**
> "For a business Perhaps the most useful output can be : which factors actually drive the model's predictions?
>
> The ranking is:
> 1. **Age** — by far the dominant factor
> 2. **Transplant history** — highest medical severity signal
> 3. **Chronic diseases** — second highest severity signal
> 4. **BMI** — meaningful, especially at extreme values
> 5. **Number of major surgeries** — cumulative health burden
>
> Notably, diabetes, blood pressure, and allergies — while statistically significant — have low standalone importance. Their effects are absorbed by the more severe overlapping conditions.
>
> This tells us two things: first, our top pricing levers are age and severe medical history. Second, we should be cautious about aggressively penalizing customers for isolated, manageable conditions like controlled blood pressure."

---

## SECTION 5 — LIVE DEMO: PREDICTION APP
**[~5 minutes]**

**DO:** Switch to the browser tab with `app.py` running on `localhost:8501`

**SAY:**
> "Let me now show you the deployed tool. This is a web application — built in Streamlit — that uses our trained Random Forest model to predict premium prices in real time."

---

**DEMO 1 — Low-Risk Profile**

**DO:** Enter the following values in the form:
- Age: **28**, Height: **170**, Weight: **65**, Surgeries: **0**
- All health conditions: **No**
- Click **Predict Premium**

**SAY:**
> "Here's a young, healthy individual with no health flags. The model predicts a relatively low premium. Notice we also get a BMI calculation. And since there are no risk factors, we get a clean green confirmation."

---

**DEMO 2 — High-Risk Profile**

**DO:** Enter the following values:
- Age: **58**, Height: **165**, Weight: **95**, Surgeries: **2**
- Diabetes: **Yes**, Blood Pressure: **Yes**, Chronic Disease: **Yes**, Transplants: **Yes**
- Click **Predict Premium**

**SAY:**
> "Now a high-risk profile — older, overweight, multiple health conditions, two major surgeries, and a transplant history. Watch what happens to the premium.
>
> The model instantly produces a significantly higher estimate — reflecting the compounding risk we confirmed statistically.
>
> But notice something powerful here: it doesn't just give a number. It surfaces the specific risk factors identified — and provides tailored health recommendations for each one.
>
> This is where the tool crosses from pricing into prevention. We're not just telling customers they cost more to insure — we're showing them what they can do about it. That's a meaningful shift in how we engage with customers."

---

## SECTION 6 — LIVE DEMO: ANALYTICS DASHBOARD
**[~3 minutes]**

**DO:** Switch to the browser tab with `app1.py` running on `localhost:8502`

**SAY:**
> "The second application is an analytics dashboard — designed for internal business users. It lets you explore the underlying data interactively."

**DO:** Use the sidebar sliders to filter by age range and BMI range. Show the four pages briefly.

**SAY:**
> "You can filter by age range and BMI range to drill into specific customer segments. The four sections are:
> - **Summary Statistics** — overview of the portfolio
> - **Premium Pricing Analysis** — how premiums vary by age group and health profile
> - **Risk Factors Analysis** — the impact of specific conditions on cost
> - **Demographic Insights** — BMI vs. premium patterns with condition overlays
>
> This is a tool for your analysts and underwriters — a live view into what's driving costs across the portfolio."

---

## SECTION 7 — BUSINESS RECOMMENDATIONS
**[~5 minutes]**

**SAY:**
> "Let me now translate everything we've seen into specific business actions."

---

**Recommendation 1 — Refine Age-Based Pricing Tiers**
> "Age is the dominant cost driver. If your current pricing bands are broad — for example, grouping everyone from 40 to 55 together — you're systematically underpricing some customers and overpricing others. This model supports more granular age-tier pricing with statistical backing."

---

**Recommendation 2 — Apply Risk Loadings for Severe Conditions**
> "Transplant history and chronic diseases drive disproportionate cost increases. These customers should be identified early for specialized plans or risk loadings — and ideally, proactive care-management programs to reduce long-term claim frequency."

---

**Recommendation 3 — Use BMI as a Prevention Lever, Not Just a Pricing Input**
> "BMI is modifiable. Rather than simply charging more for high-BMI customers, consider offering premium discounts for documented BMI improvement — wellness programs, nutrition incentives, gym partnerships. This shifts cost management from reactive pricing to proactive prevention."

---

**Recommendation 4 — Avoid Over-Penalizing Minor Conditions**
> "Diabetes, blood pressure, and allergies — while real health signals — don't independently drive significant cost increases once severe conditions are accounted for. Aggressively penalizing customers for well-managed, isolated conditions increases churn and damages trust without meaningful risk benefit."

---

**Recommendation 5 — Move to Holistic Risk-Profile Pricing**
> "The model confirms risk compounds — it's not additive. A customer who is 55, has a transplant, and has chronic disease is not priced correctly by summing three separate loadings. A model-driven approach captures the interaction naturally. This is a direct argument for integrating ML pricing into your underwriting workflow."

---

**Recommendation 6 — Transparent, Explainable Pricing**
> "The feature importance rankings align with clinical and actuarial logic. That's not accidental — it's a sign the model is trustworthy and defensible. When regulators, auditors, or customers ask why a premium is what it is, you can answer that question clearly."

---

## SECTION 8 — CLOSING
**[~2 minutes]**

**SAY:**
> "To summarize what we've built and proven:
>
> - We analyzed 986 customer records across 10 health and demographic features
> - EDA revealed that age, transplant history, chronic disease, and BMI are the primary pricing drivers
> - Hypothesis testing confirmed these findings are statistically significant — not sampling artifacts
> - Our Random Forest model explains **90% of premium variance** and is validated through cross-validation
> - The deployed application provides real-time predictions, risk factor identification, and preventive health recommendations
> - The analytics dashboard gives business and underwriting teams live data exploration capability
>
> The next steps I'd recommend: integrate this model into the underwriting pipeline for new policy quotes, pilot the wellness incentive program for high-BMI customers, and explore SHAP values for individual-level pricing explanations.
>
> I'm happy to take questions."

---

## Q&A PREPARATION — ANTICIPATED QUESTIONS

**Q: How accurate is the model really?**
> "It explains 90% of variance in log-transformed premiums. On actual rupee values, the average prediction error — MAE — is very low. We also validated stability through bootstrapped prediction intervals, which were narrow for most customers and appropriately wider for complex risk profiles."

**Q: Can the model price customers it has never seen before?**
> "Yes. The model generalizes well — confirmed by cross-validation on held-out data and bootstrap testing. It was never trained on those specific individuals."

**Q: What happens if a customer lies about their health history?**
> "The model can only work with inputs provided. However, the output is fully auditable — if someone submits no health conditions but later files claims that reveal otherwise, the premium can be reassessed. Pairing this with claim history data in future versions would improve robustness."

**Q: Why not use a more complex model like XGBoost or a neural network?**
> "We tested multiple approaches. Random Forest performed best on this dataset size without additional complexity. XGBoost or neural networks would be natural next steps as we gather more data, but they offer diminishing returns at ~1,000 records and introduce interpretability challenges."

**Q: Is this model biased?**
> "We examined feature importance carefully. The model's top drivers — age and medical history — are clinically and actuarially justified. It does not include demographic proxies like location or income. The feature importance ranking is transparent and auditable."

**Q: How do we deploy this at scale?**
> "The current application is a prototype for demonstration. For production: containerize with Docker, deploy to a cloud platform (AWS, Azure, GCP), add an API layer for integration with existing underwriting systems, and establish a retraining pipeline when new data becomes available."

---

## TIMING GUIDE

| Section | Duration |
|---|---|
| Setup (pre-presentation) | 10–15 min |
| 1. Opening & Framing | 3 min |
| 2. EDA | 10 min |
| 3. Hypothesis Testing | 7 min |
| 4. Modelling Results | 5 min |
| 5. Live Demo — Prediction App | 5 min |
| 6. Live Demo — Dashboard | 3 min |
| 7. Business Recommendations | 5 min |
| 8. Closing | 2 min |
| Q&A | 10 min |
| **Total** | **~50 min** |

---

## QUICK REFERENCE — KEY NUMBERS TO MEMORIZE

- Dataset: **986 customers, 10 features**
- All **6 health conditions** statistically significant (p < 0.05, Welch's t-test)
- Surgery count: **ANOVA confirmed** significant (p < 0.05)
- Best model: **Random Forest — R² = 0.897, MAE = 0.055**
- Top features: **Age > Transplants > Chronic Disease > BMI > Surgeries**
- App type: **Streamlit, real-time prediction, rupee output**
- Log-transform used: predict in log space, convert back with `expm1`
