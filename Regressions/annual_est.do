local path "/Users/lydia/Desktop/Thesis"
ssc install estout
ssc install require
ssc install reghdfe


***********************************************************
02/20/26
***********************************************************
	*** Annual Estimates -- 10 year period -- With Controls
************************************************************
	*** HEALTH
import delimited "`path'/Data/NIH_v4/Use/nih_health.csv", clear
save "`path'/Data/NIH_v4/Use/nih_health.dta", replace

use "`path'/Data/NIH_v4/Use/nih_health.dta", clear
replace income_per_cap = income_per_cap / 1000
replace college = college / 1000000
save "`path'/Data/NIH_v4/Regress/annual_est.dta", replace

* 1 lag
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L.ln_funding
gen lag_ln_pop = L.ln_pop
gen lag_income_per_cap = L.income_per_cap
gen lag_college = L.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/annual_est_health_lag1.csv", label replace se title("Estimations of Regional Economic Activity and NIH Funding (1-year lag) - Health") mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)" lag_income_per_cap "Income per Capita (t-1, thousands)" lag_college "College Educated (t-1, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/annual_est_health_lag1.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)" lag_income_per_cap "Income per Capita (t-1, thousands)" lag_college "College Educated (t-1, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)
* This is same as: xtreg ln_firms L1.ln_funding L1.income_per_cap L1.college i.year, fe absorb(cbsa_code) vce(cluster cbsa_code) 

* 2 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L2.ln_funding
gen lag_ln_pop = L2.ln_pop
gen lag_income_per_cap = L2.income_per_cap
gen lag_college = L2.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/annual_est_health_lag2.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)" lag_ln_pop "Log Population (t-2)" lag_income_per_cap "Income per Capita (t-2, thousands)" lag_college "College Educated (t-2, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/annual_est_health_lag2.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)" lag_ln_pop "Log Population (t-2)" lag_income_per_cap "Income per Capita (t-2, thousands)" lag_college "College Educated (t-2, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 3 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L3.ln_funding
gen lag_ln_pop = L3.ln_pop
gen lag_income_per_cap = L3.income_per_cap
gen lag_college = L3.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/annual_est_health_lag3.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)" lag_ln_pop "Log Population (t-3)" lag_income_per_cap "Income per Capita (t-3, thousands)" lag_college "College Educated (t-3, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/annual_est_health_lag3.tex", label replace se  title("Estimations of Regional Economic Activity and NIH Funding (3-year lag) - Health") mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)" lag_ln_pop "Log Population (t-3)" lag_income_per_cap "Income per Capita (t-3, thousands)" lag_college "College Educated (t-3, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 4 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L4.ln_funding
gen lag_ln_pop = L4.ln_pop
gen lag_income_per_cap = L4.income_per_cap
gen lag_college = L4.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/annual_est_health_lag4.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)" lag_ln_pop "Log Population (t-4)" lag_income_per_cap "Income per Capita (t-4, thousands)" lag_college "College Educated (t-4, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/annual_est_health_lag4.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)" lag_ln_pop "Log Population (t-4)" lag_income_per_cap "Income per Capita (t-4, thousands)" lag_college "College Educated (t-4, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)


* 5 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L5.ln_funding
gen lag_ln_pop = L5.ln_pop
gen lag_income_per_cap = L5.income_per_cap
gen lag_college = L5.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/annual_est_health_lag5.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)" lag_ln_pop "Log Population (t-5)" lag_income_per_cap "Income per Capita (t-5, thousands)" lag_college "College Educated (t-5, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/annual_est_health_lag5.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)" lag_ln_pop "Log Population (t-5)" lag_income_per_cap "Income per Capita (t-5, thousands)" lag_college "College Educated (t-5, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)


************************************************************
	*** SCIENCE
import delimited "`path'/Data/NIH_v4/Use/nih_science.csv", clear
save "`path'/Data/NIH_v4/Use/nih_science.dta", replace

use "`path'/Data/NIH_v4/Use/nih_science.dta", clear
replace income_per_cap = income_per_cap / 1000
replace college = college / 1000000
save "`path'/Data/NIH_v4/Regress/annual_est.dta", replace

