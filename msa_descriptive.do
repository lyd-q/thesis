local path "/Users/lydia/Desktop/Thesis"
log using "`path'/Log/msa_descriptive.log"

***************************************************************
* v2
use "`path'/Data/nih_msa_collapsed_adjusted.dta", clear
collapse (sum) FUNDING, by(year)
scatter FUNDING year, title("Total NIH Funding across MSAs") xtitle("Year") ytitle("$ in Millions")
save "`path'/Data/Descriptive/annual_total_adjusted.dta", replace

use "`path'/Data/nih_msa_collapsed_adjusted.dta", clear
collapse (sum) FUNDING, by(year)
gen log_FUNDING = log(FUNDING)
scatter log_FUNDING year, title("Total NIH Funding across MSAs") xtitle("Year") ytitle("Log($ in Millions)")
save "`path'/Data/Descriptive/annual_total_adjusted_log.dta", replace

***************************************************************
*** graph of total funding
use "`path'/Data/nih_msa_collapse.dta", clear
collapse (sum) FUNDING, by(year)
drop if year == 1992
* convert to millions
replace FUNDING = FUNDING / 1000000
save "`path'/Data/Descriptive/annual_total.dta", replace
scatter FUNDING year, title("Total NIH Funding across MSAs") xtitle("Year") ytitle("$ in Millions")
graph export "`path'/Results/Descriptive/annual_total.jpg", as(jpg) replace


*** CPI Inflation adjustment
clear
import excel "`path'/Data/Manual/cpi_annual_avg.xlsx", firstrow
destring year, replace
save "`path'/Data/cpi_annual_avg.dta", replace

use "`path'/Data/Descriptive/annual_total.dta", clear
merge 1:1 year using "`path'/Data/cpi_annual_avg.dta"
keep if _m == 3
drop _m
save "`path'/Data/Descriptive/annual_total_adjusted.dta", replace

gen cpi_2000 = cpi if year == 2000
egen base_cpi = max(cpi_2000)
drop cpi_2000

gen adjusted_funding = (base_cpi / cpi) * FUNDING
save "`path'/Data/Descriptive/annual_total_adjusted.dta", replace


********
use "`path'/Data/Descriptive/annual_total_adjusted.dta", clear
scatter adjusted_funding year, title("Total NIH Funding across MSAs, in FY2000 dollars") xtitle("Year") ytitle("$ in Millions")
graph export "`path'/Results/Descriptive/annual_total_adjusted.jpg", as(jpg) replace


*** graph of average funding 
use "`path'/Data/nih_msa_collapse.dta", clear
collapse (mean) FUNDING, by(year)
drop if year == 1992
* convert to millions
replace FUNDING = FUNDING / 1000000
save "`path'/Data/Descriptive/annual_mean.dta", replace

use "`path'/Data/Descriptive/annual_mean.dta", clear
scatter FUNDING year, title("Average NIH Funding taken over MSAs") xtitle("Year") ytitle("$ in Millions")
graph export "`path'/Results/Descriptive/annual_mean.jpg", as(jpg) replace

use "`path'/Data/Descriptive/annual_mean.dta", clear
merge 1:1 year using "`path'/Data/cpi_annual_avg.dta"
keep if _m == 3
drop _m
save "`path'/Data/Descriptive/annual_mean_adjusted.dta", replace

gen cpi_2000 = cpi if year == 2000
egen base_cpi = max(cpi_2000)
drop cpi_2000

gen adjusted_funding = (base_cpi / cpi) * FUNDING
save "`path'/Data/Descriptive/annual_mean_adjusted.dta", replace

********
use "`path'/Data/Descriptive/annual_mean_adjusted.dta", clear
scatter adjusted_funding year, title("Average NIH Funding taken over MSAs, in FY2000 dollars") xtitle("Year") ytitle("$ in Millions")
graph export "`path'/Results/Descriptive/annual_mean_adjusted.jpg", as(jpg) replace


log close
