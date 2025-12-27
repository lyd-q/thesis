# %%
import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.api as sm
base_path = Path(__file__).resolve().parent.parent

# %%
nih_counties = pd.read_csv(base_path / "Data/Census/census_1990/nih_counties1990.csv")

# log population
nih_counties['log_total_pop'] = np.log(nih_counties['total_pop'])
# share college
nih_counties['share_college'] = nih_counties['bachelors_deg'] / nih_counties['total_pop']
# share grad school
nih_counties['share_gradschool'] = nih_counties['graduate_deg'] / nih_counties['total_pop']

# NIH funding variables
nih_counties = nih_counties.dropna(subset=['funding_dollars']) 
# can drop these now that census values have been aggregated
nih_counties = nih_counties[nih_counties['funding_dollars'] != 0]
nih_counties['funding_dollars_percap'] = nih_counties['funding_dollars'] / nih_counties['total_pop'] 
nih_counties['funding_log'] = np.log(nih_counties['funding_dollars'])
nih_counties['funding_log_percap'] = np.log(nih_counties['funding_dollars_percap'])

nih_counties['county_name'].nunique()
# 705 observations
nih_counties = nih_counties.drop(columns=['_merge'])

# %%
for lag in range(1, 6):
    nih_counties['funding_dollars'+f"_{lag}"] = nih_counties.groupby('county_code')['funding_dollars'].shift(lag)
    nih_counties['funding_dollars_percap'+f"_{lag}"] = nih_counties.groupby('county_code')['funding_dollars_percap'].shift(lag)
    nih_counties['funding_log'+f"_{lag}"] = nih_counties.groupby('county_code')['funding_log'].shift(lag)
    nih_counties['funding_log_percap'+f"_{lag}"] = nih_counties.groupby('county_code')['funding_log_percap'].shift(lag)

# %%
nih_counties = nih_counties[(nih_counties['year'] != 2003) | nih_counties['funding_dollars_5'].notna()].copy()
# 204 observations for 2003

nih_counties.loc[nih_counties['year'] == 2003, 'log_98_03'] = (nih_counties['funding_log'] - nih_counties['funding_log_5'])
nih_counties.loc[nih_counties['year'] == 2003, 'log_percap_98_03'] = (nih_counties['funding_log_percap'] - nih_counties['funding_log_percap_5'])

nih_counties['log_98_03'] = nih_counties.groupby('county_code')['log_98_03'].transform('first')
# check that percap growth rate is the same
nih_counties['log_percap_98_03'] = nih_counties.groupby('county_code')['log_percap_98_03'].transform('first')
nih_counties.to_csv(base_path / "Data/Census/census_1990/nih_counties_regress.csv", index=False)
# %%
nih_regress = nih_counties[nih_counties['year'] == 1998]
nih_regress = nih_regress.dropna(subset=['log_98_03', 'log_percap_98_03'])
nih_regress['log_98_03'].hist(bins=30, edgecolor='black')

for lag in range(1, 6):
    nih_regress_lags = nih_regress.dropna(subset=['funding_dollars'+f"_{lag}"])
    print(len(nih_regress_lags))
    # 383 observations
y = nih_regress_lags['log_98_03']
x = nih_regress_lags[['funding_log_1', 'funding_log_2', 'funding_log_3', 'funding_log_4', 'funding_log_5', 'income_per_cap', 'log_total_pop', 'share_college', 'share_gradschool', 'indus_health_services', 'indus_educ_services']]

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by County"))
# %%
nih_regress = nih_counties[nih_counties['year'] == 1998]
nih_regress = nih_regress.dropna(subset=['log_98_03', 'log_percap_98_03'])
nih_regress_lags = nih_regress.dropna(subset=['funding_dollars_1'])
y = nih_regress_lags['log_98_03']
x = nih_regress_lags[['funding_log_1','income_per_cap', 'log_total_pop', 'share_college', 'indus_health_services', 'indus_educ_services']]
x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by County"))
# %%
