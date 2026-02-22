local path "/Users/lydia/Desktop/Thesis"
ssc install estout

***************************** Annual Cross Section ******************************

***************************** SCIENCE ******************************
import delimited "`path'/Data/NIH_v4/Use/nih_science.csv", clear
save "`path'/Data/NIH_v4/Use/nih_science.dta", replace

use "`path'/Data/NIH_v4/Use/nih_science.dta", clear
* for table display purposes, will divide income percap by 1000 and college by 1mill
replace income_per_cap = income_per_cap / 1000
replace college = college / 1000000
save "`path'/Data/NIH_v4/Regress/cross_sec.dta", replace
use "`path'/Data/NIH_v4/Regress/cross_sec.dta", clear

tempfile coefstore
postfile coef year beta_firms se_firms beta_estabs se_estabs beta_emp se_emp using `coefstore', replace
				 
forvalues yr = 1992(1)2009 {
	display `yr'
	preserve
		keep if year == `yr'
		eststo f`yr': reg ln_firms ln_funding ln_pop income_per_cap college, robust
		local b_f = _b[ln_funding]
        local se_f = _se[ln_funding]
		
		eststo e`yr': reg ln_estabs ln_funding ln_pop income_per_cap college, robust
		local b_e = _b[ln_funding]
        local se_e = _se[ln_funding]
		
		eststo emp`yr': reg ln_emp ln_funding ln_pop income_per_cap college, robust
		local b_emp = _b[ln_funding]
        local se_emp = _se[ln_funding]
		
		post coef (`yr') (`b_f') (`se_f') (`b_e') (`se_e') (`b_emp') (`se_emp')
	restore
}
postclose coef
use `coefstore', clear

gen ub_f = beta_firms + 1.96*se_firms
gen lb_f = beta_firms - 1.96*se_firms
twoway (rcap ub_f lb_f year, lcolor(black)) (line beta_firms year, lwidth(medthick)), yline(0, lpattern(dash)) xtitle("Year") ytitle("Coefficient on Log Funding") title("Cross-Sectional Effect on Log Firms - Science Industry")
graph export "`path'/Outputs/Tables/Science/cross_sec/graphs/firms.pdf", replace

gen ub_e = beta_estabs + 1.96*se_estabs
gen lb_e = beta_estabs - 1.96*se_estabs
twoway (rcap ub_e lb_e year, lcolor(black)) (line beta_estabs year, lwidth(medthick)), yline(0, lpattern(dash)) xtitle("Year") ytitle("Coefficient on Log Funding") title("Cross-Sectional Effect on Log Establishments - Science Industry")
graph export "`path'/Outputs/Tables/Science/cross_sec/graphs/estabs.pdf", replace

gen ub_emp = beta_emp + 1.96*se_emp
gen lb_emp = beta_emp - 1.96*se_emp
twoway (rcap ub_emp lb_emp year, lcolor(black)) (line beta_emp year, lwidth(medthick)), yline(0, lpattern(dash)) xtitle("Year") ytitle("Coefficient on Log Funding") title("Cross-Sectional Effect on Log Employment - Science Industry")
graph export "`path'/Outputs/Tables/Science/cross_sec/graphs/emp.pdf", replace

*****
/*
esttab f1992 f1993 f1994 f1995 f1996 f1997 f1998 f1999 f2000 f2001 f2002 f2003 f2004 f2005 f2006 f2007 f2008 f2009 using "`path'/Outputs/Tables/Health/cross_sec/cross_sec_firms.csv", label replace se mtitles("1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009") coeflabels(ln_funding "Log NIH Funding" ln_pop "Log Population" income_per_cap "Income per Capita (thousands)" college "College Educated (millions)") drop(_cons)

esttab e1992 e1993 e1994 e1995 e1996 e1997 e1998 e1999 e2000 e2001 e2002 e2003 e2004 e2005 e2006 e2007 e2008 e2009 using "`path'/Outputs/Tables/Health/cross_sec/cross_sec_estabs.csv", label replace se mtitles("1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009") coeflabels(ln_funding "Log NIH Funding" ln_pop "Log Population" income_per_cap "Income per Capita (thousands)" college "College Educated (millions)") drop(_cons)

esttab emp1992 emp1993 emp1994 emp1995 emp1996 emp1997 emp1998 emp1999 emp2000 emp2001 emp2002 emp2003 emp2004 emp2005 emp2006 emp2007 emp2008 emp2009 using "`path'/Outputs/Tables/Health/cross_sec/cross_sec_emp.csv", label replace se mtitles("1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009") coeflabels(ln_funding "Log NIH Funding" ln_pop "Log Population" income_per_cap "Income per Capita (thousands)" college "College Educated (millions)") drop(_cons)
*/

***************************** HEALTH ******************************
import delimited "`path'/Data/NIH_v4/Use/nih_health.csv", clear
save "`path'/Data/NIH_v4/Use/nih_health.dta", replace

use "`path'/Data/NIH_v4/Use/nih_health.dta", clear
* for table display purposes, will divide income percap by 1000 and college by 1mill
replace income_per_cap = income_per_cap / 1000
replace college = college / 1000000
save "`path'/Data/NIH_v4/Regress/cross_sec.dta", replace
* 2/19/26
*** Cross section on all years, with no lags
use "`path'/Data/NIH_v4/Regress/cross_sec.dta", clear

tempfile coefstore
postfile coef year beta_firms se_firms beta_estabs se_estabs beta_emp se_emp using `coefstore', replace
				 
forvalues yr = 1992(1)2009 {
	display `yr'
	preserve
		keep if year == `yr'
		eststo f`yr': reg ln_firms ln_funding ln_pop income_per_cap college, robust
		local b_f = _b[ln_funding]
        local se_f = _se[ln_funding]
		
		eststo e`yr': reg ln_estabs ln_funding ln_pop income_per_cap college, robust
		local b_e = _b[ln_funding]
        local se_e = _se[ln_funding]
		
		eststo emp`yr': reg ln_emp ln_funding ln_pop income_per_cap college, robust
		local b_emp = _b[ln_funding]
        local se_emp = _se[ln_funding]
		
		post coef (`yr') (`b_f') (`se_f') (`b_e') (`se_e') (`b_emp') (`se_emp')
	restore
}
postclose coef
use `coefstore', clear

gen ub_f = beta_firms + 1.96*se_firms
gen lb_f = beta_firms - 1.96*se_firms
twoway (rcap ub_f lb_f year, lcolor(black)) (line beta_firms year, lwidth(medthick)), yline(0, lpattern(dash)) xtitle("Year") ytitle("Coefficient on Log Funding") title("Cross-Sectional Effect on Log Firms - Health Industry")
graph export "`path'/Outputs/Tables/Health/cross_sec/graphs/firms.pdf", replace

gen ub_e = beta_estabs + 1.96*se_estabs
gen lb_e = beta_estabs - 1.96*se_estabs
twoway (rcap ub_e lb_e year, lcolor(black)) (line beta_estabs year, lwidth(medthick)), yline(0, lpattern(dash)) xtitle("Year") ytitle("Coefficient on Log Funding") title("Cross-Sectional Effect on Log Establishments - Health Industry")
graph export "`path'/Outputs/Tables/Health/cross_sec/graphs/estabs.pdf", replace

gen ub_emp = beta_emp + 1.96*se_emp
gen lb_emp = beta_emp - 1.96*se_emp
twoway (rcap ub_emp lb_emp year, lcolor(black)) (line beta_emp year, lwidth(medthick)), yline(0, lpattern(dash)) xtitle("Year") ytitle("Coefficient on Log Funding") title("Cross-Sectional Effect on Log Employment - Health Industry")
graph export "`path'/Outputs/Tables/Health/cross_sec/graphs/emp.pdf", replace

*****

esttab f1992 f1993 f1994 f1995 f1996 f1997 f1998 f1999 f2000 f2001 f2002 f2003 f2004 f2005 f2006 f2007 f2008 f2009 using "`path'/Outputs/Tables/Health/cross_sec/cross_sec_firms.csv", label replace se mtitles("1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009") coeflabels(ln_funding "Log NIH Funding" ln_pop "Log Population" income_per_cap "Income per Capita (thousands)" college "College Educated (millions)") drop(_cons)

esttab e1992 e1993 e1994 e1995 e1996 e1997 e1998 e1999 e2000 e2001 e2002 e2003 e2004 e2005 e2006 e2007 e2008 e2009 using "`path'/Outputs/Tables/Health/cross_sec/cross_sec_estabs.csv", label replace se mtitles("1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009") coeflabels(ln_funding "Log NIH Funding" ln_pop "Log Population" income_per_cap "Income per Capita (thousands)" college "College Educated (millions)") drop(_cons)

esttab emp1992 emp1993 emp1994 emp1995 emp1996 emp1997 emp1998 emp1999 emp2000 emp2001 emp2002 emp2003 emp2004 emp2005 emp2006 emp2007 emp2008 emp2009 using "`path'/Outputs/Tables/Health/cross_sec/cross_sec_emp.csv", label replace se mtitles("1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009") coeflabels(ln_funding "Log NIH Funding" ln_pop "Log Population" income_per_cap "Income per Capita (thousands)" college "College Educated (millions)") drop(_cons)


*** Cross section with lags
use "`path'/Data/NIH_v4/Regress/cross_sec.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L.ln_funding
gen lag_ln_pop = L.ln_pop
gen lag_income_per_cap = L.income_per_cap
gen lag_college = L.college

forvalues yr = 1993(1)2009 {
	display `yr'
	preserve
		keep if year == `yr'
		eststo f`yr': reg ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, robust
		eststo e`yr': reg ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, robust
		eststo emp`yr': reg ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, robust
	restore
}

esttab f1993 f1994 f1995 f1996 f1997 f1998 f1999 f2000 f2001 f2002 f2003 f2004 f2005 f2006 f2007 f2008 f2009 using "`path'/Outputs/Tables/Health/cross_sec/cross_sec_firms_lag1.csv", label replace se mtitles("1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)" lag_income_per_cap "Income per Capita (t-1, thousands)" lag_college "College Educated (t-1, millions)") drop(_cons)

esttab e1993 e1994 e1995 e1996 e1997 e1998 e1999 e2000 e2001 e2002 e2003 e2004 e2005 e2006 e2007 e2008 e2009 using "`path'/Outputs/Tables/Health/cross_sec/cross_sec_estabs_lag1.csv", label replace se mtitles("1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)" lag_income_per_cap "Income per Capita (t-1, thousands)" lag_college "College Educated (t-1, millions)") drop(_cons)

esttab emp1993 emp1994 emp1995 emp1996 emp1997 emp1998 emp1999 emp2000 emp2001 emp2002 emp2003 emp2004 emp2005 emp2006 emp2007 emp2008 emp2009 using "`path'/Outputs/Tables/Health/cross_sec/cross_sec_emp_lag1.csv", label replace se mtitles("1992" "1993" "1994" "1995" "1996" "1997" "1998" "1999" "2000" "2001" "2002" "2003" "2004" "2005" "2006" "2007" "2008" "2009") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)" lag_income_per_cap "Income per Capita (t-1, thousands)" lag_college "College Educated (t-1, millions)") drop(_cons)



***************
* 1995
use "`path'/Data/NIH_Outcomes/cross_sec.dta",  clear
keep if year == 1995
* pop, income, bachelors
eststo f95: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo e95: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo emp95: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg, robust

* 2000
use "`path'/Data/NIH_Outcomes/cross_sec.dta",  clear
keep if year == 2000
eststo f00: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo e00: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo emp00: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg, robust

* 2005
use "`path'/Data/NIH_Outcomes/cross_sec.dta",  clear
keep if year == 2005
eststo f05: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo e05: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo emp05: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg, robust

* 2010
use "`path'/Data/NIH_Outcomes/cross_sec.dta",  clear
keep if year == 2010
eststo f10: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo e10: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo emp10: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg, robust

* 2015
use "`path'/Data/NIH_Outcomes/cross_sec.dta",  clear
keep if year == 2015
eststo f15: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo e15: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo emp15: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg, robust

* 2020
use "`path'/Data/NIH_Outcomes/cross_sec.dta",  clear
keep if year == 2020
eststo f20: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo e20: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg, robust
eststo emp20: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg, robust

esttab f95 f00 f05 f10 f15 f20 using `path'/Outputs/Tables/Indus_health/cross_sec_firms.tex, label replace se mtitles("1995" "2000" "2005" "2010" "2015" "2020") coeflabels(ln_funding "Log NIH Funding" ln_pop "Log Population" income_per_cap "Income per Capita" bachelors_deg "College Educated (count)") drop(_cons)

esttab e95 e00 e05 e10 e15 e20 using `path'/Outputs/Tables/Indus_health/cross_sec_estabs.tex, label replace se mtitles("1995" "2000" "2005" "2010" "2015" "2020") coeflabels(ln_funding "Log NIH Funding" ln_pop "Log Population" income_per_cap "Income per Capita" bachelors_deg "College Educated (count)") drop(_cons)

esttab emp95 emp00 emp05 emp10 emp15 emp20 using `path'/Outputs/Tables/Indus_health/cross_sec_emp.tex, label replace se mtitles("1995" "2000" "2005" "2010" "2015" "2020") coeflabels(ln_funding "Log NIH Funding" ln_pop "Log Population" income_per_cap "Income per Capita" bachelors_deg "College Educated (count)") drop(_cons)



// esttab f95 f00 f05 f10 f15 f20 using "`path'/Outputs/Tables/Indus_educ/cross_sec_firms.csv", se replace
// esttab e95 e00 e05 e10 e15 e20 using "`path'/Outputs/Tables/Indus_educ/cross_sec_estabs.csv", se replace
// esttab emp95 emp00 emp05 emp10 emp15 emp20 using "`path'/Outputs/Tables/Indus_educ/cross_sec_emp.csv", se replace

// * pop, income, bachelors, graduate
// eststo f95: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo e95: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo emp95: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust

// * pop, income, bachelors, graduate
// eststo f00: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo e00: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo emp00: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust

// * pop, income, bachelors, graduate
// eststo f05: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo e05: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo emp05: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust

// * pop, income, bachelors, graduate
// eststo f10: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo e10: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo emp10: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust


// * pop, income, bachelors, graduate
// eststo f15: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo e15: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo emp15: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust

// * pop, income, bachelors, graduate
// eststo f20: reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo e20: reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
// eststo emp20: reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg graduate_deg, robust
