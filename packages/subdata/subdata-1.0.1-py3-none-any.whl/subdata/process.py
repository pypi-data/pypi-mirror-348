### 'process_datasets(dict_of_datasets)' is a function that processes the datasets found in the provided input dict_of_datasets. The information on how the datasets are to be processed is found in 'process_dict.json'.

### 'process_single_column(df, dataset_dict)' is a helper function that processes datasets where the target info is stored in a single column (via a single category variable with the different targets as the different options). It uses the information on how a dataset is to be processed and how old target names are to be mapped to new target names stored in 'process_dict.json'.

### 'process_multi_columns(df, dataset_dict)' is a helper function that processes datasets where the target info is stored in multiple columns (via a series of target-specific dummy-variables). It uses the information on how a dataset is to be processed and how old target names are to be mapped to new target names stored in 'process_dict.json'.

import json
import numpy as np
import pandas as pd
import time

import importlib.resources

from subdata.utils import load_mapping, load_process

def process_datasets(dict_of_datasets, mapping_name='original'):

    mapping_dict = load_mapping(mapping_name)
    process_dict = load_process()

    print(f'Starting to process {len(dict_of_datasets.keys())} datasets.')

    dict_of_processed_datasets = {}
    
    for dataset_name, df in dict_of_datasets.items():
        
        start_time = time.time()
        
        dataset_dict = process_dict[dataset_name]
        dataset_dict['mapping'] = mapping_dict[dataset_name]
        
        match dataset_dict['mode']:
            case 'single_column':
                df = process_single_column(df, dataset_dict)
            case 'multi_columns':
                df = process_multi_columns(df, dataset_dict)
                
        df['dataset'] = dataset_name
        dict_of_processed_datasets[dataset_name] = df
        
        print(f'\t{dataset_name} processed in {str(np.round(time.time()-start_time,4)).rjust(10)}s')
                
    return dict_of_processed_datasets
                   
def process_single_column(df, dataset_dict):
    df = df[dataset_dict['columns']]
    df.columns = ['text','target']
    df = df.dropna(subset=['text','target'])
    df.loc[:,'target'] = df.loc[:,'target'].replace(dataset_dict['mapping'])
    df.loc[:,'target'] = [t.split(',') for t in df['target']]
    df = df.explode('target')
    nested = [t.split(',') for t in dataset_dict['mapping'].values()]
    df = df.loc[df['target'].isin(set([t for sublist in nested for t in sublist])),:]
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def process_multi_columns(df, dataset_dict):
    df = df[dataset_dict['columns']+[c for c in dataset_dict['mapping'].keys()]]
    df = df.rename(columns={dataset_dict['columns'][0]: 'text'})
    df_new = pd.DataFrame()
    for k in dataset_dict['mapping'].keys():
        temp = df[df[k]>0]
        temp = pd.DataFrame(list(temp['text']), columns=['text'])
        temp['target'] = k
        df_new = pd.concat([df_new, temp])
    df = df_new
    df.loc[:,'target'] = df.loc[:,'target'].replace(dataset_dict['mapping'])
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df