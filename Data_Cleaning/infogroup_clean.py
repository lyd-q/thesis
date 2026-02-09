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
naics_codes['primary_naics_code'] = naics_codes['primary_naics_code'].astype(int)
naics_codes['naics_code_2dig'] = naics_codes['primary_naics_code'] // 1000000
naics_codes['naics_code_4dig'] = naics_codes['primary_naics_code'] // 10000
naics_codes = naics_codes.loc[naics_codes['naics_code_4dig'].isin([5417, 6113]) | (naics_codes['naics_code_2dig'] == 62)]
# "Scientific Research and Development Services", "Colleges, Universities, and Professional Schools", "Health Care and Social Assistance"
np.savetxt(
    base_path / "Data/Crosswalks/naics_codes.txt",
    naics_codes['primary_naics_code'].astype(int),
    fmt="%s"
)
# %%
infog_97_07 = pd.read_csv(base_path / "Raw_data/Infogroup/infog_97_07_naics.csv",
    dtype={
            "archive_version_year": "int64",
            "abi": "string",
            "ticker": "string",
            "parent_number": "string",
            "company": "string",
            "address_line_1": "string",
            "city": "string",
            "state": "string",
            "zipcode": "string",
            "zip4": "string",
            "county_code": "string",
            "area_code": "string",
            "idcode": "string",
            "location_employee_size_code": "string",
            "primary_sic_code": "string",
            "sic6_descriptions": "string",
            "primary_naics_code": "string",
            "naics8_descriptions": "string",
            "sic_code": "string",
            "sic6_descriptions_sic": "string",
            "business_status_code": "string",
            "industry_specific_first_byte": "string",
            "office_size_code": "string",
            "company_holding_status": "string",
            "subsidiary_number": "string",
            "parent_employee_size_code": "string",
            "parent_sales_volume_code": "string",
            "site_number": "string",
            "address_type_indicator": "string",
            "population_code": "string",
            "census_tract": "string",
            "census_block": "string",
            "match_code": "string",
            "cbsa_code": "string",
            "cbsa_level": "string",
            "csa_code": "string",
            "fips_code": "string",
            "year_established": "float64",
            "employee_size_location": "float64",
            "sales_volume_location": "float64",
            "parent_actual_employee_size": "float64",
            "parent_actual_sales_volume": "float64",
            "latitude": "float64",
            "longitude": "float64",
        }
)
# %%
# look at 1997 for an example
infog_97 = infog_97_07[infog_97_07['archive_version_year'] == 1997]
infog_97.to_csv(base_path / 'Raw_data/Infogroup/infog_97_naics.csv', index=False)
# %%
# keep only relevant NAICS
cbsa = pd.read_csv(base_path / "Data/Crosswalks/cbsa_codes.txt", header=None)
infog_97_cbsa = infog_97[infog_97['cbsa_code'].isin(cbsa[0].astype(str))]
infog_97_cbsa.to_csv(base_path / "Data/Infogroup/infog_97_cbsa.csv")
# %%
infog_97_cbsa_geo = infog_97_cbsa[['latitude', 'longitude']]
infog_97_cbsa_geo.to_csv(base_path / "Data/Infogroup/infog_97_cbsa_geo.csv")


# %% ### Let's try just Boston
infog_97_boston = infog_97_cbsa[infog_97_cbsa['cbsa_code']=="14460"]
infog_97_boston.to_csv(base_path / "Data/Infogroup/infog_97_boston.csv")

# %%
