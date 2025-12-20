#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%%
base_path = "/Users/lydia/Desktop/Thesis"
nih_raw = pd.read_stata(f"{base_path}/Data/nih_raw.dta")
nih_raw.head()

# %%
print(nih_raw['year'].value_counts())

nih_raw.to_csv(f"{base_path}/Data/Python/nih_raw.csv")

#%%
# --- imports ---
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

# --- load data from Stata ---
# convert_categoricals=False keeps string labels (useful for C() dummies)
nih_cbsa = pd.read_stata("/Users/lydia/Desktop/Thesis/Data/nih_msa_collapsed_adjusted.dta")
nih_cbsa = nih_cbsa[nih_cbsa["year"] <= 2003]
nih_cbsa = nih_cbsa[nih_cbsa["year"] >= 1997]

# optional: make sure key columns are present / coerced
for col in ['year', 'CBSA_code', 'log_FUNDING']:
    if col not in nih_cbsa.columns:
        raise ValueError(f"Column '{col}' not found. Available: {list(nih_cbsa.columns)}")

# coerce year to int (or at least numeric)
nih_cbsa['year'] = pd.to_numeric(nih_cbsa['year'], errors="coerce").astype(float)

# sort to ensure proper lagging within each metro
nih_cbsa = nih_cbsa.sort_values(['CBSA_code', 'year']).reset_index(drop=True)

for i in range(1, 6):
    nih_cbsa[f"log_FUNDING_lag_{i}"] = (
        nih_cbsa.groupby("CBSA_code")["log_FUNDING"].shift(i)
    )

lag_cols = [f"log_FUNDING_lag_{i}" for i in range(1, 6)]

# keep rows with full history and clean dtypes
model_nih_cbsa = nih_cbsa.dropna(subset=lag_cols + ["log_FUNDING", "CBSA_code", "year"]).copy()
model_nih_cbsa[lag_cols] = model_nih_cbsa[lag_cols].astype(float)
model_nih_cbsa["year"] = model_nih_cbsa["year"].astype(int)

formula = "log_FUNDING ~ " + " + ".join(lag_cols)

# fit OLS with CBSA-clustered SEs
res = smf.ols(formula=formula, data=model_nih_cbsa).fit(
    cov_type="cluster", cov_kwds={"groups": model_nih_cbsa["CBSA_code"]}
)

print(res.summary())

#%%
t1 = res.summary().tables[1]
keep = t1.index.str.contains(r'Intercept|log_FUNDING_lag_|C\(year\)')
t1_filtered = t1[keep]

# Show lag coefficients first, then year effects
order = sorted(t1_filtered.index, key=lambda x: (not x.startswith('log_FUNDING_lag_'), x))
t1_filtered = t1_filtered.loc[order]

print(t1_filtered)

