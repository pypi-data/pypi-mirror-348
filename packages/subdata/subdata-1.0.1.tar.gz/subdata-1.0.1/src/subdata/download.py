### 'download_datasets(list_of_dataset_names, {hf_token})' is a function that downloads datasets based on a list of dataset names, returning a dictionary with - if available - the requested datasets. The information on how the datasets are to be downloaded is provided in 'download_dict.json'. 
# input: [list_of_dataset {hf_token}]
# --- hf_token is optional and should be provided if one of the requested datasets requires a valid huggingface token to access the data 
# output: [dict_of_dataset]

### 'check_requirements(dataset_dict, {hf_token})' is a function that checks for a given datasets whether the requirements to access it are fulfilled. 
# input: [dataset_dict {hf_token}]
# output: bool

### [download_csv, download_parquet, download_online_zip, open_manual_zip](dataset_dict) are helper functions that access datasets from the corresponding sources and formats provided in the dataset_dict object.

### [download_hartvigsen_2022, download_mathew_2021](dataset_dict) are helper functions that have the same functionality as the other helper functions, but are tailored to a specific dataset, the access to which was not generalizable enough.

from huggingface_hub import login
from io import BytesIO
import json
import numpy as np
import os
import pandas as pd
import requests
import time
from zipfile import ZipFile

import importlib.resources

from subdata.utils import load_download

def download_datasets(list_of_dataset_names, hf_token=None):

    print(f'Starting to download {len(list_of_dataset_names)} datasets.')

    download_dict = load_download()
    
    dict_of_datasets = {}
    
    for dataset_name in list_of_dataset_names:
        start_time = time.time()
        
        dataset_dict = download_dict[dataset_name]
        
        req = check_requirements(dataset_name, dataset_dict, hf_token)
        
        if req == True:
            
            match dataset_dict['format']:
                case 'csv':
                    df = download_csv(dataset_dict)
                case 'parquet':
                    df = download_parquet(dataset_dict)
                case 'online_zip':
                    df = download_online_zip(dataset_dict)
                case 'manual_zip':
                    df = open_manual_zip(dataset_dict)
                case 'hartvigsen_2022':
                    df = download_hartvigsen_2022(dataset_dict)
                case 'mathew_2021':
                    df = download_mathew_2021(dataset_dict)
                case _:
                    print(f'\tError in downloading {dataset_name}: Unknown format.')
                    
            dict_of_datasets[dataset_name] = df
        
            print(f'\t{dataset_name} downloaded in {str(np.round(time.time()-start_time,4)).rjust(10)}s')
        
    return dict_of_datasets
        
    
    
def download_csv(dataset_dict):
    return pd.read_csv(dataset_dict['urls'][0], **dataset_dict['params'])
    
def download_parquet(dataset_dict):
    return pd.read_parquet(dataset_dict['urls'][0], **dataset_dict['params'])
    
def download_online_zip(dataset_dict):
    content = requests.get(dataset_dict['urls'][0])
    f = ZipFile(BytesIO(content.content))
    with f.open(dataset_dict['filename'], 'r') as g:
        df = pd.read_csv(g, **dataset_dict['params'])
    return df

def open_manual_zip(dataset_dict):
    f = ZipFile('input_folder/'+dataset_dict['filename']+'.zip')
    with f.open(dataset_dict['filename'], 'r') as g:
        df = pd.read_csv(g, **dataset_dict['params'])
    return df

def download_hartvigsen_2022(dataset_dict):
    columns = [['generation','group'],['Input.text','Input.target_group'],['text','target_group'],['text','target_group']]
    df = pd.DataFrame()
    for i, url in enumerate(dataset_dict['urls']):
        temp = pd.read_parquet(url)[columns[i]]
        temp.columns = ['text','target']
        if i == 2:
            temp.loc[:,'text'] = [t[2:-1] for t in temp.loc[:,'text']]
        df = pd.concat([df,temp])
    return df
    
def download_mathew_2021(dataset_dict):
    data = requests.get(dataset_dict['urls'][0]).json()
    all_rows = []
    for k, v in data.items():
        text_ = ' '.join(v['post_tokens'])
        targets_ = [l['target'] for l in v['annotators']]
        all_rows.append([text_]+targets_)
    df = pd.DataFrame(all_rows, columns=['text','target_1','target_2','target_3'])
    
    temp_ = []
    for i, row in df.iterrows():
        for col in ['target_1','target_2','target_3']:
            if len(row[col]) == 1:
                if row[col][0] == 'None':
                    continue
                else:
                    temp_.append([row['text'],row[col][0]])
            else:
                for t in row[col]:
                    temp_.append([row['text'],t])
    return pd.DataFrame(temp_, columns=['text','target'])
    
def check_requirements(dataset_name, dataset_dict, hf_token=None):
    # given requirements specified in dataset_dicts, check whether requirements for dataset are fulfilled
    match dataset_dict['requirement']:
        case 'hf_token':
            if type(hf_token) == str:
                if hf_token.startswith('hf_'):
                    try:
                        login(hf_token)
                        print(f'\t{dataset_name} - Huggingface login successful.')
                        return True
                    except:
                        print(f'\t{dataset_name} unavailable - Please provide a valid huggingface token.')
                        return False
                else:
                    print(f'\t{dataset_name} unavailable - Please provide a valid huggingface token.')
                    return False
            else:
                print(f'\t{dataset_name} unavailable - No huggingface token found. Please provide a valid huggingface token.')
                return False
        case 'dataset_upload':
            if os.path.exists('input_folder/'+dataset_dict['filename']+'.zip'):
                print(f'\t{dataset_name} - Manual dataset upload successful.')
                return True
            else:
                print(f'\t{dataset_name} unavailable - Required dataset {dataset_dict["filename"]+".zip"} not found. Please check instructions and manually upload the dataset to the input_folder in the current working directory.')
                return False
        case _:
            return True