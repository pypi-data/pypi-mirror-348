# Simple color printer for pandas DataFrames

## pip install cythondfprint

### Tested against Windows 10 / Python 3.11 / Anaconda 

### Important!

The module will be compiled when you import it for the first time. Cython and a C/C++ compiler must be installed!

```python
import pandas as pd
from cythondfprint import add_printer

add_printer(1)  # overwrites __str__ and __repr__
df = pd.read_csv(
    "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
)
print(df)
df.ds_color_print_all()
df.ds_color_print_all(
    column_rep=70,  # repeat columns after 70 rows
    max_colwidth=300,  # max column width (0 = no limit)
    ljust_space=2,
    sep=" | ",
    vtm_escape=True,  # to look pretty here: https://github.com/directvt/vtm
)
pd.color_printer_reset()  # to restore default
print(df)
pd.color_printer_activate()  # to print in color
print(df)
print(df.Name) # Series
df.Name.ds_color_print_all()  # Series
```