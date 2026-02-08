local path "/Users/lydia/Desktop/Thesis"
clear all

*** 1990-99 county population
import delimited using "`path'/Raw_data/Census/county_pop/99c8_00.txt", clear

egen line = concat(v*)
split line
keep line*

foreach x in `r(varlist)' {
	replace x = strtrim(x)
}

drop line line14 line15 line16 line17 line18 line19
drop if _n == 1 // drop US
drop if real(line8)==. // drop 2 cases that are not numbers
drop line1

rename line2 cty_fips
keep if strlen(cty_fips) == 5

drop line13 // this is April 1990 population re-estimate base
rename line3 pop1999
rename line4 pop1998
rename line5 pop1997
rename line6 pop1996
rename line7 pop1995
rename line8 pop1994
rename line9 pop1993
rename line10 pop1992
rename line11 pop1991
rename line12 pop1990

destring(pop*), replace

save "`path'/Data/Census/population/county90-99.dta", replace
use "`path'/Data/Census/population/county90-99.dta", clear

*** 2000-2010 county population
import delimited using "`path'/Raw_data/Census/county_pop/co-est00int-tot.csv", clear
drop region division sumlev
tostring(state), replace
tostring(county), replace

* make fips code
replace state = "0" + state if (strlen(state) == 1)
replace county = "00" + county if (strlen(county) == 1)
replace county = "0" + county if (strlen(county) == 2)

gen cty_fips = state + county
drop state county

keep cty_fips popestimate*
rename popestimate2000 pop2000
rename popestimate2001 pop2001
rename popestimate2002 pop2002
rename popestimate2003 pop2003
rename popestimate2004 pop2004
rename popestimate2005 pop2005
rename popestimate2006 pop2006
rename popestimate2007 pop2007
rename popestimate2008 pop2008
rename popestimate2009 pop2009
rename popestimate2010 pop2010


save "`path'/Data/Census/population/county00-10.dta", replace

*** 2011-2020 county population
import delimited using "`path'/Raw_data/Census/county_pop/co-est2020.csv", clear
drop region division sumlev
tostring(state), replace
tostring(county), replace

* make fips code
replace state = "0" + state if (strlen(state) == 1)
replace county = "00" + county if (strlen(county) == 1)
replace county = "0" + county if (strlen(county) == 2)

gen cty_fips = state + county
drop state county
drop stname 

keep cty_fips popestimate*
drop popestimate2010  
drop popestimate042020
rename popestimate2011 pop2011
rename popestimate2012 pop2012
rename popestimate2013 pop2013
rename popestimate2014 pop2014
rename popestimate2015 pop2015
rename popestimate2016 pop2016
rename popestimate2017 pop2017
rename popestimate2018 pop2018
rename popestimate2019 pop2019
rename popestimate2020 pop2020
save "`path'/Data/Census/population/county11-20.dta", replace


*** 2020-2025 county population
/*
// import excel using "`path'/Raw_data/Census/county_pop/co-est2024-pop.xlsx", clear
save "`path'/Data/Census/population/county20-24_raw.dta", replace

use "`path'/Data/Census/population/county20-24_raw.dta", clear
rename var1 location
rename var2 pop2020
rename var3 pop2021
rename var4 pop2022
rename var5 pop2023
rename var6 pop2024

replace pop2020 = subinstr(pop2020, ",", "", 3)
destring pop2020, replace

replace pop2021 = subinstr(pop2021, ",", "", 3)
destring pop2021, replace

replace pop2022 = subinstr(pop2022, ",", "", 3)
destring pop2022, replace

replace pop2023 = subinstr(pop2023, ",", "", 3)
destring pop2023, replace

replace pop2024 = subinstr(pop2024, ",", "", 3)
destring pop2024, replace

replace location = subinstr(location, ".", "", 2)
gen ctyname = substr(location, 1, strpos(location, ",")-1)
gen stname = substr(location, strpos(location, ",")+1, strlen(location))
replace stname = strtrim(stname)
replace ctyname = strtrim(ctyname)

gen county = substr(ctyname, 1, strpos(ctyname, "County")-2)
replace county = substr(location, 1, strpos(location, "city")-2) if county == ""
drop ctyname
rename county ctyname

drop location
save "`path'/Data/Census/population/county20-24.dta", replace


* get county fips
// use "`path'/Data/Census/population/county11-20.dta", clear
// keep ctyname cty_fips stname
// replace stname = strtrim(stname)
// replace ctyname = strtrim(ctyname)
// drop if cty_fips == "11000" // drop duplicate of DC
// save "`path'/Data/Census/population/county_fips.dta", replace
//
// use "`path'/Data/Census/population/county20-24.dta", clear
// merge 1:1 ctyname stname using "`path'/Data/Census/population/county_fips.dta"

*** Trying to get county_fips again
use "`path'/Data/Crosswalks/Used/city_county_map.dta", clear
keep county county_name state
rename state state_abbrev
merge m:1 state_abbrev using "`path'/Data/Crosswalks/Used/state_abbrev.dta"
rename county_name ctyname 
keep if _m == 3
drop _m
rename state_fullname stname
save "`path'/Data/Crosswalks/Used/county_fips.dta", replace
use "`path'/Data/Crosswalks/Used/county_fips.dta", clear

use "`path'/Data/Census/population/county20-24.dta", clear
replace stname = strupper(stname)
merge 1:1 ctyname stname using "`path'/Data/Crosswalks/Used/county_fips.dta"
*/

