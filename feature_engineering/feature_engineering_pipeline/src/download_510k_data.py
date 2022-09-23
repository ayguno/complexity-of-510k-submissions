"""
Author: Ozan Aygun
Purpose: Download 510(k) database to transient data storage within feature engineering pipeline.

Remarks: requires config.json
"""
import os
import json
import urllib.request
import zipfile

#################################################################################
# TIP for VScode: How to make sure default wd is the current script location
# See: https://code.visualstudio.com/docs/editor/debugging
# https://stackoverflow.com/questions/38623138/vscode-how-to-set-working-directory-for-debugging-a-python-program/55072246#55072246
# Need the subdirectory .vscode along with the launch.json inside
#################################################################################

def download_data():
    # load the configuration file
    with open("config.json", "rb") as f:
        config = json.load(f)
    print("Loaded configuration...")
    # download the most recent data (it comes zipped)
    urllib.request.urlretrieve(config['most_recent_510k_data_path'],'../data/most_recent_data.zip')
    print("Downloaded compressed data...")
    # unzip
    with zipfile.ZipFile('../data/most_recent_data.zip', 'r') as zip_ref:
        zip_ref.extractall("../data")
    print("Extracted data...")
    # delete compressed directory
    os.remove("../data/most_recent_data.zip")
    print("Removed compressed data...")
    print("Current data ready to load: "+ str(os.listdir("../data")))