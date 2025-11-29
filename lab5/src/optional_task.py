from pathlib import Path

import pandas as pd

from lab5.src.output.console import print_formatted_table
from lab5.src.output.excel import save_to_excel

SRC = Path(__file__).parent.parent

df = pd.read_excel(SRC / "data/mandatory_task.xlsx", header=None)
df = df.drop(columns=[7])

values_block = df.iloc[2:5, 2:5]      # С3:E5
table_block = df.iloc[5:17, 2:26]     # C6:AA17

result = pd.concat([values_block, table_block], axis=0, ignore_index=True)

print_formatted_table(result)
save_to_excel(result, SRC / "data/optional_task_output.xlsx")
