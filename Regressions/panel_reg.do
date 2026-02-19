ssc install estout, replace
local path "/Users/lydia/Desktop/Thesis"

*** Annual Estimates 
***************************************************************************
	*** Share employment
************************* SCIENCE **************************************************
import delimited "`path'/Data/NIH_Outcomes/nih_outcomes_science.csv", clear
save "`path'/Data/Stata/nih_outcomes_science.dta", replace

// Split into 5 year bins
* Dependent var: establishments per capita
// use "`path'/Data/Stata/nih_outcomes_science.dta", clear
// preserve
// keep if bin == 0 | year == 1993
// xtset cbsa_code year
// eststo b01: xtreg estabs_pc_small L.log_funding_pc, fe
// eststo b02: xtreg estabs_pc_medium L.log_funding_pc, fe
// eststo b03: xtreg estabs_pc_large L.log_funding_pc, fe
// restore
//
// preserve
// keep if bin == 1 | year == 1998
// xtset cbsa_code year
// eststo b11: xtreg estabs_pc_small L.log_funding_pc, fe
// eststo b12: xtreg estabs_pc_medium L.log_funding_pc, fe
// eststo b13: xtreg estabs_pc_large L.log_funding_pc, fe
// restore
//
// preserve
// keep if bin == 2 | year == 2003
// xtset cbsa_code year
// eststo b21: xtreg estabs_pc_small L.log_funding_pc, fe
// eststo b22: xtreg estabs_pc_medium L.log_funding_pc, fe
// eststo b23: xtreg estabs_pc_large L.log_funding_pc, fe
// restore
//
// preserve
// keep if bin == 3 | year == 2008
// xtset cbsa_code year
// eststo b31: xtreg estabs_pc_small L.log_funding_pc, fe
// eststo b32: xtreg estabs_pc_medium L.log_funding_pc, fe
// eststo b33: xtreg estabs_pc_large L.log_funding_pc, fe
// restore
//
// preserve
// keep if bin == 4 | year == 2013
// xtset cbsa_code year
// eststo b41: xtreg estabs_pc_small L.log_funding_pc, fe
// eststo b42: xtreg estabs_pc_medium L.log_funding_pc, fe
// eststo b43: xtreg estabs_pc_large L.log_funding_pc, fe
// restore
//
// esttab b01 b11 b21 b31 b41 using "`path'/Outputs/Tables/tables.csv", se replace

* Share employed, log funding per capita
use "`path'/Data/Stata/nih_outcomes_science.dta", clear
preserve
keep if bin == 0 | year == 1993
xtset cbsa_code year
eststo b01: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b02: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b03: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 1 | year == 1998
xtset cbsa_code year
eststo b11: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b12: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b13: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 2 | year == 2003
xtset cbsa_code year
eststo b21: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b22: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b23: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 3 | year == 2008
xtset cbsa_code year
eststo b31: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b32: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b33: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 4 | year == 2013
xtset cbsa_code year
eststo b41: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b42: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b43: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

* Small
esttab b01 b11 b21 b31 b41 using "`path'/Outputs/Tables/tables_small.csv", se replace
* Medium
esttab b02 b12 b22 b32 b42 using "`path'/Outputs/Tables/tables_medium.csv", se replace
* Large
esttab b03 b13 b23 b33 b43 using "`path'/Outputs/Tables/tables_large.csv", se replace


* Share employed, funding per capita
use "`path'/Data/Stata/nih_outcomes_science.dta", clear
preserve
keep if bin == 0 | year == 1993
xtset cbsa_code year
eststo b01: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b02: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b03: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 1 | year == 1998
xtset cbsa_code year
eststo b11: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b12: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b13: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 2 | year == 2003
xtset cbsa_code year
eststo b21: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b22: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b23: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 3 | year == 2008
xtset cbsa_code year
eststo b31: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b32: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b33: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 4 | year == 2013
xtset cbsa_code year
eststo b41: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b42: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b43: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

* Small
esttab b01 b11 b21 b31 b41 using "`path'/Outputs/Tables/tables_small.csv", se replace
* Medium
esttab b02 b12 b22 b32 b42 using "`path'/Outputs/Tables/tables_medium.csv", se replace
* Large
esttab b03 b13 b23 b33 b43 using "`path'/Outputs/Tables/tables_large.csv", se replace

************************* EDUCATION **************************************************
* Share employed, log funding per capita
import delimited "`path'/Data/NIH_Outcomes/nih_outcomes_educ.csv", clear
save "`path'/Data/Stata/nih_outcomes_educ.dta", replace

use "`path'/Data/Stata/nih_outcomes_educ.dta", clear
preserve
keep if bin == 0 | year == 1993
xtset cbsa_code year
eststo b01: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b02: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b03: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 1 | year == 1998
xtset cbsa_code year
eststo b11: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b12: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b13: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 2 | year == 2003
xtset cbsa_code year
eststo b21: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b22: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b23: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 3 | year == 2008
xtset cbsa_code year
eststo b31: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b32: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b33: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 4 | year == 2013
xtset cbsa_code year
eststo b41: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b42: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b43: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

* Small
esttab b01 b11 b21 b31 b41 using "`path'/Outputs/Tables/tables_small.csv", se replace
* Medium
esttab b02 b12 b22 b32 b42 using "`path'/Outputs/Tables/tables_medium.csv", se replace
* Large
esttab b03 b13 b23 b33 b43 using "`path'/Outputs/Tables/tables_large.csv", se replace


