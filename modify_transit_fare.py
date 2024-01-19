import sys
import numpy as np
import os
import pandas as pd
import re

def modify_transit_fare(scenario_path: str, rate, output_path: str) -> pd.DataFrame:
    """ Takes an input path to a templated ABM scenario, reads the
    input trrt.csv from the input folder, and outputs an update trrt.csv with
    new fare.

    Args:
        scenario_path: String location of the templated ABM scenario folder

    Returns:
        A DataFrame of the updated fare """
    # read in input trrt.csv
    trrt = pd.read_csv(os.path.join(scenario_path, "input", "trrt.csv"),
                       usecols = ["Route_ID",
                                  "Route_Name",
                                  "Mode",
                                  "AM_Headway",
                                  "PM_Headway",
                                  "OP_Headway",
                                  "Night_Headway",
                                  "Night_Hours",
                                  "Config",
                                  "Fare"],
                       dtype={"Route_ID": "int16",
                              "Route_Name": "str",
                              "Mode": "int16",
                              "AM_Headway": "float32",
                              "PM_Headway": "float32",
                              "OP_Headway": "float32",
                              "Night_Headway": "float32",
                              "Night_Hours": "int16",
                              "Config": "str",
                              "Fare": "float32"})
    
    # apply the rate to change headway
    rate = float(rate)
    
    trrt["Fare"] = trrt["Fare"] * rate
    
    # write out updated colums
    return trrt

def modify_transit_special_fare(scenario_path: str, rate, output_path: str):
    """ Takes an input path to a templated ABM scenario, reads the
    input special_fare.txt from the input folder, and outputs an update special_fare.txt with
    new fare.

    Args:
        scenario_path: String location of the templated ABM scenario folder

    Returns:
        A text of the updated transit special fare """
    # read in input special_fare.txt
    special_fare_path = os.path.join(scenario_path, "input", "special_fares.txt")
    update_fare_path = os.path.join(output_path, "special_fares.txt")
    
    fin = open(special_fare_path, "r")
    fout = open(update_fare_path, "w")
    
    with fin as f:
        data = f.read()
    
    # write out updated special fare
    rate = float(rate)

    if rate == 0.5:
        with fout as f:
            data = data.replace('3.00', '1.50').replace('7.50', '3.75')
            f.write(data)
            #f.write(re.sub(r"3.00", r"1.50", data))
            #f.write(re.sub(r"7.50", r"3.75", data))    
    if rate == 0:
        with fout as f:
            data = data.replace('3.00', '0.00').replace('7.50', '0.00')
            f.write(data)
    if rate == 1.5:
        with fout as f:
            data = data.replace('3.00', '4.50').replace('7.50', '11.25')
            f.write(data)
    
    fout.close()
    fin.close()
    
    return 

scenario_path = sys.argv[1]
rate = sys.argv[2]
output_path = sys.argv[3]
modify_transit_fare(scenario_path, rate, output_path).to_csv(os.path.join(output_path, "trrt.csv"), index=False)
modify_transit_special_fare(scenario_path, rate, output_path)