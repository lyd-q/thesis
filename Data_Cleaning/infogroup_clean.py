# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
base_path = Path(__file__).resolve().parent.parent.parent

#%%
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_use.csv")
# %%
cbsa = nih['cbsa_code'].astype(str).unique()
np.savetxt(
    base_path / "Data/Crosswalks/cbsa_codes.txt",
    cbsa,
    fmt="%s"
)
# with open(base_path / "Data/Crosswalks/cbsa_codes.txt", "w") as f:
#     f.write(str(cbsa))
# np.savetxt(base_path / "Data/Crosswalks/cbsa_codes.txt", str(cbsa))

# %%
infog_97 = pd.read_csv(base_path / "Raw_data/Infogroup/infog_97.csv", low_memory=False)
infog_97.head
# %%
naics = infog_97[['primary_naics_code', 'naics8_descriptions']].sort_values('primary_naics_code').drop_duplicates()
np.savetxt(
    base_path / "Data/Crosswalks/naics.txt",
    naics,
    fmt="%s"
)
# %%
naics_codes = infog_97[['primary_naics_code']].drop_duplicates().sort_values(['primary_naics_code'])
naics_codes.dtypes
naics_codes['naics_code_2dig'] = naics_codes['primary_naics_code'] // 1000000
naics_codes = naics_codes.loc[naics_codes['naics_code_2dig'].isin([54, 61, 62])]
np.savetxt(
    base_path / "Data/Crosswalks/naics_codes.txt",
    naics_codes['primary_naics_code'].astype(int),
    fmt="%s"
)
# %%
infog_97_07 = pd.read_csv(base_path / "Raw_data/Infogroup/infog_97_07.csv", low_memory=False)
# %%
infog_97 = infog_97_07[['archive_version_year'] == 1997]
infog_97.to_csv('')