import json
import os
import pandas as pd

import importlib.resources

from subdata.download import download_datasets
from subdata.process import process_datasets
from subdata.utils import load_mapping, load_taxonomy, load_overview, load_download, save_modified_resource, taxonomy_to_latex, mapping_to_latex, overview_to_latex, save_latex


### function to update the mapping from dataset keys to targets for a single, specified dataset
# input {dataset: {key_original: value_new}} to change mapping from dataset-specific key to new target (value_new) (only for this dataset)

def update_mapping_specific(mapping_change, mapping_name='modified'):

    if mapping_name.lower() == 'original':
        print(f'Please choose another name for the new mapping. {mapping_name} is not allowed.')
        return None
        
    mapping_dict = load_mapping(mapping_name)

    valid_targets = [e for t in list(set([v for k_,d in mapping_dict.items() for k,v in d.items()])) for e in t.split(',')] # trust the process
    changes = []
    
    for dataset, change in mapping_change.items():
        if dataset not in mapping_dict.keys():
            print(f'{dataset} not a valid dataset name. Please refer to the dataset overview to identify the spelling and format of valid datasets.')
            continue
        for key_original, value_new in change.items():
            if value_new not in valid_targets:
                print(f'{value_new} is not a valid target name. Please refer to the original mapping to identify the spelling and format of valid targets.')
                continue
            if key_original in mapping_dict[dataset].keys():
                value_old = mapping_dict[dataset][key_original]
                mapping_dict[dataset][key_original] = value_new
                changes.append([dataset, key_original, value_old, value_new])
            else:
                print(f'{key_original} not found as a key in {dataset}-mapping - no change to the mapping has been made. Please refer to the original mapping to identify the spelling and format of valid keys.')

    save_modified_resource(mapping_dict, 'mapping_'+mapping_name)

    if len(changes) > 0:
        print('Overview of mapping changes:')
        for change in changes:
            print(f'\tDataset: {change[0].ljust(20)} Key: {change[1].ljust(20)} Old Value: {change[2].ljust(20)} New Value: {change[3]}')
    else:
        print(f'No changes have been made.')
    
    return mapping_dict

### function to update the mapping from dataset keys to targets for all datasets
# input {key_original: value_new} to change mapping from key to new target (value_new) (for all datasets)

def update_mapping_all(mapping_change, mapping_name='modified'):

    if mapping_name.lower() == 'original':
        print(f'Please choose another name for the new mapping. {mapping_name} is not allowed.')
        return None

    mapping_dict = load_mapping(mapping_name)

    valid_targets = [e for t in list(set([v for k_,d in mapping_dict.items() for k,v in d.items()])) for e in t.split(',')] # trust the process
    changes = []
    
    for key_original, value_new in mapping_change.items():
        if value_new not in valid_targets:
            print(f'{value_new} is not a valid target name. Please refer to the original mapping to identify the spelling and format of valid targets.')
            continue
        for dataset, dataset_mapping in mapping_dict.items():
            if key_original in dataset_mapping.keys():
                value_old = dataset_mapping[key_original]
                mapping_dict[dataset][key_original] = value_new
                changes.append([dataset, key_original, value_old, value_new])

    save_modified_resource(mapping_dict, 'mapping_'+mapping_name)
    
    if len(changes) > 0:
        print('Overview of mapping changes:')
        for change in changes:
            print(f'\tDataset: {change[0].ljust(20)} Key: {change[1].ljust(20)} Old Value: {change[2].ljust(20)} New Value: {change[3]}')
    else:
        print(f'No changes have been made.')

    return mapping_dict

# input {target: (old_category, new_category)} to move target from old_category to new_category. 
# if new_category == None, then target will effectively be removed from taxonomy
# if new_category not in existing taxonomy, a new category of targets will be added

