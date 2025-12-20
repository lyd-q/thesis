# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import statsmodels.api as sm
base_path = Path(__file__).resolve().parent.parent

# %% ### Adjust variable ###
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")
x_var = 'indus_health_services'

# %% ### Full Dataset Version ###
y = nih['log_98_03']
x = nih[x_var]
nih_reg = nih
#%%
x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))


# nih_reg_sorted = nih_regress_lags.sort_values('funding_log_1')
nih_reg_sorted = nih_reg.sort_values(x_var)


plt.scatter(nih_reg_sorted[x_var], nih_reg_sorted['log_98_03'], label="Data")

# Predict
X_sorted = sm.add_constant(nih_reg_sorted[x_var])
y_pred = model.predict(X_sorted)

plt.plot(nih_reg_sorted[x_var], y_pred, color='red', label="OLS fit")

plt.legend()
plt.xlabel(x_var)
plt.ylabel("log_98_03")
#plt.title("Log Growth and Education Industry Size, Subset")
plt.title("Log Growth and Workers in Health Industry, All observations")
plt.show()

# %% ### Subset ###
nih_subset = nih[['CBSA_title', 'funding_dollars', 'log_98_03', 'log_total_pop', 'indus_health_services']]
nih_subset.sort_values(by=['indus_health_services'], ascending=False)
#%% Excluding outliers
nih_reg = nih[(nih['log_98_03'] < 2.5)]
y = nih_reg['log_98_03']
x = nih_reg[x_var]
nih_reg = nih_reg[nih_reg['indus_health_services'] < 667000]