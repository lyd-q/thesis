# %% Import packages
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import statsmodels.api as sm
base_path = Path(__file__).resolve().parent.parent


# %% ################## Mean Reversion ###################
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")
nih = nih[nih['year'] == 2003]
nih = nih.dropna(subset=['log_98_03'])
nih = nih.nlargest(50, 'funding_log_percap_5')
y = nih['funding_log_percap']
x = nih['funding_log_percap_5']

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title='Mean Reversion'))
plt.scatter(nih['funding_log_percap_5'], nih['funding_log_percap'], label="MSAs", alpha=0)
for _, row in nih.iterrows():
    plt.annotate(
        row['CBSA_title_abbrev'],           
        (row['funding_log_percap_5'], row['funding_log_percap']),  
        xytext=(5, 5),                      
        textcoords="offset points",
        fontsize=6,
        alpha=0.7,
        ha="center",
        va="center"
    )

# Predict
X_sorted = sm.add_constant(nih['funding_log_percap_5'])
y_pred = model.predict(X_sorted)

plt.plot(nih['funding_log_percap_5'], y_pred, color='red', label="OLS fit")

plt.legend()
plt.xlabel('funding_log_percap_5')
plt.ylabel("funding_log_percap")
plt.title("Mean Reversion")
plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/mean_reversion_log_top50funding.png", bbox_inches="tight")
plt.show()


# %%
# ['Unnamed: 0', 'CBSA_code', 'year', 'CBSA_level', 'CBSA_title', 'state',
#        'funding_dollars', 'total_pop', 'total_income_imputed', 'bachelors_deg',
#        'graduate_deg', 'income_per_cap', 'share_college', 'share_gradschool',
#        'funding_dollars_percap', 'funding_log', 'funding_log_percap',
#        'funding_dollars_1', 'funding_dollars_percap_1', 'funding_log_1',
#        'funding_log_percap_1', 'funding_dollars_2', 'funding_dollars_percap_2',
#        'funding_log_2', 'funding_log_percap_2', 'funding_dollars_3',
#        'funding_dollars_percap_3', 'funding_log_3', 'funding_log_percap_3',
#        'funding_dollars_4', 'funding_dollars_percap_4', 'funding_log_4',
#        'funding_log_percap_4', 'funding_dollars_5', 'funding_dollars_percap_5',
#        'funding_log_5', 'funding_log_percap_5', 'log_98_03', 'percap_98_03',
#        'share_health_indus', 'share_educ_indus', 'CBSA_title_abbrev',
#        'CBSA_title_abbrev_largeMSA']
################### Full Regressions - log growth ###################
# %% ### Adjust variable ###
x_var = 'funding_log_percap_1'

# Get data
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")
nih = nih[nih['year'] == 1998]
nih = nih.dropna(subset=['log_98_03'])


 ### Full Dataset Version ###
y = nih['log_98_03']
x = nih[x_var]
nih_reg = nih

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))
nih_reg_sorted = nih_reg.sort_values(x_var)
plt.scatter(nih_reg_sorted[x_var], nih_reg_sorted['log_98_03'], label="MSAs", alpha=0)
# nih["CBSA_title_abbrev_largeMSA"] = (
#     nih["CBSA_title_abbrev_largeMSA"]
#     .fillna("")
# )
for _, row in nih_reg_sorted.iterrows():
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

# Predict
X_sorted = sm.add_constant(nih_reg_sorted[x_var])
y_pred = model.predict(X_sorted)

plt.plot(nih_reg_sorted[x_var], y_pred, color='red', label="OLS fit")

plt.legend()
plt.xlabel(x_var)
plt.ylabel("log_98_03")
plt.title(f"Log Growth and {x_var}, All observations")
plt.savefig(base_path / f"Outputs/Explore_Reg_Full/log/log_full_{x_var}.png", bbox_inches="tight")
plt.show()

# %%
################### Full Regressions - percap growth ###################
x_var = 'funding_dollars_percap_1'

 ### Full Dataset Version ###
y = nih['percap_98_03']
x = nih[x_var]
nih_reg = nih

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))
nih_reg_sorted = nih_reg.sort_values(x_var)
plt.scatter(nih_reg_sorted[x_var], nih_reg_sorted['percap_98_03'], label="MSAs", alpha=0)

for _, row in nih_reg_sorted.iterrows():
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

# Predict
X_sorted = sm.add_constant(nih_reg_sorted[x_var])
y_pred = model.predict(X_sorted)

