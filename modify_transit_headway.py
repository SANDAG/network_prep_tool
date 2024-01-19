import sys
import numpy as np
import os
import pandas as pd

def modify_transit_headway(scenario_path: str, rate, output_path: str) -> pd.DataFrame:
    """ Takes an input path to a templated ABM scenario, reads the
    input trrt.csv from the input folder, and outputs an update trrt.csv with
    new headway.

    Args:
        scenario_path: String location of the templated ABM scenario folder

    Returns:
        A DataFrame of the updated headway """
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
    
    trrt["AM_Headway"] = trrt["AM_Headway"] * rate
    trrt["PM_Headway"] = trrt["PM_Headway"] * rate
    trrt["OP_Headway"] = trrt["OP_Headway"] * rate
    trrt["Night_Headway"] = trrt["Night_Headway"] * rate
    
    # write out updated colums
    return trrt

scenario_path = sys.argv[1]
rate = sys.argv[2]
output_path = sys.argv[3]
modify_transit_headway(scenario_path, rate, output_path).to_csv(os.path.join(output_path, "trrt.csv"), index=False)