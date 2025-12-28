# %% Import packages
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import statsmodels.api as sm
base_path = Path(__file__).resolve().parent.parent.parent

# %% ################## Get File of Only 1998-2003 ###################
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_all.csv")
nih = nih.drop(columns='funding_nominal')
nih = nih[(nih['year'] == 1998) | (nih['year'] == 2003)]

nih["funding_2003"] = nih.groupby("CBSA_code")["funding"].transform(lambda x: x[nih.loc[x.index, "year"] == 2003].iloc[0])
nih["log_funding_2003"] = nih.groupby("CBSA_code")["log_funding"].transform(lambda x: x[nih.loc[x.index, "year"] == 2003].iloc[0])
nih["funding_pc_2003"] = nih.groupby("CBSA_code")["funding_pc"].transform(lambda x: x[nih.loc[x.index, "year"] == 2003].iloc[0])
nih["log_funding_pc_2003"] = nih.groupby("CBSA_code")["log_funding_pc"].transform(lambda x: x[nih.loc[x.index, "year"] == 2003].iloc[0])

nih = nih[nih["year"] == 1998]

name_change = {
    'funding_pc_1': 'funding_pc_1997',
    'log_funding_1': 'log_funding_1997',
    'log_funding_pc_1': 'log_funding_pc_1997'
}

nih.to_csv(base_path / "Data/NIH_v3/cross_sec/nih_use.csv", index=False)


# %%
rename
funding_pc_1	log_funding_1	log_funding_pc_1
# %%
