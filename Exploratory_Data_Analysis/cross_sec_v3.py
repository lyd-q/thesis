# %% Import packages
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import statsmodels.api as sm
base_path = Path(__file__).resolve().parent.parent.parent

# %% ################## Get File of Only 1998-2003 ###################
nih_all = pd.read_csv(base_path / "Data/NIH_v3/nih_all.csv")
nih = nih_all[nih_all['year'] == 1998].copy()
nih.to_csv(base_path / "Data/NIH_v3/cross_sec/nih_use.csv", index=False)

# %%
################## Mean Reversion - Log ###################
nih_set = nih.copy()
# nih_set = nih.nsmallest(50, 'funding_pc_1998')
# nih_set = nih.nsmallest(50, 'total_pop')
y = nih_set['log_funding_2003']
x = nih_set['log_funding_1998']

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title='Mean Reversion'))

plt.scatter(nih_set['log_funding_1998'], nih_set['log_funding_2003'], label="MSAs", alpha=0)
for _, row in nih_set.iterrows():
    plt.annotate(
        row['CBSA_title_abbrev'],           
        (row['log_funding_1998'], row['log_funding_2003']),  
        xytext=(5, 5),                      
        textcoords="offset points",
        fontsize=6,
        alpha=0.7,
        ha="center",
        va="center"
    )
X_sorted = sm.add_constant(nih_set['log_funding_1998'])
y_pred = model.predict(X_sorted)

plt.plot(nih_set['log_funding_1998'], y_pred, color='red', label="OLS fit")

plt.legend()
plt.xlabel('log_funding_1998')
plt.ylabel("log_funding_2003")
plt.title("Mean Reversion")
plt.savefig(base_path / f"Outputs/Explore_Reg_Full/mean_reversion/mean_reversion_log.png", bbox_inches="tight")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/mean_reversion/mean_rev_log_top100pop.png", bbox_inches="tight")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/mean_reversion/mean_rev_log_bottom50funding.png", bbox_inches="tight")
plt.show()

# %%
################## Mean Reversion - Levels ###################
# nih_set = nih.copy()
nih_set = nih.nlargest(100, 'funding_pc_1998')
# nih_set = nih.nlargest(100, 'total_pop')
y = nih_set['funding_pc_2003']
x = nih_set['funding_pc_1998']

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title='Mean Reversion'))

plt.scatter(nih_set['funding_pc_1998'], nih_set['funding_pc_2003'], label="MSAs", alpha=0)
for _, row in nih_set.iterrows():
    plt.annotate(
        row['CBSA_title_abbrev'],           
        (row['funding_pc_1998'], row['funding_pc_2003']),  
        xytext=(5, 5),                      
        textcoords="offset points",
        fontsize=6,
        alpha=0.7,
        ha="center",
        va="center"
    )
X_sorted = sm.add_constant(nih_set['funding_pc_1998'])
y_pred = model.predict(X_sorted)

plt.plot(nih_set['funding_pc_1998'], y_pred, color='red', label="OLS fit")

plt.legend()
plt.xlabel('funding_pc_1998')
plt.ylabel("funding_pc_2003")
plt.title("Mean Reversion - Levels")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Full/mean_reversion/mean_reversion_levels.png", bbox_inches="tight")
plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/mean_reversion/mean_rev_levels_top100funding.png", bbox_inches="tight")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/mean_reversion/mean_rev_levels_bottom100pop.png", bbox_inches="tight")
plt.show()

# ['CBSA_code', 'CBSA_title', 'year', 'funding_nominal', 'funding',
#        'log_funding', 'total_pop', 'total_income_imputed', 'income_per_cap',
#        'share_college', 'share_gradschool', 'share_health_indus',
#        'share_educ_indus', 'log_pop', 'funding_pc', 'log_funding_pc',
#        'ADMINISTRATION', 'ANATOMY/CELL BIOLOGY', 'ANESTHESIOLOGY',
#        'BIOCHEMISTRY', 'BIOLOGY', 'BIOMEDICAL ENGINEERING', 'BIOPHYSICS',
#        'BIOSTATISTICS & OTHER MATH SCI', 'CHEMISTRY', 'DENTISTRY',
#        'DERMATOLOGY', 'EMERGENCY MEDICINE', 'ENGINEERING (ALL TYPES)',
#        'FAMILY MEDICINE', 'GENETICS', 'INTERNAL MEDICINE/MEDICINE',
#        'MICROBIOLOGY/IMMUN/VIROLOGY', 'NEUROLOGY', 'NEUROSCIENCES',
#        'NEUROSURGERY', 'NUTRITION', 'OBSTETRICS & GYNECOLOGY', 'OPHTHALMOLOGY',
#        'ORTHOPEDICS', 'OTHER BASIC SCIENCES', 'OTHER CLINICAL SCIENCES',
#        'OTHER HEALTH PROFESSIONS', 'OTOLARYNGOLOGY', 'PATHOLOGY', 'PEDIATRICS',
#        'PHARMACOLOGY', 'PHYSICAL MEDICINE & REHAB', 'PHYSICS', 'PHYSIOLOGY',
#        'PLASTIC SURGERY', 'PSYCHIATRY', 'PSYCHOLOGY',
#        'PUBLIC HEALTH & PREV MEDICINE', 'RADIATION-DIAGNOSTIC/ONCOLOGY',
#        'SOCIAL SCIENCES', 'SURGERY', 'UROLOGY', 'VETERINARY SCIENCES',
#        'ZOOLOGY', 'total_share_field', 'Construction',
#        'Other Research-Related', 'R&D Contracts', 'RPGs - Non SBIR/STTR',
#        'RPGs - SBIR/STTR', 'Research Centers', 'Research Grants',
#        'Training - Individual', 'Training - Institutional', 'total_share_mech',
#        'funding_1997', 'funding_1998', 'funding_2003', 'funding_pc_1997',
#        'funding_pc_1998', 'funding_pc_2003', 'log_funding_1997',
#        'log_funding_1998', 'log_funding_2003', 'log_funding_pc_1997',
#        'log_funding_pc_1998', 'log_funding_pc_2003', 'log_98_03',
#        'percap_98_03', 'CBSA_title_abbrev']
# %% 
################### Regressions - log growth ###################
#### Adjust variable ###
x_var = 'PUBLIC HEALTH & PREV MEDICINE'

