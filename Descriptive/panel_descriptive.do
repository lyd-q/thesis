local path "/Users/lydia/Desktop/Thesis"

import delimited "`path'/Data/NIH_v3/nih_bins.csv", clear

ssc install estout, replace
*** 5-year period bins
* nominal levels
// xtset cbsa_code bin
// xtreg estabs funding 1.bin#c.funding
// xtreg estabs funding 1.bin#c.funding, fe vce(cluster cbsa_code)
// xtreg firms funding 1.bin#c.funding
// xtreg firms funding 1.bin#c.funding, fe vce(cluster cbsa_code)
// xtreg emp funding 1.bin#c.funding
// xtreg emp funding 1.bin#c.funding, fe vce(cluster cbsa_code)
//
// * per capita
// xtreg estabs_pc funding_pc 1.bin#c.funding_pc
// xtreg estabs_pc funding_pc 1.bin#c.funding_pc, fe vce(cluster cbsa_code)
// xtreg firms_pc funding_pc 1.bin#c.funding_pc
// xtreg firms_pc funding_pc 1.bin#c.funding_pc, fe vce(cluster cbsa_code)
// xtreg emp_share funding_pc 1.bin#c.funding_pc
// xtreg emp_share funding_pc 1.bin#c.funding_pc, fe vce(cluster cbsa_code)


* simple panel
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

* with bin fixed effects
xtreg emp_share c.funding_pc##ib1.bin, fe vce(cluster cbsa_code)


xtreg emp_share c.log_funding##ib1.bin, fe vce(cluster cbsa_code)



xtreg estabs_entry_rate funding_pc i.bin, fe vce(cluster cbsa_code)
xtreg estabs_entry_rate log_funding i.bin, fe vce(cluster cbsa_code)
xtreg estabs_entry_rate c.funding_pc##ib1.bin, fe vce(cluster cbsa_code)
xtreg estabs_entry_rate c.log_funding##ib1.bin, fe vce(cluster cbsa_code)

	   
/*
import delimited "`path'/Data/NIH_v3/nih_use_outcomes.csv", clear

// keep if (year >= 1997) & (year <= 2004) 

// make balanced
duplicates tag cbsa_code, gen(flag)
keep if flag == 7


xtset cbsa_code year

// y variables: firms, estabs, emp
xtsum emp funding_pc

// panel regression
xtreg emp funding_pc i.year, fe

// joint F-test on time fixed effects
testparm i.year

* coefficient is negative


* try cross-sectional
keep if year == 1998
reg emp funding_pc, vce()
reg firms funding_pc, vce()
reg estabs funding_pc, vce()

keep if year == 2003
reg emp funding_pc, vce()
reg firms funding_pc, vce()
reg estabs funding_pc, vce()

* what is statistically significant: i think because it clarifies college towns
import delimited "`path'/Data/NIH_v3/nih_use_outcomes.csv", clear
keep if year == 1998
reg emp funding_pc share_educ_indus, vce()
reg firms funding_pc share_educ_indus, vce()
reg estabs funding_pc share_educ_indus, vce()

reg emp funding_pc share_college, vce()
reg firms funding_pc share_college, vce()
reg estabs funding_pc share_college, vce()





*** TWFE DiD
import delimited "`path'/Data/NIH_v3/nih_use_outcomes.csv", clear
keep if year >= 1992 & year <= 2008

ssc install reghdfe
ssc install ftools
ssc install coefplot

xtset cbsa_code year

// exposure var = 1997 funding (funding_pc_1997)
gen post = (year >= 1998)

// gen ln_emp = ln(emp)
// gen ln_emp = ln(emp)
// gen ln_emp = ln(emp)

gen ln_estabs = ln(estabs)


reghdfe ln_emp ib0.post#c.log_funding_1997, absorb(cbsa_code year) vce(cluster cbsa_code)

// for plotting
reghdfe ln_estabs i.year#c.log_funding_1997, absorb(cbsa_code year) vce(cluster cbsa_code)
coefplot, keep(*.year#c.log_funding_1997) vertical yline(0) xline(6, lcolor(gs10) lpattern(dash)) title("Impact of NIH Doubling (1998-2003) on Firms") ylabel(, format(%9.2f))
