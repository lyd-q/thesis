# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
base_path = Path(__file__).resolve().parent.parent.parent
import pandas as pd
from rapidfuzz import process, fuzz


# %%
nih_read = pd.read_stata("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_grants.dta")
nih_read.columns
nih_read.shape

# %%
nih = nih_read.copy()
# %%
taggs1 = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/HHS/TAGGS_97-06.csv")
taggs1.columns

taggs1 = taggs1.rename(columns={
    "Issue Date Fiscal Year":"year",
    "Legal Entity Name":"organizationname",
    "Legal Entity Address":"address",
    "Legal Entity City":"city",
    "Legal Entity State":"state",
    "Legal Entity ZIP Code":"zip",
    "Legal Entity County":"county_name",
    "Sum of Actions ":"funds"
})
taggs1 = taggs1.loc[taggs1.groupby(["organizationname", "county_name"])["funds"].idxmax()]
taggs1 = taggs1.drop(columns=["funds", "zip"])
taggs1 = taggs1.drop_duplicates()
print(taggs1.shape)
taggs2 = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/HHS/TAGGS_07-21.csv")
taggs2.columns
taggs2 = taggs2.rename(columns={
    "Issue Date Fiscal Year":"year",
    "Legal Entity Name":"organizationname",
    "Legal Entity Address":"address",
    "Legal Entity City":"city",
    "Legal Entity State":"state",
    "Legal Entity ZIP Code":"zip",
    "Legal Entity County":"county_name",
    "Sum of Actions ":"funds"
})
print(taggs2.shape)

taggs = pd.concat([taggs1, taggs2], axis=0)

# %%
# drop PO boxes
box = [r'POST OFFICE', r'\bP\.?O\.?\b', r'\bP\.?O\.?B\b', r'\bBOX\b']
pattern = "|".join(box)
taggs = taggs[
    ~taggs["address"]
     .str.upper()
     .str.contains(pattern, regex=True, na=False)
]
taggs["funds"] = pd.to_numeric(taggs["funds"], errors="coerce").fillna(0)
taggs = taggs.loc[taggs.groupby(["organizationname", "county_name"])["funds"].idxmax()]
taggs = taggs.drop(columns=["funds", "zip"])
taggs = taggs.drop_duplicates()

print(taggs.shape)


# %% Clean names
nih[['organizationname', 'county_name']] = nih[['organizationname', 'county_name']].apply(lambda s: s.str.upper())
taggs[['organizationname', 'county_name', 'address', 'city', 'state']] = taggs[['organizationname', 'county_name', 'address', 'city', 'state']].apply(lambda s : s.str.upper())
nih['name'] = nih['organizationname'].copy()
nih['county'] = nih['county_name'].copy()
taggs['name'] = taggs['organizationname'].copy()
taggs['county'] = taggs['county_name'].copy()

nih['name'] = nih['name'] .str.replace(r"[^A-Z0-9]", "", regex=True)
taggs['name'] = taggs['name'] .str.replace(r"[^A-Z0-9]", "", regex=True)

nih['county'] = nih['county'] .str.replace(r"[^A-Z0-9]", "", regex=True)
taggs['county'] = taggs['county'] .str.replace(r"[^A-Z0-9]", "", regex=True)

# do not match on county
nih_addresses_exact = nih.merge(taggs, how='left', on=['name'], indicator=True)
nih_addresses_exact['_merge'].value_counts()
#%% 
# exact match with PO boxes ignored
nih_addresses_exact.sort_values(by=['_merge'])
nih_addresses_exact.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses_exact.csv", index=False)




# keep unmatched to do further clean/fuzzy matching

# %%
nih_addresses.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses.csv", index=False)
 
