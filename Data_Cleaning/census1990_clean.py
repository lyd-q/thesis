# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
base_path = Path(__file__).resolve().parent.parent.parent

# %%
census1990 = pd.read_csv(base_path / "Raw_data/Census/census_1990/census1990.csv")

keep = ["STUSAB", "COUNTY", "COUNTYA", "STATE", "STATEA", "ET1001", "E37006", "E37007", "E4P014", "E4P015", "E4U001", "E01001"]
census1990 = census1990[keep]

# %%
rename_dict = {
    "STUSAB": "state_abbrev",
    "COUNTY": "county_name",
    "COUNTYA": "county_code",
    "STATE": "state_name",
    "STATEA": "state_code",
    "ET1001": "total_pop",
    "E37006": "bachelors_deg",
    "E37007": "graduate_deg",
    "E4P014": "indus_health_services",
    "E4P015": "indus_educ_services",
    "E4U001": "income_household_median",
    "E01001": "income_per_cap"
}
census1990 = census1990.rename(columns=rename_dict)
census1990.head()

#%%
census1990 = census1990.iloc[1:]
census1990[['county_code', 'state_code']] = census1990[['county_code', 'state_code']].astype(str)
census1990.head()
# %%
# make combined county code
census1990['county'] = census1990['state_code'] + census1990['county_code']
census1990['county'] = census1990['county'].astype('string').str.strip().str.zfill(5)
census1990.head()