* 1 lag
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L.ln_funding
gen lag_ln_pop = L.ln_pop
gen lag_income_per_cap = L.income_per_cap
gen lag_college = L.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/annual_est_science_lag1.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)" lag_income_per_cap "Income per Capita (t-1, thousands)" lag_college "College Educated (t-1, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/annual_est_science_lag1.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)" lag_income_per_cap "Income per Capita (t-1, thousands)" lag_college "College Educated (t-1, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)
* This is same as: xtreg ln_firms L1.ln_funding L1.income_per_cap L1.college i.year, fe absorb(cbsa_code) vce(cluster cbsa_code) 

* 2 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L2.ln_funding
gen lag_ln_pop = L2.ln_pop
gen lag_income_per_cap = L2.income_per_cap
gen lag_college = L2.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/annual_est_science_lag2.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)" lag_ln_pop "Log Population (t-2)" lag_income_per_cap "Income per Capita (t-2, thousands)" lag_college "College Educated (t-2, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/annual_est_science_lag2.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)" lag_ln_pop "Log Population (t-2)" lag_income_per_cap "Income per Capita (t-2, thousands)" lag_college "College Educated (t-2, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 3 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L3.ln_funding
gen lag_ln_pop = L3.ln_pop
gen lag_income_per_cap = L3.income_per_cap
gen lag_college = L3.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/annual_est_science_lag3.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)" lag_ln_pop "Log Population (t-3)" lag_income_per_cap "Income per Capita (t-3, thousands)" lag_college "College Educated (t-3, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/annual_est_science_lag3.tex", label replace se  title("Estimations of Regional Economic Activity and NIH Funding (3-year lag) - Health") mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)" lag_ln_pop "Log Population (t-3)" lag_income_per_cap "Income per Capita (t-3, thousands)" lag_college "College Educated (t-3, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 4 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L4.ln_funding
gen lag_ln_pop = L4.ln_pop
gen lag_income_per_cap = L4.income_per_cap
gen lag_college = L4.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/annual_est_science_lag4.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)" lag_ln_pop "Log Population (t-4)" lag_income_per_cap "Income per Capita (t-4, thousands)" lag_college "College Educated (t-4, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/annual_est_science_lag4.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)" lag_ln_pop "Log Population (t-4)" lag_income_per_cap "Income per Capita (t-4, thousands)" lag_college "College Educated (t-4, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)


* 5 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L5.ln_funding
gen lag_ln_pop = L5.ln_pop
gen lag_income_per_cap = L5.income_per_cap
gen lag_college = L5.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop lag_income_per_cap lag_college, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/annual_est_science_lag5.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)" lag_ln_pop "Log Population (t-5)" lag_income_per_cap "Income per Capita (t-5, thousands)" lag_college "College Educated (t-5, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/annual_est_science_lag5.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)" lag_ln_pop "Log Population (t-5)" lag_income_per_cap "Income per Capita (t-5, thousands)" lag_college "College Educated (t-5, millions)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)






***********************************************************
	*** Annual Estimates -- 10 year period -- With Population
************************************************************
	*** HEALTH
import delimited "`path'/Data/NIH_v4/Use/nih_health.csv", clear
save "`path'/Data/NIH_v4/Use/nih_health.dta", replace

use "`path'/Data/NIH_v4/Use/nih_health.dta", clear
replace income_per_cap = income_per_cap / 1000
replace college = college / 1000000
save "`path'/Data/NIH_v4/Regress/annual_est.dta", replace