* Share employed, funding per capita
use "`path'/Data/Stata/nih_outcomes_educ.dta", clear
preserve
keep if bin == 0 | year == 1993
xtset cbsa_code year
eststo b01: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b02: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b03: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 1 | year == 1998
xtset cbsa_code year
eststo b11: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b12: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b13: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 2 | year == 2003
xtset cbsa_code year
eststo b21: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b22: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b23: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 3 | year == 2008
xtset cbsa_code year
eststo b31: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b32: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b33: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 4 | year == 2013
xtset cbsa_code year
eststo b41: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b42: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b43: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

* Small
esttab b01 b11 b21 b31 b41 using "`path'/Outputs/Tables/tables_small.csv", se replace
* Medium
esttab b02 b12 b22 b32 b42 using "`path'/Outputs/Tables/tables_medium.csv", se replace
* Large
esttab b03 b13 b23 b33 b43 using "`path'/Outputs/Tables/tables_large.csv", se replace



************************* HEALTH **************************************************
import delimited "`path'/Data/NIH_Outcomes/nih_outcomes_health.csv", clear
save "`path'/Data/Stata/nih_outcomes_health.dta", replace

* Share employed, log funding per capita
use "`path'/Data/Stata/nih_outcomes_health.dta", clear
preserve
keep if bin == 0 | year == 1993
xtset cbsa_code year
eststo b01: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b02: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b03: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 1 | year == 1998
xtset cbsa_code year
eststo b11: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b12: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b13: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 2 | year == 2003
xtset cbsa_code year
eststo b21: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b22: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b23: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 3 | year == 2008
xtset cbsa_code year
eststo b31: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b32: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b33: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 4 | year == 2013
xtset cbsa_code year
eststo b41: xtreg emp_pc_small L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b42: xtreg emp_pc_medium L.log_funding_pc i.year, fe vce(cluster cbsa_code)
eststo b43: xtreg emp_pc_large L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

* Small
esttab b01 b11 b21 b31 b41 using "`path'/Outputs/Tables/tables_small.csv", se replace
* Medium
esttab b02 b12 b22 b32 b42 using "`path'/Outputs/Tables/tables_medium.csv", se replace
* Large
esttab b03 b13 b23 b33 b43 using "`path'/Outputs/Tables/tables_large.csv", se replace


* Share employed, funding per capita
use "`path'/Data/Stata/nih_outcomes_health.dta", clear
preserve
keep if bin == 0 | year == 1993
xtset cbsa_code year
eststo b01: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b02: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b03: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 1 | year == 1998
xtset cbsa_code year
eststo b11: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b12: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b13: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 2 | year == 2003
xtset cbsa_code year
eststo b21: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b22: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b23: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 3 | year == 2008
xtset cbsa_code year
eststo b31: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b32: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b33: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 4 | year == 2013
xtset cbsa_code year
eststo b41: xtreg emp_pc_small L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b42: xtreg emp_pc_medium L.funding_pc i.year, fe vce(cluster cbsa_code)
eststo b43: xtreg emp_pc_large L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

* Small
esttab b01 b11 b21 b31 b41 using "`path'/Outputs/Tables/tables_small.csv", se replace
* Medium
esttab b02 b12 b22 b32 b42 using "`path'/Outputs/Tables/tables_medium.csv", se replace
* Large
esttab b03 b13 b23 b33 b43 using "`path'/Outputs/Tables/tables_large.csv", se replace

***************************************************************************


***************************************************************************
	*** Try on all measures (overall data)
import delimited "`path'/Data/NIH_Outcomes/nih_use_outcomes.csv", clear
gen emp_pc = emp / total_pop
save "`path'/Data/Stata/nih_outcomes.dta", replace

* Share employed, log(funding per capita)
use "`path'/Data/Stata/nih_outcomes.dta", clear

preserve
keep if bin == 0 | year == 1993
xtset cbsa_code year
eststo b01: xtreg emp_pc L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 1 | year == 1998
xtset cbsa_code year
eststo b11: xtreg emp_pc L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 2 | year == 2003
xtset cbsa_code year
eststo b21: xtreg emp_pc L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 3 | year == 2008
xtset cbsa_code year
eststo b31: xtreg emp_pc L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 4 | year == 2013
xtset cbsa_code year
eststo b41: xtreg emp_pc L.log_funding_pc i.year, fe vce(cluster cbsa_code)
restore

esttab b01 b11 b21 b31 b41 using "`path'/Outputs/Tables/tables.csv", se replace


* Share employed, funding per capita
use "`path'/Data/Stata/nih_outcomes.dta", clear

preserve
keep if bin == 0 | year == 1993
xtset cbsa_code year
eststo b01: xtreg emp_pc L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 1 | year == 1998
xtset cbsa_code year
eststo b11: xtreg emp_pc L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 2 | year == 2003
xtset cbsa_code year
eststo b21: xtreg emp_pc L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 3 | year == 2008
xtset cbsa_code year
eststo b31: xtreg emp_pc L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

preserve
keep if bin == 4 | year == 2013
xtset cbsa_code year
eststo b41: xtreg emp_pc L.funding_pc i.year, fe vce(cluster cbsa_code)
restore

esttab b01 b11 b21 b31 b41 using "`path'/Outputs/Tables/tables.csv", se replace



