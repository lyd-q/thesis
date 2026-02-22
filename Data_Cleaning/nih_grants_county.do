local path "/Users/lydia/Desktop/Thesis"

use "`path'/Data/Working/nih_counties.dta", clear

merge m:1 year using "`path'/Data/Working/cpi_annual_avg.dta"
keep if _m == 3
drop _m
save "`path'/Data/NIH_v3/nih_cbsa_msa.dta", replace

use "`path'/Data/NIH_v3/nih_cbsa_msa.dta", clear
gen cpi_2000 = cpi if year == 2000
egen base_cpi = max(cpi_2000)
drop cpi_2000

rename FUNDING funding_real
drop if funding_real == .
gen funding_adj = (base_cpi / cpi) * funding_real
drop base_cpi cpi
save "`path'/Data/NIH_v3/nih_cbsa_msa.dta", replace
