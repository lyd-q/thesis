ssc install estout, replace
local path "/Users/lydia/Desktop/Thesis"



***********************************************************
use "`path'/Data/NIH_Outcomes/sector/nih_health.dta", clear
save "`path'/Data/NIH_Outcomes/fiveyear.dta", replace

use "`path'/Data/NIH_Outcomes/fiveyear.dta", clear
// keep if year == 1993 | year == 1997
keep cbsa_code funding year pop bachelors_deg income_per_cap firms estabs emp
* make wide
// reshape wide cbsa_code funding pop firms estabs emp, i(cbsa_code) j(year)
keep if funding != .

xtset year cbsa_code
reg D5.firms D5.funding D5.pop firms estabs emp, robust

reghdfe D5.firms D5.funding D5.pop firms estabs emp, vce(cluster cbsa_code)



* simple panel (replicating brookings)
xtset cbsa_code bin
xtreg estabs funding, fe vce(cluster cbsa_code)
xtreg firms funding, fe vce(cluster cbsa_code)
xtreg emp funding, fe vce(cluster cbsa_code)

destring(funding_pc), replace
xtreg estabs_pc funding_pc, fe vce(cluster cbsa_code)
xtreg firms_pc funding_pc, fe vce(cluster cbsa_code)
*****

import delimited "`path'/Data/NIH_v3/nih_bins.csv", clear
xtset cbsa_code bin

eststo clear
preserve
	keep if bin <= 2
	eststo: xtreg emp_share funding_pc i.bin, fe vce(cluster cbsa_code)
restore
import delimited "`path'/Data/NIH_v3/nih_bins.csv", clear
xtset cbsa_code bin
eststo: xtreg emp_share funding_pc i.bin, fe vce(cluster cbsa_code)
esttab using `path'\table.tex, label replace


 
xtreg emp_share log_funding i.bin, fe vce(cluster cbsa_code)

reghdfe emp_share funding_pc, absorb(cbsa_code bin) vce(cluster cbsa_code)

