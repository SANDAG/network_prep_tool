import sys
import numpy as np
import os
import pandas as pd

def modify_parking_cost(scenario_path,rate,mgra_MoHub,policy,policy_type=1):
    df_policy = pd.read_csv(policy)
    df_mohub = pd.read_csv(mgra_MoHub)
    df_mgra = pd.read_csv(os.path.join(scenario_path,"input", "mgra15_based_input2035.csv"))
    merged_df = pd.merge(df_mohub,df_policy,on='MoHubType',how='left')
    merged_df.loc[merged_df['PARKCOV_ID'].isnull(),['Hourly','Daily','Monthly']] = None
    merged_df = merged_df[['mgra','Hourly','Daily','Monthly']]
    merged_df.columns = ['mgra','exp_hourly_pca','exp_daily_pca','exp_monthly_pca']

    merged_df['exp_hourly_pca'] = merged_df['exp_hourly_pca']*rate
    merged_df['exp_daily_pca'] = merged_df['exp_daily_pca']*rate
    merged_df['exp_monthly_pca'] = merged_df['exp_monthly_pca']*rate

    final_df = pd.merge(df_mgra,merged_df,on='mgra',how='outer')
    final_df.sort_values(by='mgra',inplace=True)
    final_df.reset_index(drop=True,inplace=True)
    final_df['exp_hourly'] = np.where(final_df['exp_hourly_pca'].isna(),final_df['exp_hourly'],final_df['exp_hourly_pca'])
    final_df['exp_daily'] = np.where(final_df['exp_daily_pca'].isna(),final_df['exp_daily'],final_df['exp_daily_pca'])
    final_df['exp_monthly'] = np.where(final_df['exp_monthly_pca'].isna(),final_df['exp_monthly'],final_df['exp_monthly_pca'])
    final_df.drop(['exp_hourly_pca','exp_daily_pca','exp_monthly_pca'],axis=1,inplace=True)

    return final_df




# policy = "T:/projects/sr15/abm3_dev/sensitivity_test_plan/test_inputs/07_parking_cost_pos50/ParkingPolicies.csv"
mgra_MoHub = "T:/projects/sr15/abm3_dev/sensitivity_test_plan/test_inputs/07_parking_cost_pos50/moHub_mgra.csv"
policy = sys.argv[1]
scenario_path = 'T:/projects/sr15/abm3_dev/sensitivity_test_plan/2035_0126_template/'
# policy = './ParkingPolicies_PCA.csv'
# mgra_MoHub = './moHub_mgra_PCA.csv'
rate_perc = sys.argv[2] # 0,50,-50 = *1, *1.5, *0.5
output_path = './'
policy_type = sys.argv[3] #1 = pca, 2 = MoHub
if rate_perc=='0':
    rate=1.0
elif rate_perc=='50':
    rate=1.5
elif rate_perc=='-50':
    rate=0.5
else:
    print("Input rate % needs to be (0,50,-50)")

out_file = os.path.join(output_path,"mgra15_based_input2035.csv")
modify_parking_cost(scenario_path,rate,mgra_MoHub,policy,policy_type).to_csv(out_file,index=False)
