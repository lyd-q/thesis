# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import statsmodels.api as sm
base_path = Path(__file__).resolve().parent.parent
# %%
nih_by_msa = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_upload.csv")

# %%
# do regressions using the 1998 observations
#nih_regress = nih_by_msa[nih_by_msa['year'] == 1998]
nih_regress = nih_by_msa[nih_by_msa['year'] == 2003]
nih_regress = nih_regress.dropna(subset=['log_98_03'])
nih_regress = nih_regress[nih_regress['CBSA_level'] == 'Metropolitan Statistical Area']
# %%
# Look at distribution
nih_regress['log_98_03'].hist(bins=30, edgecolor='black')

#%%
# add a log total population
nih_regress['log_total_pop'] = np.log(nih_regress['total_pop'])
# %%
y = nih_regress['log_98_03']
x = nih_regress[['log_total_pop', 'income_per_cap', 'share_college', 'share_gradschool', 'indus_health_services', 'indus_educ_services', 'funding_log_percap_1']]

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary())

#%% 
# Do a regression based on growth rate from previous years
# For regression in previous years, check that funding obs are not missing
for lag in range(1, 6):
    nih_regress_lags = nih_regress.dropna(subset=['funding_dollars'+f"_{lag}"])
    print(len(nih_regress_lags))
    # 178 observations
y = nih_regress_lags['log_98_03']
x = nih_regress_lags[['funding_log_1', 'funding_log_2', 'funding_log_3', 'funding_log_4', 'funding_log_5', 'log_total_pop', 'income_per_cap', 'share_college', 'share_gradschool', 'indus_health_services', 'indus_educ_services']]
# x = nih_regress_lags[['funding_dollars_1', 'funding_dollars_2', 'funding_dollars_3', 'funding_dollars_4', 'funding_dollars_5']]
# x = nih_regress_lags[['funding_log_percap_1', 'funding_log_percap_2', 'funding_log_percap_3', 'funding_log_percap_4', 'funding_log_percap_5']]
# x = nih_regress_lags[['funding_dollars_percap_1', 'funding_dollars_percap_2', 'funding_dollars_percap_3', 'funding_dollars_percap_4', 'funding_dollars_percap_5']]
x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))

#%%
y = nih_regress_lags['log_98_03']
x = nih_regress_lags[['funding_log_1', 'log_total_pop', 'income_per_cap', 'share_college', 'indus_health_services', 'indus_educ_services']]
# x = nih_regress_lags[['funding_dollars_1', 'funding_dollars_2', 'funding_dollars_3', 'funding_dollars_4', 'funding_dollars_5']]
# x = nih_regress_lags[['funding_log_percap_1', 'funding_log_percap_2', 'funding_log_percap_3', 'funding_log_percap_4', 'funding_log_percap_5']]
# x = nih_regress_lags[['funding_dollars_percap_1', 'funding_dollars_percap_2', 'funding_dollars_percap_3', 'funding_dollars_percap_4', 'funding_dollars_percap_5']]
x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))

#%%
########## Now with funding mechanisms ###########################
y = nih_regress_lags['log_98_03']
x = nih_regress_lags['funding_log_percap_1']
#%%
# Look at subsets of the data
nih_reg = nih_regress_lags[(nih_regress_lags['log_98_03'] < 2.5)]
y = nih_reg['log_98_03']
x = nih_reg['funding_log_percap_1']
nih_reg['log_98_03'].plot.hist(bins=30, title="Log Growth 1998 to 2003, subset")
#%%
x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))


# nih_reg_sorted = nih_regress_lags.sort_values('funding_log_1')
nih_reg_sorted = nih_reg.sort_values('funding_log_percap_1')


plt.scatter(nih_reg_sorted['funding_log_percap_1'], nih_reg_sorted['log_98_03'], label="Data")

# Predict
X_sorted = sm.add_constant(nih_reg_sorted['funding_log_percap_1'])
y_pred = model.predict(X_sorted)

plt.plot(nih_reg_sorted['funding_log_percap_1'], y_pred, color='red', label="OLS fit")

plt.legend()
plt.xlabel("funding_log_percap_1")
plt.ylabel("log_98_03")
# plt.title("Log Growth and 1997 Funding, No outliers")
plt.title("Log Growth and 1997 Funding")
plt.show()
# %%
nih_reg['log_98_03'].plot.hist(bins=30, title="Log Growth 1998 to 2003")
# %%
nih_regress['log_98_03'].mean()
# %%
# Outliers
nih_outliers = nih_regress_lags[(nih_regress_lags['log_98_03'] > 2.5)]
nih_outliers["CBSA_title"].unique()


# %% ####################### Adjust variable ####################
x_var = 'indus_health_services'

# %% Check subset
nih_subset = nih_regress[['CBSA_title', 'funding_dollars', 'log_98_03', 'log_total_pop', 'indus_health_services']]
nih_subset.sort_values(by=['indus_health_services'], ascending=False)

# %% Full dataset
y = nih_regress_lags['log_98_03']
x = nih_regress_lags[x_var]
nih_reg = nih_regress_lags
nih_reg = nih_reg[nih_reg['indus_health_services'] < 667000]
#%% Excluding outliers
nih_reg = nih_regress_lags[(nih_regress_lags['log_98_03'] < 2.5)]
y = nih_reg['log_98_03']
x = nih_reg[x_var]
nih_reg = nih_reg[nih_reg['indus_health_services'] < 667000]
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
# %%