# %%
# Normalize common abbreviations / remove glue words (word-boundary safe)
noise_and_abbrevs = {
    r"\bUNIV\b": "UNIVERSITY",
    r"\bSCH\b": "SCHOOL",
    r"\bCTR\b": "CENTER",
    r"\bREGENTS\b": "",        # optional
    r"\bOF\b": "",
    r"\bAND\b": "",
    r"\bST\.?\b": "SAINT",     # matches ST and ST.
}

def clean_org_column(df, col_name):
    # 1) Use pandas string dtype; keep missing as empty string (avoid "NAN")
    s = df[col_name].astype("string").fillna("").str.upper()

    # 2) Normalize punctuation/separators to spaces BEFORE word-level replacements
    s = (s.str.replace(r"[^A-Z0-9 ]", " ", regex=True)
           .str.replace(r"\s+", " ", regex=True)
           .str.strip())

    # 3) Expand/remove specific words with word boundaries
    for pattern, replacement in noise_and_abbrevs.items():
        s = s.str.replace(pattern, replacement, regex=True)

    # 4) Re-collapse whitespace after replacements
    s = (s.str.replace(r"\s+", " ", regex=True)
           .str.strip())

    # 5) Crush to alphanumeric-only (no spaces) for matching key
    s = s.str.replace(r"[^A-Z0-9]", "", regex=True)

    # Write back (overwriting col_name, since it's already your working copy)
    df[col_name] = s
    return df

# Apply in-place to your working columns
clean_org_column(nih, "name")
clean_org_column(nih, "county")

clean_org_column(taggs, "name")
clean_org_column(taggs, "county")


# nih['county'] = nih['county'].str.replace(r"[^A-Z0-9]", "", regex=True)
# taggs['county'] = taggs['county'].str.replace(r"[^A-Z0-9]", "", regex=True)
# nih['county'] = nih['county'].str.replace(r"\bST\b", "", regex=True)
# taggs['county'] = taggs['county'].str.replace(r"\bST\b", "", regex=True)
# nih['county'] = nih['county'].str.replace(r"\s+", "", regex=True)
# taggs['county'] = taggs['county'].str.replace(r"\s+", "", regex=True)


# nih['name'] = nih['name'].str.replace(r"[^A-Z0-9]", "", regex=True)
# taggs['name'] = taggs['name'].str.replace(r"[^A-Z0-9]", "", regex=True)

# replace = {
#     r"\bUNIV\b": "UNIVERSITY",
#     r"\bSCH\b": "SCHOOL",
#     r"\bCTR\b": "CENTER",
# }
# for pattern, rep in replace.items():
#     nih['name'] = nih['name'].str.replace(pattern, rep, regex=True)
# nih['name'] = nih['name'].str.replace(r"\bREGENTS\b", "", regex=True)
# nih['name'] = nih['name'].str.replace(r"\bOF\b", "", regex=True)
# nih['name'] = nih['name'].str.replace(r"\s+", " ", regex=True).str.strip()

# for pattern, rep in replace.items():
#     taggs['name'] = taggs['name'].str.replace(pattern, rep, regex=True)
# taggs['name'] = taggs['name'].str.replace(r"\bREGENTS\b", "", regex=True)
# taggs['name'] = taggs['name'].str.replace(r"\bOF\b", "", regex=True)
# taggs['name'] = taggs['name'].str.replace(r"\s+", " ", regex=True).str.strip()

#%% Do exact match first
print(nih.shape)
print(taggs.shape)
nih_addresses = nih.merge(taggs, how='left', on=['organizationname', 'county'], indicator=True)
nih_addresses['_merge'].value_counts()
#%%
nih_addresses.sort_values(by=['_merge'])
nih_addresses.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses_keepPO.csv", index=False)


# %%
nih_addresses_v2 = nih.merge(taggs, how='left', on=['organizationname'], indicator=True)
nih_addresses_v2['_merge'].value_counts()
#%%
nih_addresses_v2.sort_values(by=['_merge'])
nih_addresses_v2.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses_v2.csv", index=False)
# %%
nih_unmatched_v2 = nih_addresses_v2[nih_addresses_v2['_merge'] == 'left_only']
print(nih_unmatched_v2['organizationname'].nunique())
nih_unmatched_v2.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses.csv", index=False)
# %%

