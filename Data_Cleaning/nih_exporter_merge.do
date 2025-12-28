
local path "/Users/lydia/Desktop/Thesis"




use "`path'/Data/Working/nih_counties.dta", clear
rename county cnty
rename state st
* fix Rockville, MD
replace cnty = 24031 if city == "ROCKVILLE"
merge m:1 cnty using "`path'/Data/Crosswalks/county_msa_map.dta"
preserve
	keep if _m == 1
	drop _m
	save "`path'/Data/nih_msa_unmatched.dta", replace
restore
keep if _m == 3
drop _m
save "`path'/Data/nih_msa.dta", replace


	*** Fix unmatched - mostly Colorado, Miami FL, and Maryland
use "`path'/Data/nih_msa_unmatched.dta", clear
keep county_name st cnty msan pmsan
duplicates drop
save "`path'/Data/nih_msa_manual.dta", replace
* (1) manually add in msa and msan, and merge with msa location info
clear
import excel "`path'/Data/Manual/county_msa_2009.xlsx", firstrow
merge 1:m msan pmsan using "`path'/Data/Crosswalks/county_msa_map.dta"
keep if _m == 3
keep if cntyn == "Denver CO" | cntyn == "Dade FL" 
drop _m
save "`path'/Data/nih_msa_manual.dta", replace

* (3) merge locations with unmatched data observations
use "`path'/Data/nih_msa_unmatched.dta", clear
merge m:1 county_name st cnty using "`path'/Data/nih_msa_manual.dta"
keep if _m == 3
drop _m
save "`path'/Data/nih_msa_manual_matched.dta", replace

* (4) append to automatic matches
use "`path'/Data/nih_msa.dta", clear
append using "`path'/Data/nih_msa_manual_matched.dta", force
drop if msa == . | msa == 9999
save "`path'/Data/nih_msa.dta", replace


***************************************************
	*** Using Exporter Data
***************************************************
forvalues year = 1992(1)2024{
	clear
	import delimited "`path'/Raw_data/NIH Exporter/RePORTER_PRJ_C_FY`year'.csv", clear
	gen year = 	`year'
	describe
	save "`path'/Data/NIH_v2/nih_exporter_`year'.dta", replace
}

use "`path'/Data/NIH_v2/nih_exporter_1992.dta", clear
forvalues year = 1992(1)2024 {
	append using "`path'/Data/NIH_v2/nih_exporter_`year'.dta", force
	erase "`path'/Data/NIH_v2/nih_exporter_`year'.dta"
	save "`path'/Data/NIH_v2/nih_exporter.dta", replace
}



***************************************************
	*** Get Science Field
***************************************************

use "`path'/Data/NIH_v2/nih_exporter.dta", clear
rename full_project_num PROJECTNUMBER
drop if org_dept == ""
duplicates drop PROJECTNUMBER org_dept, force
save "`path'/Data/NIH_v2/nih_departments.dta", replace

* There are a few duplicates (2-240, 3-24, 5-5) but not that many relative to overall (singles-1332791), so I will just keep one with highest direct cost

use "`path'/Data/NIH_v2/nih_departments.dta", clear
gsort PROJECTNUMBER -direct_cost_amt
by PROJECTNUMBER: gen rank = _n
keep if rank == 1
drop rank
keep PROJECTNUMBER org_dept
save "`path'/Data/NIH_v2/nih_departments.dta", replace


***************************************************
	*** Get Dun and Bradstreet number
***************************************************
use "`path'/Data/NIH_v2/nih_exporter.dta", clear
rename full_project_num PROJECTNUMBER
keep PROJECTNUMBER org_name org_duns
keep if org_duns != ""
duplicates drop
duplicates drop PROJECTNUMBER org_name, force //only applies to one observation "SRI INTERNATIONAL"
rename org_name ORGANIZATIONNAME
save "`path'/Data/NIH_v2/nih_DUN.dta", replace

