"""
Author: Ozan Aygun
Purpose: Use analytical_data stored in feature_store, prepare training, validation and test sets using KNUMBER
and store at feature_store

Remarks: requires config.json
"""

import json
import pandas as pd

def prepare_held_out_data():

    with open("config.json","rb") as f:
        config = json.load(f)

    val_start =  int(config['validation_data_start_year'])
    val_end = int(config['validation_data_end_year'])
    test_start = int(config['test_data_start_year'])
    test_end = int(config['test_data_end_year'])


    analytical_data = pd.read_csv(config['feature_store_dir'] + 'analytical_data.csv')
    index_data = analytical_data[['KNUMBER','DECISIONDATE']].copy()
    index_data['DECISIONDATE'] = pd.to_datetime(index_data['DECISIONDATE'])
    index_data['DECISIONYEAR'] = index_data.DECISIONDATE.dt.year 
    index_data['DATASET'] = 'train'

    index_data.loc[:,'DATASET'][(index_data['DECISIONYEAR'] >= val_start) & 
        (index_data['DECISIONYEAR'] <= val_end)] = "validation"
    
    index_data.loc[:,'DATASET'][(index_data['DECISIONYEAR'] >= test_start) & 
        (index_data['DECISIONYEAR'] <= test_end)] = "test"

    # Output train, validation, and test set keys
    index_data[index_data["DATASET"] == "train"].to_csv(config['feature_store_dir'] + "train_KNUMBER.csv",index = False)
    index_data[index_data["DATASET"] == "validation"].to_csv(config['feature_store_dir'] + "validation_KNUMBER.csv",index = False)
    index_data[index_data["DATASET"] == "test"].to_csv(config['feature_store_dir'] + "test_KNUMBER.csv",index = False)    
    print("Prepared train, validation and test data set keys...")
