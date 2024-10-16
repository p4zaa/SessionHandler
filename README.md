# Session Management Library

The **Session Management Library** provides a flexible session handling class that allows you to store multiple variables and track their changes. It includes an undo feature that enables reverting to previous values while optimizing data storage by avoiding duplicates.

## Features

- Store multiple variables of various data types (e.g., Python objects, Pandas DataFrames, Polars DataFrames).
- Undo changes for specific keys, allowing you to revert to previous states.
- Check for identical values using custom hash functions, preventing unnecessary storage of unchanged data.
- Set or modify hash functions for specific data types to customize the comparison behavior.

## Usage

### Importing the Library

```python
from SessionHandler import Session
```

### Creating a Session

You can create a new session by initializing the `Session` class:

```python
session = Session(max_versions=3)
```

### Setting Hash Functions

You can set custom hash functions for specific data types:

```python
import pandas as pd
import polars as pl

# Define custom hash functions
def hash_pandas_dataframe(df):
    # Implement your hashing logic here
    pass

def hash_polars_dataframe(df):
    # Implement your hashing logic here
    pass

# Set the hash functions
session.set_hash_func(pd.DataFrame, hash_pandas_dataframe)
session.set_hash_func(pl.DataFrame, hash_polars_dataframe)
```

### Storing Data

Store data in the session using the `set` method:

```python
session.set('key', value)
```

### Retrieving Data

Retrieve stored data using the `get` method:

```python
value = session.get('key')
```

### Undoing Changes

To undo the last change for a specific key, use the `undo` method:

```python
session.undo('key')
```

### Example

```python
import pandas as pd
from SessionHandler import Session

# Create a session
session = Session(max_versions=3)

# Set a DataFrame
df1 = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
session.set('df', df1)

# Update the DataFrame
df2 = pd.DataFrame({'col1': [5, 6], 'col2': [7, 8]})
session.set('df', df2)

# Undo the last change
session.undo('df')

# Get the previous value
previous_df = session.get('df')  # This will be df1
```

### Custom Hash Function Example

You can customize the hash function for different data types:

```python
# Custom hash function for Pandas DataFrame
def hash_pandas_dataframe(df):
    return pd.util.hash_pandas_object(df).values.tobytes()

# Set the hash function
session.set_hash_func(pd.DataFrame, hash_pandas_dataframe)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to contribute to this project.
