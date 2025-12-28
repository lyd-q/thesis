
#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


#%%
base_path = "/Users/lydia/Desktop/Thesis"
nih = pd.read_stata(f"{base_path}/Data/NIH_v3/nih_cbsa_msa.dta")
nih.head()

# %%
base_path = Path(__file__).resolve().parent.parent.parent

# %%
# Keep relevant info
nih = nih['ORGANIZATIONNAME', 'PROJECTNUMBER', 'FUNDINGMECHANISM', 'PINAME', 'PIPERSONID',
           'PROJECTTITLE', 'FUNDING', 'CONGRESSIONALDISTRICT', 
           'city', 'state', 'county_fips', 'county_name',
           'CBSA_code',
           'org_dept', 'org_duns']

# %%
nih.to_csv(base_path / "Data/NIH_v3/nih_grants_complete.csv")

# This is what I plan to upload to RDC
# could append BDS outcomes and census info, but maybe just at collapsed level (which I can always merge back to individual level)