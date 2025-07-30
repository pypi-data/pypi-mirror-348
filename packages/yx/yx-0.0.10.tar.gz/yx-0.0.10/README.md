# yx
Dataframe manipulation tools

To install:	```pip install yx```

## Overview
The `yx` package provides a comprehensive suite of tools designed for efficient and flexible manipulation of pandas DataFrames. It includes functions for handling NaN values, type casting, digitizing data, and more complex operations like conditional replacements and rolling out columns. This package is particularly useful for data preprocessing, cleaning, and transformation tasks in data analysis and machine learning workflows.

## Features
- **NaN Handling**: Functions to replace NaN values and check for NaNs in various ways.
- **Type Handling**: Utilities to determine and cast data types of DataFrame columns, especially for numeric types.
- **Data Transformation**: Functions to digitize data, perform conditional replacements, and manipulate DataFrame columns and rows.
- **Utility Functions**: A collection of helper functions to perform operations like flattening hierarchical indices, removing columns, and filtering data.

## Usage Examples

### Checking and Replacing Empty Cells
You can easily check for and replace "empty" cells (cells that are NaN, None, or falsy):
```python
import pandas as pd
from yx import is_empty, replace_empty_cells_with

df = pd.DataFrame({'data': [None, np.nan, 0, '', [], False, True]})
print(df.applymap(is_empty))
# Replace empty cells with a specified value (e.g., 'Empty')
df = replace_empty_cells_with(df, 'Empty')
print(df)
```

### Type Handling
Determine the most common numerical type in a column and cast all possible columns to numeric types:
```python
from yx import common_numerical_type, cast_all_cols_to_numeric_if_possible

df = pd.DataFrame({'numbers': [1, 2.5, np.nan, 4]})
print(common_numerical_type(df['numbers']))  # Outputs: float
df = cast_all_cols_to_numeric_if_possible(df)
print(df.dtypes)
```

### Digitizing Data
Divide data into bins and then group by these digitized values:
```python
from yx import digitize_and_group

df = pd.DataFrame({'values': np.random.rand(10)})
digit_groups = digitize_and_group(df, digit_cols=['values'], digit_agg_fun='mean')
print(digit_groups)
```

### Rolling Out Columns
Expand list-like entries in DataFrame columns into separate rows:
```python
from yx import rollout_cols

df = pd.DataFrame({
    'A': [1, 2],
    'B': [[10, 20], [30]]
})
df_rolled = rollout_cols(df, cols_to_rollout='B')
print(df_rolled)
```

## Function Documentation
Below are some of the key functions provided by the `yx` package:

### `is_empty(cell)`
Checks if a DataFrame cell is considered "empty". A cell is deemed empty if it is a NaN-like value, an empty iterable, or a falsy value excluding the boolean value False.

### `conditional_replace(df, replacement, condition)`
Replaces values in a DataFrame based on a specified condition function.

### `common_numerical_type(iterable)`
Determines the most common numerical type (int or float) in an iterable, handling NaNs and None values gracefully.

### `digitize_and_group(df, digit_cols=None, digit_agg_fun='mean', agg_fun='mean', **kwargs)`
Digitizes the columns of a DataFrame into specified bins and groups them, optionally aggregating using a specified function.

### `rollout_cols(df, cols_to_rollout=None)`
Expands list-like entries in specified DataFrame columns into separate rows, aligning other column values accordingly.

These utilities make it easier to preprocess and manipulate data efficiently in Python, leveraging the power of pandas and numpy.