use "`path'/Raw_data/Census/county_pop/pop2021.dta", clear
merge 1:1 statea countya using "`path'/Raw_data/Census/county_pop/pop2022.dta",
keep if _m == 3
drop _m
merge 1:1 statea countya using "`path'/Raw_data/Census/county_pop/pop2023.dta",
keep if _m == 3
drop _m
merge 1:1 statea countya using "`path'/Raw_data/Census/county_pop/pop2024.dta",
keep if _m == 3
drop _m
save "`path'/Data/Census/population/county20-24.dta", replace
gen cty_fips = statea + countya
drop statea countya


*** Should all merge to MSAs first, then combine

use "`path'/Data/Census/population/county90-99.dta", clear
destring cty_fips, replace
rename cty_fips county_fips
merge 1:1 county_fips using "`path'/Data/Crosswalks/Used/county_cbsa_xwalk_2009.dta"
keep if _m == 3
drop _m
save "`path'/Data/Census/population/county90-99_msa.dta", replace
collapse (sum) pop*, by(CBSA_code CBSA_title)
save "`path'/Data/Census/population/county90-99_msa.dta", replace


use "`path'/Data/Census/population/county00-10.dta", clear
destring cty_fips, replace
rename cty_fips county_fips
merge 1:1 county_fips using "`path'/Data/Crosswalks/Used/county_cbsa_xwalk_2009.dta"
keep if _m == 3
drop _m
save "`path'/Data/Census/population/county00-10_msa.dta", replace
collapse (sum) pop*, by(CBSA_code CBSA_title)
save "`path'/Data/Census/population/county00-10_msa.dta", replace

use "`path'/Data/Census/population/county11-20.dta", clear
destring cty_fips, replace
rename cty_fips county_fips
merge 1:1 county_fips using "`path'/Data/Crosswalks/Used/county_cbsa_xwalk_2009.dta"
keep if _m == 3
drop _m
save "`path'/Data/Census/population/county11-20_msa.dta", replace
collapse (sum) pop*, by(CBSA_code CBSA_title)
save "`path'/Data/Census/population/county11-20_msa.dta", replace

use "`path'/Data/Census/population/county20-24.dta", clear
destring cty_fips, replace
rename cty_fips county_fips
merge 1:1 county_fips using "`path'/Data/Crosswalks/Used/county_cbsa_xwalk_2009.dta"
keep if _m == 3
drop _m
save "`path'/Data/Census/population/county21-24_msa.dta", replace
collapse (sum) pop*, by(CBSA_code CBSA_title)
save "`path'/Data/Census/population/county21-24_msa.dta", replace

use "`path'/Data/Census/population/county90-99_msa.dta", clear
merge 1:1 CBSA_code CBSA_title using "`path'/Data/Census/population/county00-10_msa.dta"
keep if _m == 3
drop _m
merge 1:1 CBSA_code CBSA_title using "`path'/Data/Census/population/county11-20_msa.dta"
keep if _m == 3
drop _m
merge 1:1 CBSA_code CBSA_title using "`path'/Data/Census/population/county21-24_msa.dta"
keep if _m == 3
drop _m
order pop*, alphabetic
* I don't think the 2021-2024 estimates can be trusted
drop pop2021 pop2022 pop2023 pop2024
save "`path'/Data/Census/population/population_msa.dta", replace
