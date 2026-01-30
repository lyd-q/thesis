
#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
base_path = Path(__file__).resolve().parent.parent.parent

#%%
# CBSA_code, CBSA_title, and year are labels
# everything else, average over the 5-year period and MSA
# periods: 1994-98, 1999-2003, 2004-2008
# then run a panel regression with indicator on 1999-2003 periods

# Make bins
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_use_outcomes.csv")
nih.loc[nih['year'].between(1994, 1998), 'bin'] = 0
nih.loc[nih['year'].between(1999, 2003), 'bin'] = 1
nih.loc[nih['year'].between(2004, 2008), 'bin'] = 2
nih.loc[nih['year'].between(2009, 2013), 'bin'] = 3
nih.loc[nih['year'].between(2014, 2018), 'bin'] = 4
# %%
nih_bins = nih.drop(columns='year')
nih_bins = nih_bins[nih_bins['bin'].notna()]
group_cols = ['bin', 'CBSA_code', 'CBSA_title', 'CBSA_title_abbrev']
value_cols = nih.columns.difference(group_cols)
nih[value_cols] = nih[value_cols].apply(pd.to_numeric, errors='coerce')
nih.to_csv(base_path / "Data/NIH_v3/nih_bins_working.csv", index=False)
# %%
# creates binned version over averages
nih_bins = nih_bins.groupby(group_cols, as_index=False).mean()
nih_bins.to_csv(base_path / "Data/NIH_v3/nih_bins.csv", index=False)

# %%
# normalize outcomes into per capita 
nih_bins = nih_bins.drop(columns=['total_share_field', 'total_share_mech',
       'funding_1997', 'funding_1998', 'funding_2003', 'funding_pc_1997',
       'funding_pc_1998', 'funding_pc_2003', 'log_funding_1997',
       'log_funding_1998', 'log_funding_2003', 'log_funding_pc_1997',
       'log_funding_pc_1998', 'log_funding_pc_2003', 'log_98_03',
       'percap_98_03'])
# %%
nih_bins['firms_pc'] = nih_bins['firms'] / nih_bins['total_pop']
nih_bins['estabs_pc'] = nih_bins['estabs'] / nih_bins['total_pop']
nih_bins['emp_share'] = nih_bins['emp'] / nih_bins['total_pop']

# %%
# drop the two observations that don't have bin==2
CBSA_counts = nih_bins['CBSA_code'].value_counts()
to_drop = CBSA_counts[CBSA_counts == 2].index
nih_bins = nih_bins[~nih_bins['CBSA_code'].isin(to_drop)]
nih_bins.to_csv(base_path / "Data/NIH_v3/nih_bins.csv", index=False)

# now that data is done, run the regressions in stata


# %%
# add ln of values to do elasticity regression