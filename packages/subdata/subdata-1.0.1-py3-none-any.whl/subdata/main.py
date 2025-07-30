### 'create_target_dataset(target {hf_token})' is a function that creates the dataset for the requested target.

### 'create_category_dataset(category {h_token})' is a function that creates the dataset for the requested category.

import json
import numpy as np
import os
import pandas as pd

import importlib.resources

from subdata.download import download_datasets
from subdata.process import process_datasets
from subdata.utils import load_overview, load_mapping, load_taxonomy, load_instruction

if not os.path.exists('input_folder'):
    os.mkdir('input_folder')    


def create_target_dataset(target, mapping_name='original', overview_name='original', hf_token=None):

    overview_dict = load_overview(overview_name)

    if target not in list(set(overview_dict.keys())):
        print(f'{target} is not a valid target. Please refer to the taxonomy to specify a valid target.')
    
    relevant_datasets = [dataset[0] for dataset in overview_dict[target]]
    dict_of_datasets = download_datasets(relevant_datasets, hf_token)
    dict_of_processed_datasets = process_datasets(dict_of_datasets, mapping_name)
    target_dataset = pd.DataFrame()
    for df in dict_of_processed_datasets.values():
        target_dataset = pd.concat([target_dataset, df[df['target']==target]])
    
    return target_dataset

def create_category_dataset(category, mapping_name='original', taxonomy_name='original', overview_name='original', hf_token=None):

    overview_dict = load_overview(overview_name)
    taxonomy_dict = load_taxonomy(taxonomy_name)

    if category not in list(set(taxonomy_dict.keys())):
        print(f'{category} is not a valid category. Please refer to the taxonomy to specify a valid category.')
    
    targets = taxonomy_dict[category]
    relevant_datasets = list(set([dataset[0] for target in targets for dataset in overview_dict[target]]))
    dict_of_datasets = download_datasets(relevant_datasets, hf_token)
    dict_of_processed_datasets = process_datasets(dict_of_datasets, mapping_name)
    target_dataset = pd.DataFrame()
    for df in dict_of_processed_datasets.values():
        target_dataset = pd.concat([target_dataset, df[df['target'].isin(targets)]])
        
    return target_dataset



### 'get_target_info(target)' is a function that identifies the relevant datasets for a specific target group, using the information provided in 'overview_dict.json'. It prints out the number of available instances across the different datasets, informing about any requirements associated with accessing the data using the information available in 'instruction_dict.json'.

### 'get_category_info(category)' is a function that identifies the relevant datasets for a target category, using the information provided in 'overview_dict.json'. It prints out the number of available instances for the different target groups contained in the category as well as across the different datasets, informing about any requirements associated with accessing the data using the information available in 'instruction_dict.json'.


def get_target_info(target, overview_name='original'):

    instruction_dict = load_instruction()
    overview_dict = load_overview(overview_name)  

    if target not in list(set(overview_dict.keys())):
        print(f'{target} is not a valid target. Please refer to the taxonomy to specify a valid target.')
    
    relevant_datasets = overview_dict[target]
    n_total = np.sum([dataset[1] for dataset in relevant_datasets])
    print(f'{n_total:,} instances from {len(relevant_datasets)} datasets available for target_group {target}.')
    for dataset in relevant_datasets:
        instruction = instruction_dict[dataset[0]] if dataset[0] in list(instruction_dict.keys()) else 'available'
        print(f'\t{dataset[0].ljust(25)}\t{dataset[1]:,}\t{instruction}')
        
def get_category_info(category, overview_name='original', taxonomy_name='original'):

    instruction_dict = load_instruction()
    overview_dict = load_overview(overview_name) 
    taxonomy_dict = load_taxonomy(taxonomy_name)

    if category not in taxonomy_dict.keys():
        print(f'{category} is not a valid category. Please refer to the taxonomy to specify a valid category.')
    
    relevant_datasets = [dataset for target in taxonomy_dict[category] for dataset in overview_dict[target]]
    unique_datasets = list(set([dataset[0] for dataset in relevant_datasets]))
    targets = taxonomy_dict[category]
    
    targets_sums = {target: None for target in targets}
    for target in targets:
        targets_sums[target] = np.sum([dataset[1] for dataset in overview_dict[target]])
    n_total = np.sum([count for count in targets_sums.values()])
   
    print(f'{n_total:,} instances across {len(targets)} target groups from {len(unique_datasets)} datasets available.')
    for target, n_target in targets_sums.items():
        print(f'\t{target.ljust(20)}\t{n_target:,}')
    print('___________________________________________________________________________________')
    
    datasets_sums = {dataset: [] for dataset in unique_datasets}
    for dataset in relevant_datasets:
        datasets_sums[dataset[0]].append(dataset[1])

    print('Dataset overview:')
    for dataset, n_dataset in datasets_sums.items():
        instruction = instruction_dict[dataset] if dataset in list(instruction_dict.keys()) else 'available'
        print(f'\t{dataset.ljust(25)}\t{np.sum(n_dataset):,}\t{instruction}')