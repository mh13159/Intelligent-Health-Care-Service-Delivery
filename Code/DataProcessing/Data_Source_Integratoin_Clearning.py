# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:15:05 2020

@author: hamza
"""
import pandas as pd

# Define file paths
RAW_DATA_DIR = "../../Data/Raw/"
PROCESSED_DATA_DIR = "../../Data/Processed/"

# Load datasets
def load_dataset(file_path, file_name, skip_rows=1):
    return pd.read_csv(file_path + file_name, skiprows=skip_rows)

facilities = load_dataset(RAW_DATA_DIR, "Facilities.xlsx")
population_demographics = load_dataset(RAW_DATA_DIR + "Population_Demographics/", "ACSDP5Y2018.DP05_data_with_overlays_2020-06-02T120849.csv")
maternity_info = load_dataset(RAW_DATA_DIR + "Maternity/", "ACSDT5Y2011.B13002_data_with_overlays_2020-06-07T222955.csv")

# Clean ZCTA values
def clean_zcta(dataframe, column_name):
    return dataframe[column_name].str[len("ZCTA5")+1:]

population_demographics["Geographic Area Name"] = clean_zcta(population_demographics, "Geographic Area Name")
maternity_info["Geographic Area Name"] = clean_zcta(maternity_info, "Geographic Area Name")

# Merge datasets
integrated_data = facilities.merge(population_demographics, left_on="Facility Area-Zipcode", right_on="Geographic Area Name").merge(maternity_info, left_on="Facility Area-Zipcode", right_on="Geographic Area Name")

# Define column names
PERCENT_ELDERLY_COL = "Percent Estimate!!SEX AND AGE!!Total population!!65 to 74 years"
PERCENT_FEMALE_COL = "Percent Estimate!!SEX AND AGE!!Total population!!Female"
MATERNITY_TOTAL_WOMEN_COL = "Estimate!!Total"
MATERNITY_WOMEN_GAVE_BIRTH_COL = "Estimate!!Total!!Women who had a birth in the past 12 months"
TOTAL_POPULATION_COL = "Estimate!!RACE!!Total population"

# Convert column data types
integrated_data = integrated_data.astype({
    PERCENT_ELDERLY_COL: float,
    PERCENT_FEMALE_COL: float,
    MATERNITY_TOTAL_WOMEN_COL: int,
    MATERNITY_WOMEN_GAVE_BIRTH_COL: int
})

# Calculate current elderly population count
elderly_population_col = (integrated_data[TOTAL_POPULATION_COL] * (integrated_data[PERCENT_ELDERLY_COL] / 100)).astype(int)

# Calculate current maternity population count
maternity_percentage_female_col = ((integrated_data[MATERNITY_TOTAL_WOMEN_COL] / integrated_data[MATERNITY_WOMEN_GAVE_BIRTH_COL]) / 100)
female_total_population_col = (integrated_data[TOTAL_POPULATION_COL] * (integrated_data[PERCENT_FEMALE_COL] / 100)).astype(int)
maternity_total_population_col = (maternity_percentage_female_col * female_total_population_col).astype(int)

# Create export required dataset
export_data = facilities.copy()
export_data["Area Population"] = integrated_data[TOTAL_POPULATION_COL]
export_data["Maternity Population within Area"] = maternity_total_population_col
export_data["Elderly Population within Area"] = elderly_population_col

# Save the export dataset to a CSV file
export_data.to_csv(PROCESSED_DATA_DIR + "DataFeatures_v01.csv", index=False)





