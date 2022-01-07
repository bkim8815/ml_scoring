import subprocess
import pandas as pd
import numpy as np
import timeit
import os
import json
import pickle
##################Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f)

prod_deployment_path = os.path.join(config['prod_deployment_path'])
test_data_path = os.path.join(config['test_data_path'])

output_folder_path = os.path.join(config['output_folder_path'])


##################Function to get model predictions
def model_predictions():
    #read the deployed model and a test dataset, calculate predictions


    with open(prod_deployment_path+'/'+'trainedmodel.pkl', 'rb') as file:
        model = pickle.load(file)

    testdata=pd.read_csv(test_data_path+ '/'+'testdata.csv')


    X = testdata[['lastmonth_activity','lastyear_activity','number_of_employees']].values.reshape(-1,3)
    y = testdata['exited'].values.reshape(-1,1)

    predicted=model.predict(X)
    # print(predicted)
    return predicted



##################Function to get summary statistics
def dataframe_summary():
    #calculate summary statistics here
    stats = []
    df=pd.read_csv(output_folder_path+ '/'+'finaldata.csv')
    df = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees', 'exited']]
    stats.append(df.mean().to_list())
    stats.append(df.std().to_list())
    stats.append(df.median().to_list())
    print(stats)

    return stats

##################Function to get timings
def execution_time():
    #calculate timing of training.py and ingestion.py
    training_timings=[]

    starttime = timeit.default_timer()
    os.system('python3 training.py')
    timing=timeit.default_timer() - starttime
    training_timings.append(timing)

    starttime = timeit.default_timer()
    os.system('python3 ingestion.py')
    timing=timeit.default_timer() - starttime
    training_timings.append(timing)
    print(training_timings)
    return training_timings

##################Function to check dependencies
def outdated_packages_list():
    outdated = subprocess.check_output(['pip', 'list', '--outdated'])
    with open('outdated.txt', 'wb') as f:
        f.write(outdated)


##################Function to check na_percent
def missing_data():
    df=pd.read_csv(output_folder_path+ '/'+'finaldata.csv')
    nas = []
    for col in df.columns:
        na_pct=df[col].isna().sum() / len(df)
        nas.append(na_pct)
    return nas

if __name__ == '__main__':
    model_predictions()
    dataframe_summary()
    missing_data()
    execution_time()
    outdated_packages_list()
