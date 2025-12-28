
### Documentation: Code files ###
Data_Cleaning:
    * nih_grants_clean.py: Clean NIH grants with MSA merged, then make version collapsed by MSA
    * census1990_clean.py: Clean 1990 census, then collapse by MSA
    * bds_outcomes_clean.py: Outcomes from BDS, collapsed by MSA
    Data_Cleaning_v1:
        * data_census_clean1990.py
        * data_census_clean2000.py
        * data_census2000.py
        * data_clean_final.py
        * data_msa_collapse.do
        * data_prep_old.py
        * raw_data_clean.do
        * data_bds_outcomes.py -- prepares and merges economic outcomes from BDS

Descriptive:
    * mapping.py -- TO-DO: change in dollars per capita maps, move Alaska and Hawaii, save as high-res
    * msa_descriptive.do -- annual trends in funding by msa
    * panel_descriptive.do -- annual trends in funding overall -- TO-DO:

Exploratory_Data_Analysis:
    * cross_regress_county.py -- Old, by county only
    * cross_regress_msa.py -- Old, by MSA
    * cross_sec_regress_v0.5.py -- Old
    * cross_sec_regress_v2.py -- Updated regressions with plotting
    * data_trends.py
    * diff_in_diff.py

Bartik Shift Share


### Documentation: Relevant Data Files ###
NIH:
    * Data/nih_US.dta = NIH grants in US states, raw
    * Data/nih_county.dta = NIH grants with counties merged 1992-2024, manual county matches added
    * Data/nih_cbsa.dta = US NIH grants with MSA merged, before collapse

    * Data/NIH_v2/nih_msa.dta = grants with org_dept (field) and (congressional district) added


Census:

BDS: