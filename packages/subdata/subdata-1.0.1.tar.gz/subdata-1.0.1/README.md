### Library Description
We develop the subdata Python library as a central resource for researchers interested in evaluating the alignment of LLMs with human perspectives on downstream NLP tasks. While a number of approaches exist that test whether a fine-tuned or instruction-tuned LLM consistently mirrors and thus represents different human individuals or subgroups, there is no such approach and resource for testing the alignment directly where it oftentimes truly matters in NLP: the downstream (annotation) task. In essence, the subdata library allows easy access to a number of datasets suitable for evaluating whether a LLM replicates the same annotation effects as expected or observed from human annotators. Crucially, we not just facilitate the download of single datasets, but rather allows researchers to pick, choose, and combine exactly and only those instances relevant to them from a broad range of available datasets. While the current state of the subdata library is limited to the construct of hate speech and an approach for the evaluation of alignment briefly introduced below and in our corresponding paper **SubData: A Python Library to Collect and Combine Datasets for Evaluating LLM Alignment on Downstream Tasks** (link to preprint coming soon), we aim to extend its scope to more (subjective) constructs and tasks and to introduce additional approaches for measuring the LLM alignment with different human perspectives.

We welcome any suggestions for further datasets that should be included or possible extensions of the library's functionality. We are also very interested in any exchange and inspiration on everything related to LLM subjectivity and the alignment of LLMs with different human perspectives, so please reach out if you would like to have a friendly chat on the topic. 

### Installation
We make the library available via PyPi: https://pypi.org/project/subdata/. It can thus be conveniently installed via `pip install subdata`. 

### Functionality
In the following, we explain the core functionality of the subdata library. Most importantly, the functions *create_target_dataset* and *create_category_dataset* allow the user to automatically download, process and combine instances targeted at a specified target group or category from different data sources into a single dataset, using a standardized mapping from keywords to target and a unified taxonomy. The functions *get_target_info* and *get_category_info* may be consulted before the call to create the actual dataset, as they provide the info on the number of instances and data sources available for the specified target groups or categories.

In addition to the library's core functionality, we took care to implement the possibility to modify the resources we provide, namely, the mapping from keywords found in the original datasets to target groups and the assignment of target groups into categories. The functions *update_mapping_specific* and *update_mapping_all* allow to map a set of keywords to another target group, either for a single dataset or across all datasets. The function *add_target* allows to introduce a new target group altogether, while the function *update_taxonomy* allows to move target groups from one category to another as well as to even create new categories, assigning multiple existing target groups into the new category. Lastly, the function *update_overview* should be called after any modification to the mapping or the taxonomy is done in order to update the overview used internally to combine the requested dataset when calling *create_target_dataset* or *create_category_dataset*.

#### Dataset Creation and Access

