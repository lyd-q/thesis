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
################## Mean Reversion ###################
nih_set = nih.copy()
# nih_set = nih.nlargest(50, 'funding_log_percap_5')
y = nih_set['log_funding_2003']
x = nih_set['log_funding_1998']

x = sm.add_constant(x)
model = sm.OLS(y, x).fit(cov_type='HC1')
print(model.summary(title='Mean Reversion'))

plt.scatter(nih['log_funding_1998'], nih['log_funding_2003'], label="MSAs", alpha=0)
for _, row in nih.iterrows():
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
X_sorted = sm.add_constant(nih['log_funding_1998'])
y_pred = model.predict(X_sorted)

plt.plot(nih['log_funding_1998'], y_pred, color='red', label="OLS fit")

plt.legend()
plt.xlabel('log_funding_1998')
plt.ylabel("log_funding_2003")
plt.title("Mean Reversion")
plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/mean_reversion_log.png", bbox_inches="tight")
# plt.savefig(base_path / f"Outputs/Explore_Reg_Subset/mean_reversion_log_top50funding.png", bbox_inches="tight")
plt.show()
# %%