plt.plot(nih_reg_sorted[x_var], y_pred, color='red', label="OLS fit")

plt.legend()
plt.xlabel(x_var)
plt.ylabel("percap_98_03")
plt.title(f"Dollars per Capita Growth and {x_var}, All observations")
plt.savefig(base_path / f"Outputs/Explore_Reg_Full/percap/percap_full_{x_var}.png", bbox_inches="tight")
plt.show()


# %% ################### With Controls - log growth ###################
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


# ['Unnamed: 0', 'CBSA_code', 'year', 'CBSA_level', 'CBSA_title', 'state',
#        'funding_dollars', 'total_pop', 'total_income_imputed', 'bachelors_deg',
#        'graduate_deg', 'income_per_cap', 'share_college', 'share_gradschool',
#        'funding_dollars_percap', 'funding_log', 'funding_log_percap',
#        'funding_dollars_1', 'funding_dollars_percap_1', 'funding_log_1',
#        'funding_log_percap_1', 'funding_dollars_2', 'funding_dollars_percap_2',
#        'funding_log_2', 'funding_log_percap_2', 'funding_dollars_3',
#        'funding_dollars_percap_3', 'funding_log_3', 'funding_log_percap_3',
#        'funding_dollars_4', 'funding_dollars_percap_4', 'funding_log_4',
#        'funding_log_percap_4', 'funding_dollars_5', 'funding_dollars_percap_5',
#        'funding_log_5', 'funding_log_percap_5', 'log_98_03', 'percap_98_03',
#        'share_health_indus', 'share_educ_indus', 'CBSA_title_abbrev',
#        'CBSA_title_abbrev_largeMSA']
# %% ################### With Controls - percap growth ###################
 ### Adjust variable ###
x_var = 'funding_dollars_1'

# Get data
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")
nih = nih[nih['year'] == 1998]
nih = nih.dropna(subset=['percap_98_03'])

 ### Full Dataset Version ###
y = nih['percap_98_03']
x = nih[[x_var, 'funding_dollars_percap']]
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
plt.ylabel("Residual (percap_98_03)")
plt.title(f"Residualized per capita growth vs {x_var}\n(controlling for 1998 funding)", fontsize=10)
plt.savefig(base_path / f"Outputs/Explore_Reg_Full/percap_control/percap_control_full_{x_var}.png", bbox_inches="tight")
plt.show()



# %% ################### Subset Regressions ###################
# ['Unnamed: 0', 'CBSA_code', 'year', 'CBSA_level', 'CBSA_title', 'state',
#        'funding_dollars', 'total_pop', 'total_income_imputed', 'bachelors_deg',
#        'graduate_deg', 'income_per_cap', 'share_college', 'share_gradschool',
#        'funding_dollars_percap', 'funding_log', 'funding_log_percap',
#        'funding_dollars_1', 'funding_dollars_percap_1', 'funding_log_1',
#        'funding_log_percap_1', 'funding_dollars_2', 'funding_dollars_percap_2',
#        'funding_log_2', 'funding_log_percap_2', 'funding_dollars_3',
#        'funding_dollars_percap_3', 'funding_log_3', 'funding_log_percap_3',
#        'funding_dollars_4', 'funding_dollars_percap_4', 'funding_log_4',
#        'funding_log_percap_4', 'funding_dollars_5', 'funding_dollars_percap_5',
#        'funding_log_5', 'funding_log_percap_5', 'log_98_03', 'percap_98_03',
#        'share_health_indus', 'share_educ_indus', 'CBSA_title_abbrev',
#        'CBSA_title_abbrev_largeMSA']
################### Subset - log growth ###################
# %% ### Adjust variable ###
x_var = 'total_pop'

# Get data
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")
nih = nih[nih['year'] == 1998]
nih = nih.dropna(subset=['log_98_03'])

### Pick Subset ####
# top 50 in population 
nih = nih.nlargest(50, 'funding_log_percap')

y = nih['log_98_03']
x = nih[x_var]
nih_reg = nih

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))
nih_reg_sorted = nih_reg.sort_values(x_var)
plt.scatter(nih_reg_sorted[x_var], nih_reg_sorted['log_98_03'], label="MSAs", alpha=0)

for _, row in nih_reg_sorted.iterrows():
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

# Predict
X_sorted = sm.add_constant(nih_reg_sorted[x_var])
y_pred = model.predict(X_sorted)