`create_target_dataset`
  - input: target (str), mapping_name (str, default 'original'), overview_name (str, default 'original', hf_token (str, default None)
  - takes a valid target, downloads, processes and combines all available datasets for the target and returns a single dataset df with text, target and source columns. some datasets are only available if providing a valid huggingface token or uploading the raw data to input_folder. uses the specified mapping, taxononmy and overview for the creation of the dataset, defaulting to the original versions.
  - output: target_dataset (df) 

`create_category_dataset`
  - input: category (str), mapping_name (str, default 'original'), taxonomy_name (str, default 'original', overview_name (str, default 'original'), hf_token (str, default None)
  - takes a valid category, downloads, processes and combines all available datasets for the targets in that category and returns a single dataset df with text, target and source columns. some datasets are only available if providing a valid huggingface token or uploading the raw data to input_folder. uses the specified mapping, taxononmy and overview for the creation of the dataset, defaulting to the original versions.
  - output: target_dataset (df)

`get_target_info`
  - input: target (str), overview_name (str, default 'original')
  - takes a valid target and returns an overview of the datasets from which the target is available, the number of instances for the target in the dataset as well as the access requirements for the dataset. if the dataset is not readily available there is also information on how to access the dataset. uses the specified overview for the provided information, defaulting to the original version.
  - output: none

`get_category_info`
  - input: category (str), overview_name (str, default 'original'), taxonomy_name (str, default 'original')
  - takes a valid category and returns an overview of the targets and the corresponding number of instances within the category, an overview of the datasets from which the targets are available and the corresponding number of instances per dataset, as well as the access requirements for the dataset. if the dataset is not readily available there is also information on how to access the dataset. uses the specified taxonomy and overview for the provided information, defaulting to the original versions.
  - output: none

#### Taxonomy Customization

`update_taxonomy`
  - input: taxonomy_change ({target: (old_category, new_category)}), taxonomy_name (str, default 'modified')
  - updates the specified taxonomy (either newly created if taxonomy_name non-existent or updating if taxonomy_name already created earlier), moving the specified target from old_category to new_category. if new_category == None, then the target will effectively be removed from the updated taxonomy. if new_category (str) not found in specified taxonomy, a new category with name new_category will be added to the updated taxonomy. e.g., {'jews': ('religion', 'race')} will move target 'jews' from category 'religion' to category 'race'. e.g., {'jews': ('religion', None)} will remove target 'jews' from taxonomy. e.g., {'jews': ('religion', 'relevant'), 'blacks': ('race', 'relevant')} will move targets 'jews' and 'blacks' into newly created category 'relevant'.
  - output: taxonomy_dict (dict)

`add_target`
  - input: target (str), target_category (str), target_keywords [list of str], mapping_name (str, default 'modified'), taxonomy_name (str, default 'modified')
  - creates a new target and moves it into specified target_category for the specified taxonomy (either newly created if taxonomy_name non-existent or updating if taxonomy_name already created earlier), mapping all original keywords specified in target_keywords to the new target for the specified mapping (either newly created if mapping_name non-existent or updating if mapping_name already created earlier). the target_category and target_keywords must already be existing - please refer to the taxonomy and the mapping to identify a valid target_category and valid target_keywords. e.g., target='disabled_general', target_category='disability', target_keywords=['disabled_unspecified','disabled','disabled_other'] creates new target 'disabled_general' in category 'disability' and maps the specified keywords to the newly created target.
  - output: mapping_dict (dict)

`show_taxonomy`
- input: taxonomy_name (str, default 'original'), target_categories (str=='all' or list, default 'all'), export_json (bool, default True), export_latex (bool, default True)
- returns the specified taxonomy. if target_categories == 'all', all categories included in the taxonomy will be returned, otherwise only the categories listed in target_categories will be returend. saves the taxonomy in json-format if export_json == True and as a latex-table in a txt-file if export_latex == True.
- output: taxonomy_dict (dict)   

#### Mapping Modification

`update_mapping_specific`
  - input: mapping_change ({dataset_name: {key_original: value_new}}), mapping_name (str, default 'modified')
  - updates the specified mapping (either new ly created if mapping_name non-existent or updating if mapping_name already created earlier) per dataset according to the provided dictionary. referring to the original mapping, users may map the key_original found in the original dataset_name to new targets (value_new). e.g., {'fanton_2021': {'POC': 'blacks'}} would map instances in dataset 'fanton_2021' that have the key_original 'POC' to value_new 'blacks' (originally, these are mapped to 'race_unspecified'). stores the resulting mapping with name 'mapping_name'. requires existing key_original (keys in original datasets) and value_new (targets) - refer to original mapping to identify valid values.
  - output: mapping_dict (dict) 

`update_mapping_all`
  - input: mapping_change ({key_original: value_new}), mapping_name (str, default 'modified')
  - updates the specified mapping (either newly created if mapping_name non-existent or updating if mapping_name already created earlier) across datasets according to the provided dictionary. referring to the original mapping, users may map the key_original found in different datasets to new targets (value_new). e.g., {'africans': 'origin_unspecified'} would map instances in any dataset that have the key_original 'africans' to value_new 'origin_unspecified' (originally, these are mapped to 'blacks'). stores the resulting mapping with name 'mapping_name'. requires existing key_original (keys in original datasets) and value_new (targets) - refer to original mapping to identify valid values.
  - output: mapping_dict (dict) 

`show_mapping`
- input: mapping_name (str, default 'original'), datasets (str=='all' or list, default 'all'), export_json (bool, default True), export_latex (bool, default True)
- returns the specified mapping. if datasets == 'all', the individual mappings for all datasets included in the mapping will be returned, otherwise only the individual mappings of the datasets listed in datasets will be returend. saves the mappings in json-format if export_json == True and as individual latex-tables in a txt-file if export_latex == True.
- output: mapping_dict (dict)

#### Dataset Overview

`update_overview`
  - input: overview_name (str, default 'modified'), mapping_name (str, default 'modified'), taxonomy_name (str, defaut 'modified'), hf_token (str, default None)
  - updates the overview that informs the get_info and create_dataset functions and stores the new overview with name overview_name. uses the mapping and taxonomy provided via mapping_name and taxonomy_name to create the updated overview. internally, the function tries to access all datasets to create the full overview, thus requiring a hf_token and the manual upload of relevant datasets into input_folder to consider all available datasets. function should be called after any operation that modifies the mapping or the taxonomy.

`show_overview`
- input: overview_name (str, default 'original'), taxonomy_name (str, default 'original'), export_json (bool, default True), export_latex (bool, default True)
- returns the specified overview based on the specified taxonomy. saves the overview in json-format if export_json == True and as a latex-table in a txt-file if export_latex == True.
- output: overview_dict (dict) 

### Original Mapping
The following tables document the original mapping that is used in the subdata library to map the target keywords found in the original datasets to a single taxonomy of target groups. In creating this mapping, we tried to strike a delicate balance between being as precise and specific as possible while keeping the resulting target groups still sufficiently general. Whenever multiple datasets used similar specific target groups, we also introduced the corresponding target group (e.g., disabled_mental). When a dataset used a keyword without mentioning the target group more specifically, we mapped it into a more general target group introduced for each category (e.g., disabled_unspecified). 

For the mapping, most of the decisions taken were rather straightforward and little contested, e.g., it seems logical to map both the target “JEWS” found in one dataset and the target “jewish people” found in another dataset to the single target “jews”. However, some decisions were more complicated. Whether the target “africans” should be mapped to the target “blacks” or to the target “africans”, thus interpreting it as a question of origin rather than one of race, might never be definitely determined. In such cases, we tried to consult the publication corresponding to the dataset to see whether the original creators of the resource specifically mentioned one of the potential meanings. If so, we followed their example, and if not, we tried to apply reasonable judgment and be consistent throughout the mapping.

However, we emphasize that we do not consider the mapping proposed here to be the ultimate and objective single true mapping, but would like to encourage researchers to see this mapping as a starting point and modify it to their needs and desires. For this purpose, we implemented all necessary functionality directly in the subdata library. 

Fanton et al. (2021)
|keyword|target|
|---|---|
|DISABLED|disabled_unspecified|
|JEWS|jews|
|LGBT+|lgbtq_unspecified|
|MIGRANTS|migrants|
|MUSLIMS|muslims|
|POC|race_unspecified|
|WOMEN|women|


Hartvigsen et al. (2022)
|keyword|target|
|---|---|
|asian|asians|
|asian folks|asians|
|black|blacks|
|black folks / african-americans|blacks|
|black/african-american folks|blacks|
|chinese|chinese|
|chinese folks|chinese|
|folks with mental disabilities|disabled_mental|
|folks with physical disabilities|disabled_physical|
|jewish|jews|
|jewish folks|jews|
|latino|latinx|
|latino/hispanic folks|latinx|
|lgbtq|lgbtq_unspecified|
|lgbtq+ folks|lgbtq_unspecified|
|mental_dis|disabled_mental|
|mexican|mexicans|
|mexican folks|mexicans|
|middle eastern folks|middle_eastern|
|middle_east|middle_eastern|
|muslim|muslims|
|muslim folks|muslims|
|native american folks|native_americans|
|native american/indigenous folks|native_americans|
|native_american|native_americans|
|phsycial_dis|disabled_physical|
|women|women|


Jigsaw et al. (2019)
|keyword|target|
|---|---|
|asian|asians|
|atheist|atheists|
|bisexual|bisexuals|
|black|blacks|
|buddhist|buddhists|
|christian|christians|
|female|women|
|heterosexual|heterosexuals|
|hindu|hindus|
|homosexual_gay_or_lesbian|homosexuals|
|intellectual_or_learning_disability|disabled_intellectual|
|jewish|jews|
|latino|latinx|
|male|men|
|muslim|muslims|
|other_disability|disabled_unspecified|
|other_gender|gender_unspecified|
|other_race_or_ethnicity|race_unspecified|
|other_religion|religion_unspecified|
|other_sexual_orientation|sexuality_unspecified|
|physical_disability|disabled_physical|
|psychiatric_or_mental_illness|disabled_mental|
|transgender|transgenders|
|white|whites|


Jikeli et al. (2023)
|keyword|target|
|---|---|
|Israel|jews|
|Jews|jews|
|Kikes|jews|
|ZioNazi|jews|


Jikeli et al. (2023)
|keyword|target|
|---|---|
|Asians|asians|
|Blacks|blacks|
|Jews|jews|
|Latinos|latinx|
|Muslims|muslims|


Mathew et al. (2021)
|keyword|target|
|---|---|
|African|blacks|
|Arab|arabs|
|Asexual|asexuals|
|Asian|asians|
|Bisexual|bisexuals|
|Buddhism|buddhists|
|Caucasian|whites|
|Christian|christians|
|Disability|disabled_unspecified|
|Heterosexual|heterosexuals|
|Hindu|hindus|
|Hispanic|latinx|
|Homosexual|homosexuals|
|Indian|indians|
|Indigenous|indigenous|
|Islam|muslims|
|Jewish|jews|
|Men|men|
|Nonreligious|atheists|
|Refugee|refugees|
|Women|women|


Röttger et al. (2021)
|keyword|target|
|---|---|
|Muslims|muslims|
|black people|blacks|
|disabled people|disabled_unspecified|
|gay people|homosexuals|
|immigrants|migrants|
|trans people|transgenders|
|women|women|


Sachdeva et al. (2022)
|keyword|target|
|---|---|
|target_age_children|young_aged|
|target_age_middle_aged|middle_aged|
|target_age_other|age_unspecified|
|target_age_seniors|seniors|
|target_age_teenagers|young_aged|
|target_age_young_adults|middle_aged|
|target_disability_cognitive|disabled_intellectual|
|target_disability_hearing_impaired|disabled_unspecified|
|target_disability_neurological|disabled_mental|
|target_disability_other|disabled_unspecified|
|target_disability_physical|disabled_physical|
|target_disability_unspecific|disabled_unspecified|
|target_disability_visually_impaired|disabled_unspecified|
|target_gender_men|men|
|target_gender_non_binary|non_binary|
|target_gender_other|gender_unspecified|
|target_gender_transgender_men|transgenders|
|target_gender_transgender_unspecified|transgenders|
|target_gender_transgender_women|transgenders|
|target_gender_women|women|
|target_origin_immigrant|migrants|
|target_origin_migrant_worker|migrants|
|target_origin_other|origin_unspecified|
|target_origin_specific_country|origin_unspecified|
|target_origin_undocumented|undocumented|
|target_race_asian|asians|
|target_race_black|blacks|
|target_race_latinx|latinx|
|target_race_middle_eastern|middle_eastern|
|target_race_native_american|native_americans|
|target_race_other|race_unspecified|
|target_race_pacific_islander|pacific_islanders|
|target_race_white|whites|
|target_religion_atheist|atheists|
|target_religion_buddhist|buddhists|
|target_religion_christian|christians|
|target_religion_hindu|hindus|
|target_religion_jewish|jews|
|target_religion_mormon|mormons|
|target_religion_muslim|muslims|
|target_religion_other|religion_unspecified|
|target_sexuality_bisexual|bisexuals|
|target_sexuality_gay|homosexuals|
|target_sexuality_lesbian|homosexuals|
|target_sexuality_other|sexuality_unspecified|
|target_sexuality_straight|heterosexuals|


Vidgen et al. (2021)
|keyword|target|
|---|---|
|asexual people|asexuals|
|black men|blacks,men|
|black people|blacks|
|catholics|christians|
|chinese women|chinese,women|
|christians|christians|
|communists|communists|
|conservatives|conservatives|
|democrats|democrats|
|donald trump supporters|republicans|
|elderly people|seniors|
|ethnic minorities|race_unspecified|
|feminists (male)|men|
|gay men|homosexuals|
|gay people|homosexuals|
|hindus|hindus|
|illegal immigrants|undocumented|
|immigrants|migrants|
|jewish people|jews|
|latinx|latinx|
|left-wing people|left-wingers|
|left-wing people (far left)|left-wingers|
|left-wing people (social justice)|left-wingers|
|lgbtqa community|sexuality_unspecified|
|liberals|liberals|
|men|men|
|mixed race/ethnicity|race_unspecified|
|muslims|muslims|
|non-gender dysphoric transgender people|sexuality_unspecified|
|non-masculine men|men|
|non-white people|race_unspecified|
|people from africa|blacks|
|people from britain|brits|
|people from china|chinese|
|people from india|indians|
|people from mexico|mexicans|
|people from pakistan|pakistani|
|people with aspergers|disabled_mental|
|people with autism|disabled_mental|
|people with cerebral palsy|disabled_unspecified|
|people with disabilities|disabled_unspecified|
|people with down's syndrome|disabled_intellectual|
|people with mental disabilities|disabled_mental|
|people with physical disabilities|disabled_physical|
|republicans|republicans|
|right-wing people|right-wingers|
|right-wing people (alt-right)|right-wingers|
|sexual and gender minorities|sexuality_unspecified|
|transgender people|transgenders|
|white men|whites,men|
|white people|whites|
|white women|whites,women|
|women|women|
|young people|young_aged|


Vidgen et al. (2021)
|keyword|target|
|---|---|
|african|blacks|
|arab|arabs|
|arab, ref|arabs,refugees|
|asi|asians|
|asi.chin|chinese|
|asi.east|asians|
|asi.man|asians,men|
|asi.pak|pakistani|
|asi.south|asians|
|asi.wom|asians,women|
|asylum|refugees|
|bis|bisexuals|
|bla|blacks|
|bla, african|blacks|
|bla, hispanic|blacks,latinx|
|bla, immig|blacks,migrants|
|bla, jew|blacks,jews|
|bla, jew, non.white|blacks,jews|
|bla, mixed.race|blacks|
|bla, non.white|blacks|
|bla, wom|blacks,women|
|bla.man|blacks,men|
|bla.wom|blacks,women|
|dis|disabled_unspecified|
|dis, bla|disabled_unspecified,blacks|
|dis, gay|disabled_unspecified,homosexuals|
|dis, trans|disabled_unspecified,transgenders|
|dis, wom|disabled_unspecified,women|
|eastern.europe|eastern_european|
|for|migrants|
|for, immig|migrants|
|gay|homosexuals|
|gay, bis|homosexuals,bisexuals|
|gay, gay.wom|homosexuals|
|gay.man|homosexuals|
|gay.wom|homosexuals|
|gay.wom, gay.man|homosexuals|
|gendermin|gender_unspecified|
|hispanic|latinx|
|immig|migrants|
|immig, hispanic|migrants,latinx|
|immig, non.white|migrants|
|immig, ref|migrants,refugees|
|indig|indigenous|
|indig.wom|indigenous,women|
|jew|jews|
|jew, non.white|jews|
|lgbtq|lgbtq_unspecified|
|mixed.race|race_unspecified|
|mixed.race, non.white|race_unspecified|
|mus|muslims|
|mus, arab|muslims|
|mus, immig|muslims,migrants|
|mus, jew|muslims,jews|
|mus, ref|muslims,refugees|
|mus.wom|muslims,women|
|non.white.wom|women|
|old.people|seniors|
|pol|polish|
|ref|refugees|
|russian|russians|
|trans|transgenders|
|trans, gay|transgenders,homosexuals|
|trans, gay.wom, gay.man, bis|transgenders,homosexuals,bisexuals|
|trans, gendermin|transgenders|
|trans, wom|transgenders|
|wom|women|

### Original Taxonomy

The following tables document the original taxonomy that is used in the subdata library to assign target groups into categories. 

For the taxonomy, again, most of the choices were uncontested and in line with the way that some of the original datasets assign targets to certain categories. However, there are some critical decisions we had to take. Least resolvable is probably the observation that many datasets feature an LGBTQ+ target group that is not further specified, thus mixing together both gender identities and sexual preferences. In most of those datasets, this LGBTQ+ target group ended up as part of a category called Sexuality or Sexual Orientation. We are aware that by mirroring this decision we are also replicating the confusion of gender identity and sexual preference, however, there is no real alternative for our taxonomy since we are unable to divide apart the different components of this rather unspecific target group found in the original datasets. We highlight the heterogeneity of this target group by appending _unspecified_ to the name of the target group, and, wherever we can, by mapping specific gender identity and sexual preference target groups into their correct categories (i.e., gender and sexuality). 

However, we emphasize that we do not consider the taxonomy proposed here to be the ultimate and objective single true taxonomy, but would like to encourage researchers to see this taxonomy as a starting point and modify it to their needs and desires. For this purpose, we implemented all necessary functionality directly in the subdata library. 

|age|disabled|gender|migration|origin|political|race|religion|sexuality|
|---|---|---|---|---|---|---|---|---|
|middle_aged|disabled_intellectual|men|migrants|arabs|communists|asians|atheists|asexuals|
|seniors|disabled_mental|non_binary|refugees|brits|conservatives|blacks|buddhists|bisexuals|
|young_aged|disabled_unspecified|transgenders|undocumented|chinese|democrats|indigenous|christians|heterosexuals|
|age_unspecified||women|migration_unspecified|eastern_european|left-wingers|latinx|hindus|homosexuals|
|||gender_unspecified||indians|liberals|native_americans|jews|lgbtq_unspecified|
|||||mexicans|republicans|pacific_islanders|mormons|sexuality_unspecified|
|||||middle_eastern|right-wingers|whites|muslims||
|||||pakistani|political_unspecified|race_unspecified|religion_unspecified||
|||||polish|||||
|||||russians|||||
|||||origin_unspecified|||||
