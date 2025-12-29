# %% Import packages
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import statsmodels.api as sm
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
#        'mech_training', 'mech_contracts', 'mech_other']
#%%
xvar = 'mech_other'
xvar_name = 'Other Research funding mechanism'
xvar_save = xvar
nih_use = nih.copy()
# Make bins
nih_use[f'bin_{xvar}'] = pd.cut(nih_use[xvar], 10)

# Keep only needed columns and drop missing values
nih_set = nih_use[[f'bin_{xvar}', f'{xvar}', 'log_98_03', 'percap_98_03']].dropna()
# Group by income bin
grouped = nih_set.groupby(f'bin_{xvar}')

### Log ###
# Compute intervals
summary_log = grouped['log_98_03'].agg(['count', 'mean', 'std'])
summary_log['se'] = summary_log['std'] / np.sqrt(summary_log['count'])
summary_log['x'] = grouped[f'{xvar}'].mean()
summary = summary_log.sort_values('x')
# Plot
plt.figure()
plt.errorbar(
    summary_log['x'],
    summary_log['mean'],
    yerr=summary_log['se'],
    fmt='o',
    capsize=4
)
plt.xlabel(xvar_name)
plt.ylabel('Log Growth')
plt.title(f'Log growth by {xvar_name}, Binned\n(All observations)')
plt.savefig(base_path / f"Outputs/Binned_scatter/{xvar_save}_log.png", bbox_inches="tight")

### Level ###
summary_level = grouped['percap_98_03'].agg(['count', 'mean', 'std'])
summary_level['se'] = summary_level['std'] / np.sqrt(summary_level['count'])
summary_level['x'] = grouped[f'{xvar}'].mean()
summary_level = summary_level.sort_values('x')
# Plot
plt.figure()
plt.errorbar(
    summary_level['x'],
    summary_level['mean'],
    yerr=summary_level['se'],
    fmt='o',
    capsize=4
)
plt.xlabel(xvar_name)
plt.ylabel('Dollars per capita change')
plt.title(f'Level Change by {xvar_name}, Binned\n(All observations)')
plt.savefig(base_path / f"Outputs/Binned_scatter/{xvar_save}_level.png", bbox_inches="tight")



# %%