plt.plot(nih_reg_sorted[x_var], y_pred, color='red', label="OLS fit")

plt.legend()
plt.xlabel(x_var)
plt.ylabel("log_98_03")
plt.title(f"Log Growth vs {x_var}\nTop 50 MSAs by Funding")
plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/funding_top50/log_{x_var}.png", bbox_inches="tight")
plt.show()


################### Subset - percap growth ###################
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")
nih = nih[nih['year'] == 1998]
nih = nih.dropna(subset=['percap_98_03'])

### Pick Subset ####
# top 50 in population 
nih = nih.nlargest(50, 'funding_dollars_percap')

y = nih['percap_98_03']
x = nih[x_var]
nih_reg = nih
x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title="Funding Growth (1998–2003) by MSA"))
nih_reg_sorted = nih_reg.sort_values(x_var)
plt.scatter(nih_reg_sorted[x_var], nih_reg_sorted['percap_98_03'], label="MSAs", alpha=0)

for _, row in nih_reg_sorted.iterrows():
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

# Predict
X_sorted = sm.add_constant(nih_reg_sorted[x_var])
y_pred = model.predict(X_sorted)

plt.plot(nih_reg_sorted[x_var], y_pred, color='red', label="OLS fit")

plt.legend()
plt.xlabel(x_var)
plt.ylabel("percap_98_03")
plt.title(f"Dollars per Capita Growth and {x_var}\nTop 50 MSAs by Funding")
plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/funding_top50/percap_{x_var}.png", bbox_inches="tight")
plt.show()


# %% ################### Subset with Controls - log growth ###################
# ['Unnamed: 0', 'CBSA_code', 'year', 'CBSA_level', 'CBSA_title', 'state',
#        'funding_dollars', 'total_pop', 'total_income_imputed', 'bachelors_deg',
#        'graduate_deg', 'income_per_cap', 'share_college', 'share_gradschool',
#        'funding_dollars_percap', 'funding_log', 'funding_log_percap',
#        'funding_dollars_1', 'funding_dollars_percap_1', 'funding_log_1',
#        'funding_log_percap_1', 'funding_dollars_2', 'funding_dollars_percap_2',
#        'funding_log_2', 'funding_log_percap_2', 'funding_dollars_3',
#        'funding_dollars_percap_3', 'funding_log_3', 'funding_log_percap_3',
#        'funding_dollars_4', 'funding_dollars_percap_4', 'funding_log_4',
#        'funding_log_percap_4', 'funding_dollars_5', 'funding_dollars_percap_5',
#        'funding_log_5', 'funding_log_percap_5', 'log_98_03', 'percap_98_03',
#        'share_health_indus', 'share_educ_indus', 'CBSA_title_abbrev',
#        'CBSA_title_abbrev_largeMSA']
### Adjust variable ###
x_var = 'total_pop'

# Get data
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")
nih = nih[nih['year'] == 1998]
nih = nih.dropna(subset=['log_98_03'])

### Pick Subset ####
# top 50 in percap funding 
nih = nih.nlargest(50, 'total_pop')

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

# add fitted line
X_line = sm.add_constant(nih_reg_sorted[x_var])
fit_line = sm.OLS(nih_reg_sorted["resid_log"], X_line).fit()

x_grid = nih_reg_sorted[x_var]
y_hat = fit_line.predict(X_line)

plt.plot(x_grid, y_hat, linewidth=2)  # fitted line

#plt.axhline(0, color="red", linewidth=1)

plt.xlabel(x_var)
plt.ylabel("Residual (log_98_03)")
plt.title(f"Residualized log growth vs {x_var}\nWith controls, top 50 MSAs by 1998 funding", fontsize=10)
plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/population_top50_control/log_control_{x_var}.png", bbox_inches="tight")
plt.show()

################### Subset With Controls - percap growth ###################
# Get data
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")
nih = nih[nih['year'] == 1998]
nih = nih.dropna(subset=['percap_98_03'])

### Pick Subset ####
# top 50 in percap funding 
nih = nih.nlargest(50, 'total_pop')

y = nih['percap_98_03']
x = nih[[x_var, 'funding_dollars_percap']]
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
plt.ylabel("Residual (percap_98_03)")
plt.title(f"Residualized per capita growth vs {x_var}\nWith controls, top 50 MSAs by 1998 funding", fontsize=10)
plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/population_top50_control/percap_control_{x_var}.png", bbox_inches="tight")
plt.show()
# %%
