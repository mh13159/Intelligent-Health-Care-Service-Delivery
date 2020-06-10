# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:15:05 2020

@author: hamza
"""


#import Libraries
import pandas as pd


Raw_Data_Directroy_Path_Relative = "..\\..\\Data\\Raw\\"
Processed_Data_Directroy_Path_Relative = "..\\..\\Data\\Processed\\"

#Load Datasets

    # Dataset 1 Facilities - Dataset 1.3.1 (Ntroduction, n.d.)

Facilities  = (pd.
               read_excel
               (Raw_Data_Directroy_Path_Relative+
                "Facilites.xlsx"))

    # converting Zipcode type to string
Facilities= Facilities.astype({"Facility Area-Zipcode":str})


    # Dataset 2  Population Demographics - Datasets 1.3.2 (Ntroduction, n.d.)

Population_Demographics = (pd.
                           read_csv
                           (Raw_Data_Directroy_Path_Relative+
                            "Population_Demographics\\ACSDP5Y2018."+
                            "DP05_data_with_overlays_2020-06-02T120849.csv",
                            header=1))

clean_ZCTA_pop = [ZCTA[len("ZCTA5")+1:] for ZCTA in list(Population_Demographics
                                                   ["Geographic Area Name"])]
Population_Demographics["Geographic Area Name"]= clean_ZCTA_pop

    # Dataset 3 Maternity Information - Datasets 1.3.2 (Ntroduction, n.d.)
Maternity_Information = (pd.
                           read_csv
                           (Raw_Data_Directroy_Path_Relative+
                            "Maternity\\"+
                            "ACSDT5Y2011."+
                            "B13002_data_with_overlays_2020-06-07T222955.csv",
                            header=1))


clean_ZCTA_mat = [ZCTA[len("ZCTA5")+1:] for ZCTA in list(Maternity_Information
                                                   ["Geographic Area Name"])]


Maternity_Information["Geographic Area Name"]= clean_ZCTA_mat


Integrated_Data_Facility_Population_Maternity = (Facilities.merge
                                                 (Population_Demographics,
                                                  how="inner",
                                                  left_on=
                                                  "Facility Area-Zipcode",
                                                  right_on=
                                                  "Geographic Area Name").
                                                 merge
                                                 (Maternity_Information,
                                                  how="inner",
                                                  left_on=
                                                  "Facility Area-Zipcode",
                                                  right_on=
                                                  "Geographic Area Name"))
Perecnt_Elderly_col_name = "Percent Estimate!!SEX AND AGE!!Total population!!65 to 74 years"

Percent_Female_col_name = "Percent Estimate!!SEX AND AGE!!Total population!!Female"

Maternity_Total_Women_col_name = "Estimate!!Total"

Maternity_Women_Gave_Birth_Past_12_months_col_name =("Estimate!!Total!!Women who had a birth in the past 12 months")

Total_Population_col_name = "Estimate!!RACE!!Total population"

Integrated_Data_Facility_Population_Maternity = (
    Integrated_Data_Facility_Population_Maternity.
    astype({Perecnt_Elderly_col_name:float,
            Percent_Female_col_name:float,
            Maternity_Total_Women_col_name:int,
            Maternity_Women_Gave_Birth_Past_12_months_col_name:int}))


# <Calculation for Current Elderly Population Count>#

Elderly_Total_Population_col = (
    Integrated_Data_Facility_Population_Maternity
    [Total_Population_col_name]*
    (Integrated_Data_Facility_Population_Maternity
     [Perecnt_Elderly_col_name]/100)
    )
# <Calculation for Current Elderly Population Count>#

# <ROUND OFF> #

Elderly_Total_Population_col = Elderly_Total_Population_col.astype("int")

# <ROUND OFF> #

# <Calculation for Current Maternity Population Count>#
Maternity_Percentage_Female_Population_col = (
    (Integrated_Data_Facility_Population_Maternity
     [Maternity_Total_Women_col_name]/
     Integrated_Data_Facility_Population_Maternity
     [Maternity_Women_Gave_Birth_Past_12_months_col_name])/
    100
    )


Female_Total_Population_col = (Integrated_Data_Facility_Population_Maternity
                               [Total_Population_col_name]*
                               (Integrated_Data_Facility_Population_Maternity
                               [Percent_Female_col_name]/100)
                               )

    # <ROUND OFF> #
Female_Total_Population_col = Female_Total_Population_col.astype("int")
    # <ROUND OFF> #


Maternity_Total_Population_col = (
    Maternity_Percentage_Female_Population_col*
    Female_Total_Population_col
    )

    # <ROUND OFF> #
Maternity_Total_Population_col = Maternity_Total_Population_col.astype("int")
    # <ROUND OFF> #


# <Calculation for Current Maternity Population Count> #


# <Create Export Required Dataset>#

Export_Data = pd.DataFrame()
Export_Data = Facilities

Export_Data["Area Population"] = (
    Integrated_Data_Facility_Population_Maternity
    [Total_Population_col_name])

Export_Data["Maternity Population within Area"] = ( 
    Maternity_Total_Population_col
    )

Export_Data["Elderly Population within Area"] = ( 
    Elderly_Total_Population_col
    )

# Increase/decrease trend col  - IN PROGRESS
"""Based on trend slope + / -  over historic data"""

 
# Increase/decrease percentage col - IN PROGRESS
"""Based on yearly historic data"""



''' Assign Facility Type based on highest number of resource available over 
 service categories ---  P: 10 , S: 20 T: 30 ---> T type facility '''

(Export_Data.
 to_csv
 (Processed_Data_Directroy_Path_Relative+"DataFeatures_v01.csv"))
# <Create Export Required Dataset> #








