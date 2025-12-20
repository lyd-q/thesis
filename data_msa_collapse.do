
local path "/Users/lydia/Desktop/Thesis"
log using "`path'/Log/data_clean.log"

***************************************************************
	*** Prepare geography crosswalks
	
* cities to county
clear
import delimited "`path'/Data/Crosswalks/city_county_map.csv"
replace city = strupper(city)
duplicates drop
save "`path'/Data/Crosswalks/city_county_map.dta", replace

* county to MSA
clear
import delimited "`path'/Data/Crosswalks/county_2009_sort.csv"
duplicates drop
save "`path'/Data/Crosswalks/county_msa_map.dta", replace

*** Get state abbreviations list
/*
use "`path'/Data/Crosswalks/city_county_map.dta", clear
drop city county county_name
duplicates drop state, force
sort state
save "`path'/Data/Crosswalks/states.dta", replace
*/

clear
import excel "`path'/Data/Crosswalks/state_abbrev.xlsx", firstrow
replace state_fullname = strupper(state_fullname)
save `path'/Data/Crosswalks/state_abbrev.dta, replace


***************************************************************
			*** CLEANING FOR GEOGRAPHY COLLAPSE ****
***************************************************************
	
	*** Clean city and state names 
use "`path'/Data/nih_raw.dta", clear
replace CITY = strtrim(CITY)
replace CITY = strupper(CITY)
replace STATEORCOUNTRYNAME = strtrim(STATEORCOUNTRYNAME)
replace STATEORCOUNTRYNAME = strupper(STATEORCOUNTRYNAME)
save "`path'/Data/nih_raw.dta", replace

***************************************************************
	*** fix exception cases where state_fullname == "NULL"
	* mainly in years 2009, and 1992-98
use "`path'/Data/nih_raw.dta", clear
keep if STATEORCOUNTRYNAME == "NULL" | STATEORCOUNTRYNAME == ""
save "`path'/Data/Cleaning/nih_raw_null.dta", replace
collapse (sum) FUNDING, by(CITY STATEORCOUNTRYNAME)
sort STATEORCOUNTRYNAME CITY
save "`path'/Data/Cleaning/nih_locationlist_null.dta", replace

* import manual city matches
clear
import excel "`path'/Data/Manual/null_states.xlsx", sheet(v2) firstrow
duplicates drop
save "`path'/Data/Cleaning/null_states.dta", replace

use "`path'/Data/Cleaning/nih_locationlist_null.dta", clear
drop STATEORCOUNTRYNAME
collapse (sum) FUNDING, by(CITY)
merge m:1 CITY using "`path'/Data/Cleaning/null_states.dta"
drop _m
keep CITY STATEORCOUNTRYNAME
keep if STATEORCOUNTRYNAME != ""
save "`path'/Data/Cleaning/nih_locationlist_null.dta", replace

use "`path'/Data/Cleaning/nih_raw_null.dta", clear
drop STATEORCOUNTRYNAME
merge  m:1 CITY using "`path'/Data/Cleaning/nih_locationlist_null.dta"
keep if _m == 3
drop _m
save "`path'/Data/Cleaning/nih_null.dta", replace

	*** Add back into raw data
use "`path'/Data/nih_raw.dta", clear
drop if STATEORCOUNTRYNAME == "NULL" | STATEORCOUNTRYNAME == ""
append using "`path'/Data/Cleaning/nih_null.dta", force
save "`path'/Data/nih_US.dta", replace

**************************************************************

	*** Merge state abbreviations and drop non-US
/*
* work with locations list first, then merge later
use "`path'/Data/nih_US.dta", clear
keep CITY STATEORCOUNTRYNAME
duplicates drop
sort STATEORCOUNTRYNAME CITY
save "`path'/Data/Cleaning/nih_locationlist.dta", replace

use "`path'/Data/Cleaning/nih_locationlist.dta", clear
rename STATEORCOUNTRYNAME state_fullname
merge m:1 state_fullname using "`path'/Data/Crosswalks/state_abbrev.dta"
sort _m state_fullname
* only keep US (those with matched states)
keep if _m == 3
drop _m
save "`path'/Data/Cleaning/nih_locationlist.dta", replace

	*** City to County merge
use "`path'/Data/Cleaning/nih_locationlist.dta", clear
rename CITY city
rename state_abbrev state
merge m:1 city state using "`path'/Data/Crosswalks/city_county_map.dta"
save "`path'/Data/Cleaning/nih_locationlist.dta", replace
*/


* full dataset
use "`path'/Data/nih_US.dta", clear
rename STATEORCOUNTRYNAME state_fullname
merge m:1 state_fullname using "`path'/Data/Crosswalks/state_abbrev.dta"
sort _m state_fullname
* only keep US (those with matched states)
keep if _m == 3
drop _m
rename CITY city
rename state_abbrev state
merge m:1 city state using "`path'/Data/Crosswalks/city_county_map.dta"
preserve
	keep if _m == 1
	drop _m
	save "`path'/Data/Cleaning/nih_county_unmatched_raw.dta", replace
	keep city state_fullname FUNDING state county county_name
	collapse (sum) FUNDING, by(city state_fullname state county county_name)
	save "`path'/Data/Cleaning/nih_county_unmatched.dta", replace
