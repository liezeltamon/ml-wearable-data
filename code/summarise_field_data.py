# Explore download field data from UKBB

# %% Setup
import sys
from pathlib import Path
import pandas as pd
import os
# Add utils/python to the Python path
#sys.path.append(str(Path("~/git/ml-wearable-data/utils/python").expanduser()))
sys.path.append(os.path.join(str(Path(__file__).parent.parent), "utils", "python"))
# Import the env module
from env import find_project_dir
import numpy as np
import ast
import re

#%% Functions

import re
# Function to remove non-alphanumeric characters
def remove_non_alphanumeric(text):
    """
    Remove non-alphanumeric characters from the given text.

    Parameters:
    text (str): The input string from which non-alphanumeric characters will be removed.

    Returns:
    str: The cleaned string with only alphanumeric characters.
    """
    return re.sub(r'[^a-zA-Z0-9]', '', text)

# %% Parameters
proj_dir = find_project_dir(Path(__file__), ".git")
os.chdir(proj_dir)
data_dir = "data"
ukbb_data_path = os.path.join(data_dir, "results_eid.csv")
natmed_disese_mapping_path = os.path.join(data_dir, "schalkamp_disease_code_mapping_disease.csv")
field_ids = {"acc_qc_passed": "90016", 
             "start_requested_wear_period": "90003", 
             "icd10": "41270", 
             "icd9": "41271"}
# %%
ukbb_df = pd.read_csv(ukbb_data_path)
ukbb_cols = [ "p" + field_id for field_id in field_ids.values()]
ukbb_df = ukbb_df[ukbb_cols]
ukbb_df.columns = field_ids.keys()
#ukbb_df['start_requested_wear_period'] = pd.to_datetime(ukbb_df['start_requested_wear_period'])
ukbb_df.head()

# %% Number of participants with good quality wearable data                                                    

# Count the number of participants with good quality wearable data
ukbb_df["with_acc_data"] = ~ukbb_df["start_requested_wear_period"].isna()
print(ukbb_df["with_acc_data"].value_counts())
participant_counts = ukbb_df.groupby(["acc_qc_passed", "with_acc_data"]).size().reset_index(name='counts')
print(participant_counts)

# Check for non-finite values in the 'start_requested_wear_period' column
is_acc_qc_passed = ukbb_df['acc_qc_passed'] == 1
if ukbb_df.loc[is_acc_qc_passed, "start_requested_wear_period"].isna().any():
    print("There are good quality acc with no start_requested_wear_period")
ukbb_acc_qc_passed_df = ukbb_df[is_acc_qc_passed]
ukbb_acc_qc_passed_df.count()
ukbb_acc_qc_passed_df.reset_index(drop=True, inplace=True)
ukbb_acc_qc_passed_df

# %% Number of participants with wearable data per disease
# Classify participants
ukbb_acc_qc_passed_sick_df = ukbb_acc_qc_passed_df[~ukbb_acc_qc_passed_df["icd10"].isna()]
ukbb_acc_qc_passed_sick_df.shape

# %%
is_not_nan = ~ukbb_acc_qc_passed_sick_df["icd10"].isnull()
icd10_lvls = ukbb_acc_qc_passed_sick_df[is_not_nan]["icd10"].str.split(pat=",", expand=True).to_numpy().flatten()
icd10_lvls = [lvl for lvl in icd10_lvls if lvl is not None]
icd10_lvls = np.unique(icd10_lvls)
icd10_lvls = np.array([remove_non_alphanumeric(element) for element in icd10_lvls])
icd10_lvls = sorted(np.unique(icd10_lvls))
print(icd10_lvls)
len(icd10_lvls)

# %%
num_rows = ukbb_acc_qc_passed_df.shape[0]
num_cols = len(icd10_lvls)
disease_arr = np.empty((num_rows, num_cols))
disease_arr.shape

index_array = np.array(icd10_lvls)
for idx in ukbb_acc_qc_passed_sick_df.index.to_list():
    print(idx)
    element = ukbb_acc_qc_passed_sick_df["icd10"].loc[idx]
    try:
        elements = ast.literal_eval(element)
        disease_arr_col_index = np.array([np.where(index_array == el)[0] for el in elements])
        disease_arr[idx, disease_arr_col_index.flatten()] = 1        
    except Exception as e:
        print(f"Error occurred at index {idx}: {e}")
        break

print(disease_arr.shape)
# %%
healthy = np.sum(disease_arr, axis = 1) == 0 # No ICD-10 code for individual
np.unique(healthy, return_counts=True)

# %%
disease_mapping_df = pd.read_csv(natmed_disese_mapping_path)
# Split based on comma and then store as list the ICD 10 codes
disease_mapping_df["disease_codes"] = disease_mapping_df["ICD 10"].str.split(",")
disease_categories = np.unique(disease_mapping_df["disease"].to_numpy())
disease_categories

# %%
disease_categories_arr = np.full((num_rows, len(disease_categories)), np.nan)
disease_categories_arr.shape
np.unique(disease_categories_arr, return_counts=True)

# %%
index_array = np.array(icd10_lvls)
for idx in disease_mapping_df.index.to_list():
    print(idx)
    elements = np.array(disease_mapping_df["disease_codes"].iloc[idx])
    elements = [remove_non_alphanumeric(text) for text in elements]
    elements = np.intersect1d(elements, index_array)
    print(elements)
    if len(elements) == 0:
        continue
    else:
        try:
            disease_arr_col_index = np.array([np.where(index_array == el)[0] for el in elements])
            disease_arr_subset_rowsums = np.sum(disease_arr[:, disease_arr_col_index.flatten()], axis = 1) > 0
            is_disease = disease_arr_subset_rowsums.astype(np.int64)
            disease_categories_arr[:, idx] = is_disease

        except Exception as e:
            print(f"Error occurred at index {idx}: {e}")
            break
    
print(disease_categories_arr.shape)

# %%
# Count values per column of disease_categories_arr
df = pd.DataFrame(disease_categories_arr, columns=disease_categories)
#df = df.astype("int64")
df.apply(pd.Series.value_counts)
