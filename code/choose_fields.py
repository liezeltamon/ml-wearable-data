# Select field ids from data/ukbb_fields.csv to download from UKBB

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

# %% Parameters
proj_dir = find_project_dir(Path(__file__), ".git")
os.chdir(proj_dir)
data_dir = "data"

# %% Load the dataset

print(os.listdir(data_dir))
df = pd.read_csv(os.path.join(data_dir, "ukbb_fields.csv"), \
                 dtype={"field_id": "string", "field_description": "string", "priority": "Int64", "comment": "string"})
df.head()

# %%
selected_fields = df[df["priority"] == 1]["field_id"].tolist()
selected_fields
