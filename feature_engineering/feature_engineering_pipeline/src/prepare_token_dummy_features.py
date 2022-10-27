"""
Author: Ozan Aygun
Purpose: Engineer dummy features from tokens determined in the initiation stage,
save to feature_store storage.

Remarks: requires config.json
         Updates: features_dummy.csv within the feature_store   
"""

import json
import pandas as pd
import numpy as np


def prepare_token_dummy_features_DEVICENAME():

    with open("config.json","rb") as f:
        config = json.load(f)

    # Locate and load the token_dict
    feature_store_path = config['feature_store_dir']    
    tokens_to_search = pd.read_csv(feature_store_path + "token_dict_DEVICENAME.csv")['tokens'].tolist()

    #Load and process analytical data
    data_510k = pd.read_csv(feature_store_path+"analytical_data.csv")[["KNUMBER","DEVICENAME"]]
    data_510k.loc[:,"DEVICENAME"] = data_510k.loc[:,"DEVICENAME"].str.lower()\
        .str.replace(" ","_").str.replace("\W","")

    # For each token in the token_dict, perform a str match
    for token in tokens_to_search:
        data_510k.loc[:,token] = data_510k.loc[:,'DEVICENAME'].str.contains(token) * 1    

    # Remove any features that didn't map (mostly because we are not applying word stemming here)
    counts = data_510k.iloc[:,2:].apply(sum,axis = 0)
    counts = ['KNUMBER']+ counts[counts > 0].index.tolist()
    data_510k = data_510k.loc[:,counts]

    # Locate the features_dummy from feature store, merge using KNUMBER and update
    features_dummy = pd.read_csv(feature_store_path + "features_dummy.csv")
    features_dummy = pd.merge(features_dummy,data_510k,on = "KNUMBER")
    features_dummy.to_csv(feature_store_path + "features_dummy.csv", index=False)