restore
keep if _m == 3
drop _m
replace county = 24031 if city == "ROCKVILLE"
save "`path'/Data/nih_counties.dta", replace
// matched:  1,727,614; not matched: 55,711 = 25%
// manually match these counties

clear
import excel "`path'/Data/Manual/null_states.xlsx", sheet(city_county_null) firstrow
save "`path'/Data/Cleaning/nih_cities_unmatched.dta", replace

use "`path'/Data/Cleaning/nih_county_unmatched_raw.dta", clear
merge m:1 city state using "`path'/Data/Cleaning/nih_cities_unmatched.dta"
save "`path'/Data/Cleaning/nih_cities_unmatched_manual.dta", replace
// matched: 54,899; not matched: 1,026 (pretty good!)

use "`path'/Data/nih_counties.dta", clear
append using "`path'/Data/Cleaning/nih_cities_unmatched_manual.dta", force
save "`path'/Data/nih_counties.dta", replace
//num observations: 1,783,948

************************************************************
	*** County to MSA with 2009 crosswalk
************************************************************
/*
use "`path'/Data/nih_counties.dta", clear
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
*/

************************************************************
	*** County to MSA with 2003 crosswalk
************************************************************
clear
import excel "`path'/Data/Crosswalks/county_msa_xwalk_2003.xlsx", firstrow
duplicates drop
destring county_fips, replace
save "`path'/Data/Crosswalks/county_cbsa_xwalk.dta", replace

use "`path'/Data/nih_counties.dta", clear

rename county county_fips
merge m:1 county_fips using "`path'/Data/Crosswalks/county_cbsa_xwalk.dta"
* keep unmatched
preserve 
	keep if _m == 1
	save "`path'/Data/county_cbsa_unmatched_raw.dta", replace
	collapse (sum) FUNDING, by(state county_fips county_name)
	keep if county_fips != .
	gsort -FUNDING
	save "`path'/Data/county_cbsa_unmatched.dta", replace
restore
* save matched
keep if _m == 3
drop _m

save "`path'/Data/nih_cbsa.dta", replace

*** TO-DO: Fix unmatched (esp. Bar Harbor Maine)


use "`path'/Data/nih_cbsa.dta", clear
keep if CBSA_level_id == "1"
collapse (sum) FUNDING, by(CBSA_code CBSA_title year)
drop if year == 1992
save "`path'/Data/nih_msa_collapsed.dta", replace


*** Adjust for inflation
use "`path'/Data/nih_msa_collapsed.dta", clear
merge m:1 year using "`path'/Data/cpi_annual_avg.dta"
keep if _m == 3
drop _m
save "`path'/Data/nih_msa_collapsed_adjusted.dta", replace

use "`path'/Data/nih_msa_collapsed_adjusted.dta", clear
gen cpi_2000 = cpi if year == 2000
egen base_cpi = max(cpi_2000)
drop cpi_2000

replace FUNDING = (base_cpi / cpi) * FUNDING
replace FUNDING = FUNDING / 1000000
label variable FUNDING "Funding in millions and FY200 dollars"
gen log_FUNDING = log(FUNDING+1)
drop cpi base_cpi
save "`path'/Data/nih_msa_collapsed_adjusted.dta", replace


***************************************************************
	*** Collapse
use "`path'/Data/nih_msa.dta", clear
collapse (sum) FUNDING, by(msa msan year)
save "`path'/Data/nih_msa_collapse.dta", replace


*** THIS IS NEW
use "`path'/Data/nih_msa_collapse.dta", clear
keep if year == 2000
replace FUNDING = FUNDING / 1000000
histogram FUNDING, bins(40) title("Amount of funding received in MSAs, 2000") xtitle("FY2000 $ in millions")


use "`path'/Data/nih_msa_collapse.dta", clear
keep if year == 2000
replace FUNDING = log(FUNDING)
histogram FUNDING, bins(40) title("Log(Amount of funding) received in MSAs, 2000") xtitle("Log of FY2000 $ in millions")

***************************************************************
	*** 
clear
import excel "`path'/Raw_Data/Census/cbsa_pop_2000-2005.xlsx", sheet(cleaned) firstrow
rename cbsa_name msan
rename cbsa_code msa
keep if metro_div_code == .
drop if msa == .
save "`path'/Data/cbsa_pop_2000-2005.dta", replace

use "`path'/Data/nih_msa_collapse.dta", clear
merge m:1 msan using "`path'/Data/cbsa_pop_2000-2005.dta"

	
use "`path'/Data/nih_msa_collapse.dta", clear
merge m:1 msa using "`path'/Data/cbsa_pop_2000-2005.dta"
	
	
	
	
log close
