# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
base_path = Path(__file__).resolve().parent.parent.parent
# %%
nih_county = pd.read_stata(base_path / "Data/NIH_v4/nih_county.dta")

/Users/lydia/Desktop/Thesis/Raw_data/CBP/cbp00co.txt /Users/lydia/Desktop/Thesis/Raw_data/CBP/cbp01co.txt /Users/lydia/Desktop/Thesis/Raw_data/CBP/Cbp02co.txt /Users/lydia/Desktop/Thesis/Raw_data/CBP/cbp03co.txt /Users/lydia/Desktop/Thesis/Raw_data/CBP/cbp04co.txt /Users/lydia/Desktop/Thesis/Raw_data/CBP/cbp05co.txt /Users/lydia/Desktop/Thesis/Raw_data/CBP/cbp06co.txt /Users/lydia/Desktop/Thesis/Raw_data/CBP/Cbp07co.txt /Users/lydia/Desktop/Thesis/Raw_data/CBP/Cbp08co.txt /Users/lydia/Desktop/Thesis/Raw_data/CBP/cbp98co.txt /Users/lydia/Desktop/Thesis/Raw_data/CBP/cbp99co.txt