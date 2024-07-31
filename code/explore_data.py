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
data_dir = os.path.join("data", "capture24")

# %% Load the dataset

# List files in data_dir
print(os.listdir(data_dir))

df = pd.read_csv(os.path.join(data_dir, "P001.csv.gz"))

# Display the first few rows of the dataframe
df.tail(10)

# %%
# Read all compressed csv files in data_dir starting with P and with extension .csv.gz and concatenate them, write in coding best practice and format  
df = pd.concat([pd.read_csv(os.path.join(data_dir, f)) for f in os.listdir(data_dir) if f.startswith("P") and f.endswith(".csv.gz")], ignore_index=True)
