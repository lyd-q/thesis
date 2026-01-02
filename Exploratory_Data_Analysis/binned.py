### Binned scatterplot -- use to represent all MSAs
# %% Import packages
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import statsmodels.api as sm
import sklearn
base_path = Path(__file__).resolve().parent.parent.parent

# %%
# Read in data
nih_all = pd.read_csv(base_path / "Data/NIH_v3/nih_use.csv")
nih = nih_all[nih_all['year'] == 1998].copy()
nih.to_csv(base_path / "Data/NIH_v3/cross_sec/nih_1998.csv", index=False)

# ['CBSA_code', 'CBSA_title', 'year', 'funding_nominal', 'funding',
#        'log_funding', 'total_pop', 'income_per_cap', 'share_college',
#        'share_gradschool', 'share_health_indus', 'share_educ_indus', 'log_pop',
#        'funding_pc', 'log_funding_pc', 'total_share_field', 'total_share_mech',
#        'funding_1997', 'funding_1998', 'funding_2003', 'funding_pc_1997',
#        'funding_pc_1998', 'funding_pc_2003', 'log_funding_1997',
#        'log_funding_1998', 'log_funding_2003', 'log_funding_pc_1997',
#        'log_funding_pc_1998', 'log_funding_pc_2003', 'log_98_03',
#        'percap_98_03', 'CBSA_title_abbrev', 'field_admin',
#        'field_basic_science', 'field_engineering', 'field_medicine',
#        'field_pop_behave_science', 'mech_research', 'mech_infrastructure',
#        'mech_training', 'mech_contracts', 'mech_other', 'rel_98_03']
#%%
xvar = 'mech_other'
xvar_name = 'Other research funding share'
xvar_save = xvar

nih_use = nih.copy()
nih_use = nih_use.dropna(subset=xvar)
# leave out Fairbanks, Alaska
nih_use = nih_use[nih_use['CBSA_title'] != 'Fairbanks, AK']
# Make bins of approx equal size
nih_use[f'bin_{xvar}'] = pd.qcut(nih_use[xvar], q=10, duplicates='drop')
# Keep only needed columns and drop missing values
nih_set = nih_use[[f'bin_{xvar}', f'{xvar}', 'log_98_03', 'percap_98_03', 'rel_98_03']]
# Group by income bin
grouped = nih_set.groupby(f'bin_{xvar}')

### Log ###
summary_log = grouped.agg(
    x=(xvar, 'median'),
    median=('log_98_03', 'median'),
    p25=('log_98_03', lambda s: s.quantile(0.25)),
    p75=('log_98_03', lambda s: s.quantile(0.75)),
    count=('log_98_03', 'size')
).sort_values('x')
# Asymmetric error bars: distance from median to 25th/75th percentiles
yerr_log = np.vstack([summary_log['median'] - summary_log['p25'],
                      summary_log['p75'] - summary_log['median']])
# OLS line
x = nih_set[xvar]
x = sm.add_constant(x)
y = nih_set['log_98_03']
model = sm.OLS(y, x).fit(cov_type='HC1')
y_hat = model.predict(x)
# Plot
plt.figure()
plt.errorbar(
    summary_log['x'],
    summary_log['median'],
    yerr=yerr_log,
    fmt='o',
    capsize=4
)
plt.plot(nih_set[xvar], y_hat, label='OLS (raw data)')
plt.xlabel(xvar_name)
plt.ylabel('Log Growth')
plt.title(f'Log growth by {xvar_name}, Binned\n(All observations)')
plt.savefig(base_path / f"Outputs/Binned_scatter/{xvar_save}_log.png", bbox_inches="tight")

### Level ###
summary_level = grouped.agg(
    x=(xvar, 'median'),
    median=('percap_98_03', 'median'),
    p25=('percap_98_03', lambda s: s.quantile(0.25)),
    p75=('percap_98_03', lambda s: s.quantile(0.75)),
    count=('percap_98_03', 'size')
).sort_values('x')
yerr_level = np.vstack([summary_level['median'] - summary_level['p25'],
                        summary_level['p75'] - summary_level['median']])
# OLS line
x = nih_set[xvar]
x = sm.add_constant(x)
y = nih_set['percap_98_03']
model = sm.OLS(y, x).fit(cov_type='HC1')
y_hat = model.predict(x)
# Plot
plt.figure()
plt.errorbar(
    summary_level['x'],
    summary_level['median'],
    yerr=yerr_level,
    fmt='o',
    capsize=4
)
plt.plot(nih_set[xvar], y_hat, label='OLS (raw data)')
plt.xlabel(xvar_name)
plt.ylabel('Dollars per capita change')
plt.title(f'Level Change by {xvar_name}, Binned\n(All observations)')
plt.savefig(base_path / f"Outputs/Binned_scatter/{xvar_save}_level.png", bbox_inches="tight")

### Relative change ###
summary_rel = grouped.agg(
    x=(xvar, 'median'),
    median=('rel_98_03', 'median'),
    p25=('rel_98_03', lambda s: s.quantile(0.25)),
    p75=('rel_98_03', lambda s: s.quantile(0.75)),
    count=('rel_98_03', 'size')
).sort_values('x')
yerr_rel = np.vstack([summary_rel['median'] - summary_rel['p25'],
                        summary_rel['p75'] - summary_rel['median']])
# OLS line
x = nih_set[xvar]
x = sm.add_constant(x)
y = nih_set['rel_98_03']
model = sm.OLS(y, x).fit(cov_type='HC1')
y_hat = model.predict(x)
# Plot
plt.figure()
plt.errorbar(
    summary_rel['x'],
    summary_rel['median'],
    yerr=yerr_rel,
    fmt='o',
    capsize=4
)
plt.plot(nih_set[xvar], y_hat, label='OLS (raw data)')
plt.xlabel(xvar_name)
plt.ylabel('Relative change')
plt.title(f'Relative Change by {xvar_name}, Binned\n(All observations)')
plt.savefig(base_path / f"Outputs/Binned_scatter/{xvar_save}_rel.png", bbox_inches="tight")