* 1 lag
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L.ln_funding
gen lag_ln_pop = L.ln_pop
gen lag_income_per_cap = L.income_per_cap
gen lag_college = L.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/pop_controls/annual_est_health_lag1.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/pop_controls/annual_est_health_lag1.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 2 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L2.ln_funding
gen lag_ln_pop = L2.ln_pop
gen lag_income_per_cap = L2.income_per_cap
gen lag_college = L2.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/pop_controls/annual_est_health_lag2.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)" lag_ln_pop "Log Population (t-2)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/pop_controls/annual_est_health_lag2.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)" lag_ln_pop "Log Population (t-2)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 3 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L3.ln_funding
gen lag_ln_pop = L3.ln_pop
gen lag_income_per_cap = L3.income_per_cap
gen lag_college = L3.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/pop_controls/annual_est_health_lag3.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)" lag_ln_pop "Log Population (t-3)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/pop_controls/annual_est_health_lag3.tex", label replace se  title("Estimations of Regional Economic Activity and NIH Funding (3-year lag) - Health") mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)" lag_ln_pop "Log Population (t-3)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 4 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L4.ln_funding
gen lag_ln_pop = L4.ln_pop
gen lag_income_per_cap = L4.income_per_cap
gen lag_college = L4.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/pop_controls/annual_est_health_lag4.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)" lag_ln_pop "Log Population (t-4)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/pop_controls/annual_est_health_lag4.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)" lag_ln_pop "Log Population (t-4)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)


* 5 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L5.ln_funding
gen lag_ln_pop = L5.ln_pop
gen lag_income_per_cap = L5.income_per_cap
gen lag_college = L5.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/pop_controls/annual_est_health_lag5.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)" lag_ln_pop "Log Population (t-5)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/pop_controls/annual_est_health_lag5.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)" lag_ln_pop "Log Population (t-5)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)


************************************************************
	*** SCIENCE
import delimited "`path'/Data/NIH_v4/Use/nih_science.csv", clear
save "`path'/Data/NIH_v4/Use/nih_science.dta", replace

use "`path'/Data/NIH_v4/Use/nih_science.dta", clear
replace income_per_cap = income_per_cap / 1000
replace college = college / 1000000
save "`path'/Data/NIH_v4/Regress/annual_est.dta", replace

* 1 lag
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L.ln_funding
gen lag_ln_pop = L.ln_pop
gen lag_income_per_cap = L.income_per_cap
gen lag_college = L.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/pop_controls/annual_est_science_lag1.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/pop_controls/annual_est_science_lag1.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)" lag_ln_pop "Log Population (t-1)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)
* This is same as: xtreg ln_firms L1.ln_funding L1.income_per_cap L1.college i.year, fe absorb(cbsa_code) vce(cluster cbsa_code) 

* 2 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L2.ln_funding
gen lag_ln_pop = L2.ln_pop
gen lag_income_per_cap = L2.income_per_cap
gen lag_college = L2.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/pop_controls/annual_est_science_lag2.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)" lag_ln_pop "Log Population (t-2)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/pop_controls/annual_est_science_lag2.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)" lag_ln_pop "Log Population (t-2)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 3 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L3.ln_funding
gen lag_ln_pop = L3.ln_pop
gen lag_income_per_cap = L3.income_per_cap
gen lag_college = L3.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/pop_controls/annual_est_science_lag3.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)" lag_ln_pop "Log Population (t-3)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/pop_controls/annual_est_science_lag3.tex", label replace se  title("Estimations of Regional Economic Activity and NIH Funding (3-year lag) - Health") mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)" lag_ln_pop "Log Population (t-3)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 4 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L4.ln_funding
gen lag_ln_pop = L4.ln_pop
gen lag_income_per_cap = L4.income_per_cap
gen lag_college = L4.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/pop_controls/annual_est_science_lag4.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)" lag_ln_pop "Log Population (t-4)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/pop_controls/annual_est_science_lag4.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)" lag_ln_pop "Log Population (t-4)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)


* 5 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L5.ln_funding
gen lag_ln_pop = L5.ln_pop
gen lag_income_per_cap = L5.income_per_cap
gen lag_college = L5.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding lag_ln_pop, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/pop_controls/annual_est_science_lag5.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)" lag_ln_pop "Log Population (t-5)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/pop_controls/annual_est_science_lag5.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)" lag_ln_pop "Log Population (t-5)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)


***********************************************************
	*** Annual Estimates -- 10 year period -- NO Controls
************************************************************
	*** HEALTH
import delimited "`path'/Data/NIH_v4/Use/nih_health.csv", clear
save "`path'/Data/NIH_v4/Use/nih_health.dta", replace

use "`path'/Data/NIH_v4/Use/nih_health.dta", clear
replace income_per_cap = income_per_cap / 1000
replace college = college / 1000000
save "`path'/Data/NIH_v4/Regress/annual_est.dta", replace

