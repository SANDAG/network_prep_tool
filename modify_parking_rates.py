import sys
import numpy as np
import os
import pandas as pd

def modify_parking_cost(scenario_path,rate,policy,mgra_MoHub):
    df_policy = pd.read_csv(policy)
    df_mohub = pd.read_csv(mgra_MoHub)
    df_mgra = pd.read_csv(os.path.join(scenario_path,"input", "mgra15_based_input2035.csv"))
    merged_df = pd.merge(df_mohub,df_policy,on='MoHubType',how='left')[['MGRA','Hourly','Daily','Monthly']]
    merged_df.columns = ['mgra','exp_hourly','exp_daily','exp_monthly']

    merged_df['exp_hourly'] = merged_df['exp_hourly']*rate
    merged_df['exp_daily'] = merged_df['exp_daily']*rate
    merged_df['exp_monthly'] = merged_df['exp_monthly']*rate

    df_mgra.drop(['exp_hourly','exp_daily','exp_monthly'],axis=1,inplace=True)
    final_df = pd.merge(df_mgra,merged_df,on='mgra',how='left')
    final_df[['exp_hourly','exp_daily','exp_monthly']] = final_df[['exp_hourly','exp_daily','exp_monthly']].fillna(0)
    final_df.sort_values(by='mgra',inplace=True)
    return final_df




policy = "T:/projects/sr15/abm3_dev/sensitivity_test_plan/test_inputs/07_parking_cost_pos50/ParkingPolicies.csv"
mgra_MoHub = "T:/projects/sr15/abm3_dev/sensitivity_test_plan/test_inputs/07_parking_cost_pos50/moHub_mgra.csv"
scenario_path = sys.argv[1]
rate_perc = sys.argv[2] # 0,50,-50 = *1, *1.5, *0.5
output_path = sys.argv[3]
if rate_perc=='0':
    rate=1.0
elif rate_perc=='50':
    rate=1.5
elif rate_perc=='-50':
    rate=0.5
else:
    print("Input rate % needs to be (0,50,-50)")

out_file = os.path.join(output_path,"mgra15_based_input2035.csv")
modify_parking_cost(scenario_path,rate,policy,mgra_MoHub).to_csv(out_file,index=False)