# Normal merge
# both          1359919
# left_only      867299

# With punctuation removed
# both          1538412
# left_only      743149

# With spaces also removed
# both          1547172
# left_only      738752

# with PO removed
both          1141715
left_only      753004

after regex and universities
both          1677030
left_only      729607

With new regex
both          984419
left_only     876325

# PO removed, regex, name only
both          1654665
left_only      541458
= 75% match rate
# %%
nih = pd.read_stata("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_grants.dta")
nih.columns
nih.
# %%
taggs1 = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/HHS/TAGGS_97-06.csv")
taggs1.columns

taggs1 = taggs1.rename(columns={
    "Issue Date Fiscal Year":"year",
    "Legal Entity Name":"organizationname",
    "Legal Entity Address":"address",
    "Legal Entity City":"city",
    "Legal Entity State":"state",
    "Legal Entity ZIP Code":"zip",
    "Legal Entity County":"county_name",
    "Sum of Actions ":"funds"
})
taggs1 = taggs1.loc[taggs1.groupby(["organizationname", "county_name"])["funds"].idxmax()]
taggs1 = taggs1.drop(columns=["funds", "zip"])
taggs1 = taggs1.drop_duplicates()
print(taggs1.shape)
# %%
taggs2 = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/HHS/TAGGS_07-21.csv")
taggs2.columns
taggs2 = taggs2.rename(columns={
    "Issue Date Fiscal Year":"year",
    "Legal Entity Name":"organizationname",
    "Legal Entity Address":"address",
    "Legal Entity City":"city",
    "Legal Entity State":"state",
    "Legal Entity ZIP Code":"zip",
    "Legal Entity County":"county_name",
    "Sum of Actions ":"funds"
})
taggs2 = taggs2.loc[taggs2.groupby(["organizationname", "county_name"])["funds"].idxmax()]
taggs2 = taggs2.drop(columns=["funds", "zip"])
taggs2 = taggs2.drop_duplicates()
print(taggs2.shape)

taggs = pd.concat([taggs1, taggs2], axis=0)
taggs.shape

# %% Try merging
nih[['organizationname', 'county_name']] = nih[['organizationname', 'county_name']].apply(lambda s: s.str.upper())
taggs[['organizationname', 'county_name']] = taggs[['organizationname', 'county_name']].apply(lambda s : s.str.upper())
nih_addresses = nih.merge(taggs, how='left', on=['organizationname', 'county_name'], indicator=True)
# %% Try merging
nih[['organizationname', 'county_name']] = nih[['organizationname', 'county_name']].apply(lambda s: s.str.upper())
taggs[['organizationname', 'county_name']] = taggs[['organizationname', 'county_name']].apply(lambda s : s.str.upper())

nih['organizationname'] = nih['organizationname'] .str.replace(r"[.,]", "", regex=True)
taggs['organizationname'] = taggs['organizationname'] .str.replace(r"[.,]", "", regex=True)
nih['organizationname'] = nih['organizationname'] .str.replace(r"\s+", "", regex=True)
taggs['organizationname'] = taggs['organizationname'] .str.replace(r"\s+", "", regex=True)

nih_addresses = nih.merge(taggs, how='left', on=['organizationname', 'county_name'], indicator=True)
nih_addresses['_merge'].value_counts()
nih_addresses.sort_values(by=['_merge'])
# %%
nih_addresses_v2 = nih.merge(taggs, how='left', on=['organizationname'], indicator=True)
nih_addresses_v2['_merge'].value_counts()
nih_addresses_v2.sort_values(by=['_merge'])
nih_addresses_v2.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses_v2.csv", index=False)
# %%
nih_addresses.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses.csv", index=False)