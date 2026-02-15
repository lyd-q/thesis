local path "/Users/lydia/Desktop/Thesis"
ssc install estout
use "`path'/Data/NIH_Outcomes/sector/nih_health.dta", clear
save "`path'/Data/NIH_Outcomes/cross_sec.dta", replace

***************
* Cross section with no lags
* 1995
use "`path'/Data/NIH_Outcomes/cross_sec.dta",  clear

forvalues yr = 1992(1)2022 {
	display 'year '
	eststo f`yr': reg ln_firms ln_funding ln_pop income_per_cap bachelors_deg, robust
	eststo e`yr': reg ln_estabs ln_funding ln_pop income_per_cap bachelors_deg, robust
	eststo emp`yr': reg ln_emp ln_funding ln_pop income_per_cap bachelors_deg, robust	
}




* Cross section with lags




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
