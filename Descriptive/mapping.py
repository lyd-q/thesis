# %%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.colors import Normalize

base_path = Path(__file__).resolve().parent.parent

#%% 
##### OLD VERSION #####
df_funding = pd.read_csv(base_path / "Data/Cleaned/nih_census.csv")

CBSACODE= "CBSA_code"
CBSATITLE = "CBSA_title"
YEAR = "year"
FUNDING = "log_funding_dollars"

df_funding[YEAR] = df_funding[YEAR].astype(int)
df_funding[CBSACODE] = df_funding[CBSACODE].astype(str).str.zfill(5)
df_funding = df_funding[df_funding["year"].between(1997, 2004)]

vmin = df_funding[FUNDING].min()
vmax = df_funding[FUNDING].max()
print("Global range:", vmin, "→", vmax)

vals = df_funding[FUNDING].dropna().to_numpy()
bins = np.quantile(vals, [i/10 for i in range(1, 10)]).tolist()
print("Shared bins:", bins)

for year in range(1998, 2005):  # 1998..2003
    df_funding_year = df_funding[df_funding[YEAR] == year]
    # Read in CBSA shapefile
    cbsa_path = f"{base_path}/Data/Mapping/tl_2010_us_cbsa10.zip"
    g_cbsa = gpd.read_file(cbsa_path)
    print(g_cbsa.columns)

    g_msa = g_cbsa[g_cbsa["LSAD10"] == "M1"].copy()
    g = g_msa.merge(df_funding_year, left_on="CBSAFP10", right_on=CBSACODE, how="left")
    g_plot = g.to_crs(5070)
    fig, ax = plt.subplots(figsize=(11, 8))
    g_plot.plot(
        column=FUNDING,
        cmap="YlGnBu",
        legend=True,
        scheme="UserDefined",
        classification_kwds={"bins": bins}, 
        missing_kwds={"color": "white", "label": "No data"},
        linewidth=0.2, edgecolor="black",
        legend_kwds={"title": "Log(Funding ($ FY2000))", "loc": "lower left",
        "fontsize": 8,
        "markerscale": 0.7,
        "labelspacing": 0.3,},
        # legend_kwds={"title": "Funding (FY2000 $ in Millions)", "loc": "lower left",
        # "fontsize": 8,
        # "markerscale": 0.7,
        # "labelspacing": 0.3,},
        ax=ax
    )
    # ax.set_title(f"NIH Funding by MSA, {year}", pad=12)
    ax.set_title(f"NIH Log Funding by MSA, {year}", pad=12)
    ax.set_axis_off()
    print(f"Saved map for {year}")
    output_png = f"{base_path}/Outputs/Maps/Log_dollars/funding_map_{year}.png"
    plt.savefig(output_png, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

    print(f"Saved map and data for {year}")
#%% 
##### NEW VERSION - PER CAPITA #####
df_funding = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_upload.csv")

CBSACODE= "CBSA_code"
CBSATITLE = "CBSA_title"
YEAR = "year"
FUNDING = "funding_log_percap"

df_funding[YEAR] = df_funding[YEAR].astype(int)
df_funding[CBSACODE] = df_funding[CBSACODE].astype(str).str.zfill(5)
df_funding = df_funding[df_funding["year"].between(1998, 2003)]

vmin = df_funding[FUNDING].min()
vmax = df_funding[FUNDING].max()
# norm = Normalize(vmin=vmin, vmax=vmax)
print("Global range:", vmin, "→", vmax)

vals = df_funding[FUNDING].dropna().to_numpy()
bins = np.quantile(vals, [i/10 for i in range(1, 10)]).tolist()
print("Shared bins:", bins)

for year in range(1998, 2004):  # 1998..2003
    df_funding_year = df_funding[df_funding[YEAR] == year]
    # Read in CBSA shapefile
    cbsa_path = f"{base_path}/Data/Mapping/tl_2010_us_cbsa10.zip"
    g_cbsa = gpd.read_file(cbsa_path)
    print(g_cbsa.columns)

    g_msa = g_cbsa[g_cbsa["LSAD10"] == "M1"].copy()
    g = g_msa.merge(df_funding_year, left_on="CBSAFP10", right_on=CBSACODE, how="inner")
    g_plot = g.to_crs(5070)
    fig, ax = plt.subplots(figsize=(11, 8))
    g_plot.plot(
        column=FUNDING,
        cmap="YlGnBu",
        legend=True,
        scheme="UserDefined",
        classification_kwds={"bins": bins}, 
        missing_kwds={"color": "white", "label": "No data"},
        #norm=norm,
        linewidth=0.2, edgecolor="black",
        legend_kwds={"title": "Log funding per capita", "loc": "upper right",
        "fontsize": 8,
        "markerscale": 0.7,
        "labelspacing": 0.3,},
        ax=ax
    )
    ax.set_title(f"Funding by MSA, {year}", pad=12)
    ax.set_axis_off()
    print(f"Saved map for {year}")
    output_png = f"{base_path}/Outputs/Maps/Log_percap/funding_map_{year}.png"
    plt.savefig(output_png, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

    print(f"Saved map and data for {year}")

# %%
# also do with log growth

df_funding = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_upload.csv")

CBSACODE= "CBSA_code"
CBSATITLE = "CBSA_title"
YEAR = "year"
FUNDING = "log_98_03"

df_funding[YEAR] = df_funding[YEAR].astype(int)
df_funding[CBSACODE] = df_funding[CBSACODE].astype(str).str.zfill(5)
df_funding = df_funding[df_funding["year"] == 1998]

# Read in CBSA shapefile
cbsa_path = f"{base_path}/Data/Mapping/tl_2010_us_cbsa10.zip"
g_cbsa = gpd.read_file(cbsa_path)
print(g_cbsa.columns)

g_msa = g_cbsa[g_cbsa["LSAD10"] == "M1"].copy()
g = g_msa.merge(df_funding, left_on="CBSAFP10", right_on=CBSACODE, how="inner")
g_plot = g.to_crs(5070)
fig, ax = plt.subplots(figsize=(11, 8))
g_plot.plot(
    column=FUNDING,
    cmap="YlGnBu",
    legend=True,
    scheme="Quantiles",
    k=10,
    linewidth=0.2, edgecolor="black",
    legend_kwds={"title": "Log growth", "loc": "upper right",
    "fontsize": 8,
    "markerscale": 0.7,
    "labelspacing": 0.3,},
    ax=ax
)
ax.set_title(f"Log Growth 1998-2003 by MSA", pad=12)
ax.set_axis_off()
print(f"Saved map")
output_png = f"{base_path}/Outputs/Maps/funding_map_growth.png"
plt.savefig(output_png, dpi=300, bbox_inches="tight")
plt.show()
plt.close()

print(f"Saved map")
# %%
