local path "/Users/lydia/Desktop/Thesis"

import delimited "`path'/Data/NIH_v3/nih_bins.csv", clear

keep if bin == 1

reg emp_share funding_pc, robust
* add controls
