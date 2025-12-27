
use "`path'/Data/nih_msa_collapsed_adjusted.dta", clear

* Goal: regress with past funding and MSA characteristics to see what explains the funding increase (not variation in funding - no fixed effects)
xtset CBSA_code year
gen lag1 = L1.log_FUNDING
gen lag2 = L2.log_FUNDING
gen lag3 = L3.log_FUNDING
gen lag4 = L4.log_FUNDING
gen lag5 = L5.log_FUNDING
save "`path'/Data/nih_msa_collapsed_adjusted_long.dta", replace
keep if year == 2003 & !missing(lag1, lag2, lag3, lag4, lag5)
reg log_FUNDING lag1 lag2 lag3 lag4 lag5

* long to wide
reshape wide log_FUNDING FUNDING, i(CBSA_code CBSA_title) j(year)
save "`path'/Data/nih_msa_collapsed_adjusted_wide.dta", replace
keep if funding

* can also do things with difference




