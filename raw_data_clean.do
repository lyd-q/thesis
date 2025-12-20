local path "/Users/lydia/Desktop/Thesis"
log using "`path'/Code/Log/raw_data_clean.log", replace


forvalues year = 1992(1)2003{
	clear
	import excel "`path'/Raw_data/Worldwide`year'.xls", firstrow
	gen year = 	`year'
	describe
	save "`path'/Data/nih_raw_`year'.dta", replace
}

forvalues year = 2004(1)2007{
	clear
	import excel "`path'/Raw_data/Worldwide`year'.xls", firstrow
	gen year = 	`year'
	* a couple funding observations have characters or words
	gen indirect_has_letter = regexm(INDIRECTCOST, "[A-Za-z]")
	gen funding_has_letter = regexm(FUNDING, "[A-Za-z]")
	drop if indirect_has_letter
	drop if funding_has_letter
	destring INDIRECTCOST, replace
	destring FUNDING, replace
	describe
	save "`path'/Data/nih_raw_`year'.dta", replace
}


clear
import excel "`path'/Raw_data/Worldwide2008.xlsx", firstrow
gen year = 2008
gen indirect_has_letter = regexm(INDIRECTCOST, "[A-Za-z]")
gen funding_has_letter = regexm(FUNDING, "[A-Za-z]")
drop if indirect_has_letter
drop if funding_has_letter
destring INDIRECTCOST, replace
destring FUNDING, replace
describe
save "`path'/Data/nih_raw_2008.dta", replace

clear
import excel "`path'/Raw_data/Worldwide2009.xls", firstrow
gen year = 2009
describe
save "`path'/Data/nih_raw_2009.dta", replace


clear
import excel "`path'/Raw_data/Worldwide2010.xlsx", firstrow
gen year = 2010
describe
save "`path'/Data/nih_raw_2010.dta", replace

forvalues year = 2011(1)2022{
	clear
	import excel "`path'/Raw_data/Worldwide`year'.xls", firstrow
	gen year = 	`year'
	describe
	save "`path'/Data/nih_raw_`year'.dta", replace
}

forvalues year = 2023(1)2025{
	clear
	import excel "`path'/Raw_data/Worldwide`year'.xlsx", firstrow
	gen year = 	`year'
	describe
	save "`path'/Data/nih_raw_`year'.dta", replace
}


***************************************************************
	*** Aggregate data
	
use "`path'/Data/nih_raw_1992.dta", clear
forvalues year = 1992(1)2025 {
	append using "`path'/Data/nih_raw_`year'.dta", force
	erase "`path'/Data/nih_raw_`year'.dta"
	save "`path'/Data/nih_raw.dta", replace
}

use "`path'/Data/nih_raw.dta", clear
drop indirect_has_letter  funding_has_letter 
save "`path'/Data/nih_raw.dta", replace
***************************************************************


log close
