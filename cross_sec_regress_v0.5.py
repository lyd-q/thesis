# %%
import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.api as sm


base_path = Path(__file__).resolve().parent.parent
nih_census = pd.read_csv(base_path / "Data/Cleaned/nih_census.csv")

#%%
nih_census['log_funding_dollars'] = np.log(nih_census['funding_dollars']+1)
FUNDING = "log_funding_dollars"
for lag in range(1, 6):
    nih_census[FUNDING+f"_{lag}"] = nih_census.groupby("CBSA_code")[FUNDING].shift(lag)

#%%
nih_03 = nih_census.loc[nih_census["year"] == 2003].copy()
X_cols = [f"{FUNDING}_1", "pct_bachelors_higher", "pct_employed", "median_household_income", "population"]
X = sm.add_constant(nih_03[X_cols])
y = nih_03[FUNDING]
model_levels = sm.OLS(y, X, missing="drop").fit(cov_type="HC1")
print(model_levels.summary(title="Levels: explain 2003 funding"))


#%%
# Subset to 2003
nih_03 = nih_census.loc[nih_census["year"] == 1998].copy()

# Dependent variable
y = nih_03["log_funding_percap"]

# Independent variables: the 5 lags
X_cols = [f"log_funding_percap_{i}" for i in range(1, 6)]
X = sm.add_constant(nih_03[X_cols])

# Fit OLS with robust SEs
model = sm.OLS(y, X, missing='drop').fit(cov_type='HC1')

print(model.summary(title="AR(5) model for log(funding per capita) in 1998"))


#%%
X_cols = [FUNDING+f"_{i}" for i in range(1, 6)]
nih_yr = nih_census[(nih_census["year"] >= 1998 & nih_census["year"] <= 2003)].copy()
X = sm.add_constant(nih_yr[X_cols])
y = nih_yr[FUNDING]

model = sm.OLS(y, X, missing='drop').fit(cov_type='HC1')
print(model.summary(title="Predicting year 2002"))

#%%
X_cols = [FUNDING+f"_{i}" for i in range(1, 5)] + ["pct_bachelors_higher"] + ["pct_employed"] + ["population"] + ["median_household_income"]
X = sm.add_constant(nih_census[X_cols])
y = nih_census[FUNDING]

model = sm.OLS(y, X, missing='drop').fit(cov_type='HC1')
print(model.summary())

# %%
