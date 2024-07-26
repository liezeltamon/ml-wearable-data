# %% Setup
import sys
from pathlib import Path
import pandas as pd
import os
# Add utils/python to the Python path
sys.path.append(str(Path("~/git/ml-wearable-data/utils/python").expanduser()))
# Import the env module
from env import find_project_dir

# %% Parameters
proj_dir = find_project_dir(Path(__file__), ".git")
os.chdir(proj_dir)
data_dir = os.path.join("data", "capture24")

# %% Read accelerometer data
df = pd.read_csv(os.path.join(data_dir, "P001.csv.gz"))
df.head()
df.shape

# %%
