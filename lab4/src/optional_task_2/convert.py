import pickle

import hcl2
import toml

# HCL -> dict
with open("data/schedule.hcl", "r") as f:
    hcl_data = hcl2.load(f)

# dict -> binary
with open("data/schedule.bin", "wb") as f:
    pickle.dump(hcl_data, f)

# binary -> dict
with open("data/schedule.bin", "rb") as f:
    loaded_data = pickle.load(f)

# dict -> TOML
with open("data/schedule.toml", "w") as f:
    toml.dump(loaded_data, f)