* 1 lag
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L.ln_funding
gen lag_ln_pop = L.ln_pop
gen lag_income_per_cap = L.income_per_cap
gen lag_college = L.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/no_controls/annual_est_health_lag1.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/no_controls/annual_est_health_lag1.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 2 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L2.ln_funding
gen lag_ln_pop = L2.ln_pop
gen lag_income_per_cap = L2.income_per_cap
gen lag_college = L2.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/no_controls/annual_est_health_lag2.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/no_controls/annual_est_health_lag2.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 3 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L3.ln_funding
gen lag_ln_pop = L3.ln_pop
gen lag_income_per_cap = L3.income_per_cap
gen lag_college = L3.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/no_controls/annual_est_health_lag3.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/no_controls/annual_est_health_lag3.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 4 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L4.ln_funding
gen lag_ln_pop = L4.ln_pop
gen lag_income_per_cap = L4.income_per_cap
gen lag_college = L4.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/no_controls/annual_est_health_lag4.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/no_controls/annual_est_health_lag4.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)


* 5 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L5.ln_funding
gen lag_ln_pop = L5.ln_pop
gen lag_income_per_cap = L5.income_per_cap
gen lag_college = L5.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/no_controls/annual_est_health_lag5.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Health/annual_est/no_controls/annual_est_health_lag5.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)


************************************************************
	*** SCIENCE
import delimited "`path'/Data/NIH_v4/Use/nih_science.csv", clear
save "`path'/Data/NIH_v4/Use/nih_science.dta", replace

use "`path'/Data/NIH_v4/Use/nih_science.dta", clear
replace income_per_cap = income_per_cap / 1000
replace college = college / 1000000
save "`path'/Data/NIH_v4/Regress/annual_est.dta", replace

* 1 lag
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L.ln_funding
gen lag_ln_pop = L.ln_pop
gen lag_income_per_cap = L.income_per_cap
gen lag_college = L.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/no_controls/annual_est_science_lag1.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/no_controls/annual_est_science_lag1.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-1)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)
* This is same as: xtreg ln_firms L1.ln_funding L1.income_per_cap L1.college i.year, fe absorb(cbsa_code) vce(cluster cbsa_code) 

* 2 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L2.ln_funding
gen lag_ln_pop = L2.ln_pop
gen lag_income_per_cap = L2.income_per_cap
gen lag_college = L2.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/no_controls/annual_est_science_lag2.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/no_controls/annual_est_science_lag2.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-2)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 3 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L3.ln_funding
gen lag_ln_pop = L3.ln_pop
gen lag_income_per_cap = L3.income_per_cap
gen lag_college = L3.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/no_controls/annual_est_science_lag3.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/no_controls/annual_est_science_lag3.tex", label replace se  mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-3)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

* 4 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L4.ln_funding
gen lag_ln_pop = L4.ln_pop
gen lag_income_per_cap = L4.income_per_cap
gen lag_college = L4.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/no_controls/annual_est_science_lag4.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/no_controls/annual_est_science_lag4.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-4)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)


* 5 lags
use "`path'/Data/NIH_v4/Regress/annual_est.dta", clear
xtset cbsa_code year
gen lag_ln_funding = L5.ln_funding
gen lag_ln_pop = L5.ln_pop
gen lag_income_per_cap = L5.income_per_cap
gen lag_college = L5.college
keep if year >= 1999 & year <= 2008

eststo m1: reghdfe ln_firms lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m2: reghdfe ln_estabs lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

eststo m3: reghdfe ln_emp lag_ln_funding, absorb(cbsa_code year) vce(cluster cbsa_code)
estadd local fe_entity "Yes", replace
estadd local fe_time "Yes", replace

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/no_controls/annual_est_science_lag5.csv", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

esttab m1 m2 m3 using "`path'/Outputs/Tables/Science/annual_est/no_controls/annual_est_science_lag5.tex", label replace se mtitles("Log Firms" "Log Estabs" "Log Empl") coeflabels(lag_ln_funding "Log NIH Funding (t-5)") s(fe_entity fe_time N, label("MSA FE" "Year FE" "Observations")) drop(_cons)

