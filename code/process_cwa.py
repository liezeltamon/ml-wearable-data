# Test processing cwa files

# %% Setup
import sys
from pathlib import Path
import os
# Add utils/python to the Python path
#sys.path.append(str(Path("~/git/ml-wearable-data/utils/python").expanduser()))
sys.path.append(os.path.join(str(Path(__file__).parent.parent), "utils", "python"))
# Import the env module
from env import find_project_dir

import pandas as pd
from accelerometer import accProcess
import actipy

# %% Parameters
proj_dir = find_project_dir(Path(__file__), ".git")
os.chdir(proj_dir)
data_dir = "data"

# %% Load the dataset

import subprocess

# Run the command-line tool
result = subprocess.run(['accProcess', 'data/sample_cwa/ax3_testfile.cwa.gz'], capture_output=True, text=True)


data, info = accProcess(os.path.join(data_dir, "sample_cwa", "ax3_testfile.cwa.gz"))

data, info = actipy.read_device(os.path.join(data_dir, "sample_cwa", "ax3_testfile.cwa.gz"),
                                lowpass_hz=20,
                                calibrate_gravity=True,
                                detect_nonwear=True,
                                resample_hz=50)

# %%
data.head()
info

# %% Extract features from wearable data