def update_taxonomy(taxonomy_change, taxonomy_name='modified'):

    if taxonomy_name.lower() == 'original':
        print(f'Please choose another name for the new taxonomy. {taxonomy_name} is not allowed.')
        return None

    taxonomy_dict = load_taxonomy(taxonomy_name)

    changes = []

    for target, change in taxonomy_change.items():
        old_category, new_category = change[0], change[1]
        
        if old_category not in taxonomy_dict.keys():
            print(f'{old_category} is not a valid category. Please refer to the original taxonomy to specify a valid original category.')
            continue

        if new_category not in taxonomy_dict.keys():
            taxonomy_dict[new_category] = []
            print(f'{new_category} is a new category. A category named {new_category} has been added to the taxonomy.')
        
        if target in taxonomy_dict[old_category]:
            taxonomy_dict[old_category].remove(target)
            taxonomy_dict[new_category].append(target)
            changes.append([target, old_category, new_category])
        else:
            print(f'{target} not found in original category {old_category}. Please refer to the original taxonomy to specify the correct original category and/or a valid target.')

    save_modified_resource(taxonomy_dict, 'taxonomy_'+taxonomy_name)
    
    if len(changes) > 0:
        print('Overview of taxonomy changes:')
        for change in changes:
            print(f'\tTarget: {change[0].ljust(20)} Old Category: {change[1].ljust(20)} New Category: {change[2].ljust(20)}')
    else:
        print(f'No changes have been made.')

    return taxonomy_dict


# input:
# - target: str, name of the new target to be added
# - target_category: str, category of the new target to be added (must be existing)
# - target_keywords: [list of str], keywords that map to the new target (must be existing)
# - mapping_name: str, name of the new mapping that is created by adding the target
# - taxonomy_name: str, name of the new taxonomy that is created by adding the target
def add_target(target, target_category, target_keywords, mapping_name='modified', taxonomy_name='modified'):

    mapping_dict = load_mapping(mapping_name)
    taxonomy_dict = load_taxonomy(taxonomy_name)

    if target_category not in taxonomy_dict.keys():
        print(f'{target_category} is not a valid category. Please refer to the taxonomy to specify a valid category.')
        return None

    taxonomy_dict[target_category].append(target)
    print(f'{target} has been successfully added to {target_category} in taxonomy {taxonomy_name}.')

    changes = []

    for target_keyword in target_keywords:
        keyword_dummy = False
        for dataset_name in mapping_dict.keys():
            if not target_keyword in mapping_dict[dataset_name].keys():
                continue
            else:
                keyword_dummy = True
                old_target = mapping_dict[dataset_name][target_keyword]
                mapping_dict[dataset_name][target_keyword] = target
                changes.append([dataset_name, target_keyword, old_target, target])
        if not keyword_dummy:
            print(f'Keyword {target_keyword} does not exist. Please refer to the mapping to specify an existing keyword.')

    save_modified_resource(mapping_dict, 'mapping_'+mapping_name)
    save_modified_resource(taxonomy_dict, 'taxonomy_'+taxonomy_name)
    
    if len(changes) > 0:
        print('Overview of changes in mapping {mapping_name}:')
        for change in changes:
            print(f'\tDataset: {change[0].ljust(20)} Keyword: {change[1].ljust(20)} Old Target: {change[2].ljust(20)} New Target: {change[3].ljust(20)}')
    else:
        print(f'No changes have been made.')

    return mapping_dict


# input: {taxonomy_name='original', target_categories='all', export=True} the name of the taxonomy to display and the target categories to include; includes all categories if target_categories=='all', else expects list of categories to include; exports .json if export_json==True and .txt with latex-table if export_latex==True
# returns the requested taxonomy

