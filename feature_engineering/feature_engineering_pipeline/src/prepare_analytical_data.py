"""
Author: Ozan Aygun
Purpose: Prepare analytical data from downloaded 510(k) database, engineer simple features,
save to feature_store storage.

Remarks: requires config.json
"""
from distutils.log import error
import os
import json
import pandas as pd
import numpy as np


def prepare_analytical_data():

    # Load config
    with open("config.json",'rb') as f:
        config = json.load(f)

    ###############################################
    # !! BACKLOG !!
    # How to properly execute empty ../data/ error
    # Otherwise output is ready
    ###############################################

    # Check if raw data exists
    if len(os.listdir("../data")) < 1:
        error(config['raw_501k_filename']+" doesn't exist.")

    if os.listdir("../data/")[0] == config['raw_510k_filename']:
        print("Found raw data for processing...")
        # Load raw data (Windows-specific argument: encoding = "ISO-8859-1")
        data_510k = pd.read_csv("../data/"+ config['raw_510k_filename'],sep="|",encoding = "ISO-8859-1")
        
        # Date formatting
        data_510k["DATERECEIVED"] = pd.to_datetime(data_510k["DATERECEIVED"])
        data_510k["DECISIONDATE"] = pd.to_datetime(data_510k["DECISIONDATE"])
        DECISION_TIME_DAYS = data_510k["DECISIONDATE"] - data_510k["DATERECEIVED"]
        data_510k["DECISION_TIME_DAYS"] = DECISION_TIME_DAYS.dt.days # define DECISION_TIME_DAYS
        data_510k["DECISION_TIME_DAYS_LOG10"] = np.log10(data_510k["DECISION_TIME_DAYS"])
        print("Formatted dates, calculated DECISION_TIME_DAYS...")
        
        # Define COMPLEXITY based on DECISION_TIME_DAYS
        data_510k["COMPLEXITY"] = "H"
        data_510k["COMPLEXITY"][data_510k["DECISION_TIME_DAYS"] <= 90] = "L"
        mask = np.logical_and(data_510k["DECISION_TIME_DAYS"] > 90, data_510k["DECISION_TIME_DAYS"] <= 265)
        data_510k["COMPLEXITY"][mask] = 'M'
        data_510k = data_510k[data_510k["DECISIONDATE"] >= pd.to_datetime('10-01-2007')] # Filter >= FY 2007 (MDUFA II)
        data_510k = data_510k[data_510k["THIRDPARTY"] == 'N']  # Filter out 3rd party submissions
        data_510k = data_510k[data_510k["TYPE"] == 'Traditional'] # Retain Traditional 510(k)s
        data_510k = data_510k[data_510k["DECISION"] == 'SESE'] # Retain records with SESE decisions
        print("Filtered data...")
        
        # Generate Dummy Variables from PRODUCTCODE and CLASSADVISECOMM
        data_510k_dummies = pd.get_dummies(data_510k[['KNUMBER','PRODUCTCODE','CLASSADVISECOMM']],
            columns=['PRODUCTCODE','CLASSADVISECOMM'], drop_first= False, 
            prefix=['PRODUCTCODE','CLASSADVISECOMM'])
        # Select the features determined during initiation (Use KNUMBER as a key between the analytical set and features)
        data_510k_features = data_510k_dummies[['KNUMBER'] + 
            ['PRODUCTCODE_'+ i for i in ['IYE','IYN','JJX','LYZ','NBW']]+
            ['CLASSADVISECOMM_'+ i for i in ['AN','HE','IM','MI','RA','TX']] ]
        
        # Save analytical data set and features into feature_store
        data_510k.to_csv(config['feature_store_dir']+"analytical_data.csv", index = False) 
        data_510k_features.to_csv(config['feature_store_dir']+"features_dummy.csv", index = False) 
        print("Saved data to feature_store, exiting...")

    else:
        error(config['raw_501k_filename']+" doesn't exist.")