# nih_set = nih.copy()
# nih_set = nih.nlargest(100, 'funding_pc_1998')
# nih_set = nih.nlargest(50, 'total_pop')
# nih_set = nih.nsmallest(100, 'funding_pc_1998')
nih_set = nih.nsmallest(50, 'total_pop')

y = nih_set['log_98_03']
x = nih_set[x_var]
x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))
plt.scatter(nih_set[x_var], nih_set['log_98_03'], label="MSAs", alpha=0)
# nih["CBSA_title_abbrev_largeMSA"] = (
#     nih["CBSA_title_abbrev_largeMSA"]
#     .fillna("")
# )
for _, row in nih_set.iterrows():
    plt.annotate(
        row['CBSA_title_abbrev'],           
        (row[x_var], row['log_98_03']),  
        xytext=(5, 5),                      
        textcoords="offset points",
        fontsize=6,
        alpha=0.7,
        ha="center",
        va="center"
    )
X_sorted = sm.add_constant(nih_set[x_var])
y_pred = model.predict(X_sorted)

plt.plot(nih_set[x_var], y_pred, color='red', label="OLS fit")
plt.legend()
plt.xlabel(x_var)
plt.ylabel("log_98_03")
x_var = 'public_health'
plt.title(f"Log Growth and {x_var}")

# plt.savefig(base_path / f"Outputs/Explore_Reg_Full/{x_var}_log_full.png", bbox_inches="tight")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/{x_var}_log_top100funding.png", bbox_inches="tight")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/{x_var}_log_top50pop.png", bbox_inches="tight")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/{x_var}_log_bottom100funding.png", bbox_inches="tight")
plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/{x_var}_log_bottom50pop.png", bbox_inches="tight")
plt.show()

# %% 
################### Regressions - levels growth ###################
### Adjust variable ###
x_var = 'PUBLIC HEALTH & PREV MEDICINE'

nih_set = nih.copy()
# nih_set = nih.nlargest(50, 'funding_pc_1998')
# nih_set = nih.nlargest(100, 'total_pop')
# nih_set = nih.nsmallest(100, 'funding_pc_1998')
# nih_set = nih.nsmallest(50, 'total_pop')

y = nih_set['percap_98_03']
x = nih_set[x_var]
x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))
plt.scatter(nih_set[x_var], nih_set['percap_98_03'], label="MSAs", alpha=0)
# nih["CBSA_title_abbrev_largeMSA"] = (
#     nih["CBSA_title_abbrev_largeMSA"]
#     .fillna("")
# )
for _, row in nih_set.iterrows():
    plt.annotate(
        row['CBSA_title_abbrev'],           
        (row[x_var], row['percap_98_03']),  
        xytext=(5, 5),                      
        textcoords="offset points",
        fontsize=6,
        alpha=0.7,
        ha="center",
        va="center"
    )
X_sorted = sm.add_constant(nih_set[x_var])
y_pred = model.predict(X_sorted)

plt.plot(nih_set[x_var], y_pred, color='red', label="OLS fit")
plt.legend()
plt.xlabel(x_var)
plt.ylabel("percap_98_03")
x_var = 'public_health'
plt.title(f"Levels Growth and {x_var}")

# plt.savefig(base_path / f"Outputs/Explore_Reg_Full/{x_var}_level_full.png", bbox_inches="tight")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/{x_var}_level_top50funding.png", bbox_inches="tight")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/{x_var}_level_top100pop.png", bbox_inches="tight")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/{x_var}_level_bottom100funding.png", bbox_inches="tight")
plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/{x_var}_level_bottom50pop.png", bbox_inches="tight")
plt.show()


# %% 
################### With Controls - log growth ###################
 ### Adjust variable ###
x_var = 'share_educ_indus'

# Get data
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")
nih = nih[nih['year'] == 1998]
nih = nih.dropna(subset=['log_98_03'])

 ### Full Dataset Version ###
y = nih['log_98_03']
x = nih[[x_var, 'funding_log_percap']]
nih_reg = nih

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))

nih["resid_log"] = model.resid
nih_reg_sorted = nih.sort_values(x_var)
plt.scatter(nih_reg_sorted[x_var], nih_reg_sorted["resid_log"], alpha=0)

for r in nih_reg_sorted.itertuples(index=False):
    if r.CBSA_title_abbrev:
        plt.text(
            getattr(r, x_var),
            r.resid_log,
            r.CBSA_title_abbrev,
            fontsize=6,
            alpha=0.7,
            ha="center",
            va="center"
        )

plt.axhline(0, color="red", linewidth=1)

plt.xlabel(x_var)
plt.ylabel("Residual (log_98_03)")
plt.title(f"Residualized log growth vs {x_var}\n(controlling for 1998 funding)", fontsize=10)
plt.savefig(base_path / f"Outputs/Explore_Reg_Full/log_control/log_control_full_{x_var}.png", bbox_inches="tight")
plt.show()