def show_taxonomy(taxonomy_name='original', target_categories='all', export_json=True, export_latex=True):

    taxonomy = load_taxonomy(taxonomy_name)

    if target_categories != 'all':
        taxonomy_out = {}
        for target_category in target_categories:
            if target_category in taxonomy.keys():
                taxonomy_out[target_category] = taxonomy[target_category]
    else:
        taxonomy_out = taxonomy.copy()

    if export_json == True:
        save_modified_resource(taxonomy_out, 'taxonomy_'+taxonomy_name)

    if export_latex == True:
        taxonomy_latex = taxonomy_to_latex(taxonomy_out)
        save_latex(taxonomy_latex, 'taxonomy_'+taxonomy_name)

    return taxonomy_out


# input: {mapping_name='original', datasets='all', export=True} the name of the mappings to display and the datasets to include; includes all datasets if datasets=='all', else expects list of datasets to include; exports .json if export_json==True and .txt with latex-table if export_latex==True
# returns the requested taxonomy

def show_mapping(mapping_name='original', datasets='all', export_json=True, export_latex=True):

    mapping = load_mapping(mapping_name)

    if datasets != 'all':
        mapping_out = {}
        for dataset in datasets:
            if dataset in mapping.keys():
                mapping_out[dataset] = mapping[dataset]
    else:
        mapping_out = mapping.copy()

    if export_json == True:
        save_modified_resource(mapping_out, 'mapping_'+mapping_name)

    if export_latex == True:
        mapping_latex = mapping_to_latex(mapping_out)
        save_latex(mapping_latex, 'mapping_'+mapping_name)

    return mapping_out


# input: {overview_name='original', export_json=True, export_latex=True} the name of the overview; exports .json if export_json==True and .txt with latex-table if export_latex==True
# returns the requested overview

def show_overview(overview_name='original', taxonomy_name='original', export_json=True, export_latex=True):

    overview = load_overview(overview_name)

    if export_json == True:
        save_modified_resource(overview, 'overview_'+overview_name)

    if export_latex == True:
        overview_latex = overview_to_latex(overview, taxonomy_name)
        save_latex(overview_latex, 'overview_'+overview_name)

    return overview


# input: {overivew_name='modified', mapping_name='modified', taxonomy_name='modified'} the name of the overview to generate and the names of the (modified) taxonomy and mapping to use for the creation of the overview. (if both mapping and taxonomy are 'original' the call will never lead to changes since a modified mapping and taxonomy can never be named original)
# creates an overview using all available datasets

def create_overview_dict(df_overview):
    
    dict_overview = {k: [] for k in df_overview['target']}
    
    for i, row in df_overview.iterrows():
        for i_dataset, n_targets in enumerate(row[2:]):
            if n_targets > 0:
                dict_overview[row.iloc[1]].append((list(df_overview.columns)[i_dataset+2],n_targets))
                
    return dict_overview

### requires user to specify the name of the mapping and taxonomy to be used. defaults to 'modified' for both.
def update_overview(overview_name='modified', mapping_name='modified', taxonomy_name='modified', hf_token=None):

    if overview_name.lower() == 'original':
        print('Please choose another name for the new overview. "original" is not allowed.')
        return None

    taxonomy_dict = load_taxonomy(taxonomy_name)
    download_dict = load_download()

    list_of_dataset_names = [k for k in download_dict.keys()]
    dict_of_datasets = download_datasets(list_of_dataset_names, hf_token)
    dict_of_processed_datasets = process_datasets(dict_of_datasets, mapping_name)    
    
    df_overview = pd.DataFrame({
        'category': [category for category, target_groups in taxonomy_dict.items() for t in target_groups],
        'target': [t for category, target_groups in taxonomy_dict.items() for t in target_groups]
    })
    
    for dataset_name in list_of_dataset_names:
        if not dataset_name in dict_of_processed_datasets.keys():
            continue
        df = dict_of_processed_datasets[dataset_name]
        n_targets = []
        for category, target_groups in taxonomy_dict.items():
            for target_group in target_groups:
                n_targets.append(len(df[df['target']==target_group]))
        df_overview[dataset_name] = n_targets

    overview_dict = create_overview_dict(df_overview)

    save_modified_resource(overview_dict, 'overview_'+overview_name)
    
    return df_overview