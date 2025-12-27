# %% Import packages
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import statsmodels.api as sm
base_path = Path(__file__).resolve().parent.parent

####################### Preparing: 5 year buckets of average percap funding and average outcome var ############
# %% Read in data
nih_buckets = pd.read_csv(base_path / "Data/Cleaned/full/nih_buckets.csv")

# %% Get subsets
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")
nih = nih[nih['year'] == 1998]
nih = nih.dropna(subset=['percap_98_03'])
nih = nih.nlargest(50, 'funding_log_percap')

# merge with nih_buckets to pick just these
nih_buckets = nih.merge(nih_buckets, on='CBSA_code', how='left', suffixes=('', '_right'), indicator=True)
print(nih_buckets['_merge'].value_counts())
nih_buckets = nih_buckets[nih_buckets['_merge'] == 'both']

####################### Regressions: ~5 year buckets of percap funding change and average outcome var ############
# %% Pre-treatment
nih_buckets0 = nih_buckets[nih_buckets['bucket']==0]

# Output: MSAs' average establishment entry rate
y = nih_buckets0['estabs_entry_rate']
# Regressor: MSAs' average funding in dollars percap
x = nih_buckets0['funding_change_0']

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title='Pre-treatment'))
plt.scatter(nih_buckets0['funding_change_0'], nih_buckets0['estabs_entry_rate'], label="MSAs", alpha=0)
for _, row in nih_buckets0.iterrows():
    plt.annotate(
        row['CBSA_title_abbrev'],           
        (row['funding_change_0'], row['estabs_entry_rate']),  
        xytext=(5, 5),                      
        textcoords="offset points",
        fontsize=6,
        alpha=0.7,
        ha="center",
        va="center"
    )

# Predict
X_sorted = sm.add_constant(nih_buckets0['funding_change_0'])
y_pred = model.predict(X_sorted)

plt.plot(nih_buckets0['funding_change_0'], y_pred, color='red', label="OLS fit")
plt.xlabel('Change in Dollars per Capita')
plt.ylabel('Average Establishment Entry Rate')
plt.title('Pre-Treatment period: 1993-1997')
plt.show()

# %% Treatment
nih_buckets1 = nih_buckets[nih_buckets['bucket']==1]

# Output: MSAs' average establishment entry rate
y = nih_buckets1['estabs_entry_rate']
# Regressor: MSAs' average funding in dollars percap
x = nih_buckets1['funding_change_1']

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title='Pre-treatment'))
plt.scatter(nih_buckets1['funding_change_1'], nih_buckets1['estabs_entry_rate'], label="MSAs", alpha=0)
for _, row in nih_buckets1.iterrows():
    plt.annotate(
        row['CBSA_title_abbrev'],           
        (row['funding_change_1'], row['estabs_entry_rate']),  
        xytext=(5, 5),                      
        textcoords="offset points",
        fontsize=6,
        alpha=0.7,
        ha="center",
        va="center"
    )

# Predict
X_sorted = sm.add_constant(nih_buckets1['funding_change_1'])
y_pred = model.predict(X_sorted)

plt.plot(nih_buckets1['funding_change_1'], y_pred, color='red', label="OLS fit")
plt.xlabel('Change in Dollars per Capita')
plt.ylabel('Average Establishment Entry Rate')
plt.title('Treatment period: 1998-2003')
plt.show()

# %% Post-treatment
nih_buckets2 = nih_buckets[nih_buckets['bucket']==2]

# Output: MSAs' average establishment entry rate
y = nih_buckets2['estabs_entry_rate']
# Regressor: MSAs' average funding in dollars percap
x = nih_buckets2['funding_change_2']

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title='Pre-treatment'))
plt.scatter(nih_buckets2['funding_change_2'], nih_buckets2['estabs_entry_rate'], label="MSAs", alpha=0)
for _, row in nih_buckets2.iterrows():
    plt.annotate(
        row['CBSA_title_abbrev'],           
        (row['funding_change_2'], row['estabs_entry_rate']),  
        xytext=(5, 5),                      
        textcoords="offset points",
        fontsize=6,
        alpha=0.7,
        ha="center",
        va="center"
    )

# Predict
X_sorted = sm.add_constant(nih_buckets2['funding_change_2'])
y_pred = model.predict(X_sorted)

plt.plot(nih_buckets2['funding_change_2'], y_pred, color='red', label="OLS fit")
plt.xlabel('Change in Dollars per Capita')
plt.ylabel('Average Establishment Entry Rate')
plt.title('Post-Treatment period: 2004-2008')
plt.show()

# %% ####################### Plot average outcome var ############
print(np.mean(nih_buckets0['estabs_entry_rate']))
print(np.mean(nih_buckets1['estabs_entry_rate']))
print(np.mean(nih_buckets2['estabs_entry_rate']))