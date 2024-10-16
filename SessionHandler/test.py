import pandas as pd
import polars as pl
import numpy as np
import hashlib
from SessionHandler import Session

# Define custom hash function for pandas DataFrame
def hash_pandas_dataframe(df):
    return hashlib.md5(pd.util.hash_pandas_object(df).values.tobytes()).hexdigest()

# Define custom hash function for polars DataFrame
def hash_polars_dataframe(df):
    return hashlib.md5(df.write_csv().encode()).hexdigest()

def run_tests():
    # Create a session with custom hash functions for Pandas and Polars
    session = Session(max_versions=3)
    session.set_hash_func(pd.DataFrame, hash_pandas_dataframe)
    session.set_hash_func(pl.DataFrame, hash_polars_dataframe)

    # Test 1: Setting and getting values (Pandas DataFrame)
    df1 = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    session.set('df', df1)
    assert session.get('df').equals(df1), "Test 1 Failed: Getting value after setting it failed."

    # Test 2: Setting and getting values (Polars DataFrame)
    pl_df1 = pl.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    session.set('pl_df', pl_df1)
    assert session.get('pl_df').equals(pl_df1), "Test 2 Failed: Getting value after setting Polars DataFrame failed."

    # Test 3: Undoing the last change for Pandas DataFrame
    df2 = pd.DataFrame({'col1': [5, 6], 'col2': [7, 8]})
    session.set('df', df2)
    assert session.get('df').equals(df2), "Test 3 Failed: Getting updated value for Pandas DataFrame failed."

    session.undo('df')
    assert session.get('df').equals(df1), "Test 3 Failed: Undoing the last change for Pandas DataFrame failed."

    # Test 4: Undoing the last change for Polars DataFrame
    pl_df2 = pl.DataFrame({'col1': [5, 6], 'col2': [7, 8]})
    session.set('pl_df', pl_df2)
    assert session.get('pl_df').equals(pl_df2), "Test 4 Failed: Getting updated value for Polars DataFrame failed."

    session.undo('pl_df')
    assert session.get('pl_df').equals(pl_df1), "Test 4 Failed: Undoing the last change for Polars DataFrame failed."

    # Test 5: Check that undo is not performed when value is the same
    session.set('df', df1)  # Reset to original
    session.set('df', df1)  # Setting the same value again
    assert len(session._key_history['df']) == 1, "Test 5 Failed: Undo history should not increase when setting the same value."

    # Test 6: Setting and getting values (Strings)
    session.set('string', "Hello, World!")
    assert session.get('string') == "Hello, World!", "Test 6 Failed: Getting string value failed."

    # Test 7: Setting and getting values (Integers)
    session.set('integer', 42)
    assert session.get('integer') == 42, "Test 7 Failed: Getting integer value failed."

    # Test 8: Setting and getting values (Lists)
    session.set('list', [1, 2, 3])
    assert session.get('list') == [1, 2, 3], "Test 8 Failed: Getting list value failed."

    # Test 9: Setting and getting values (Dictionaries)
    session.set('dict', {'key': 'value'})
    assert session.get('dict') == {'key': 'value'}, "Test 9 Failed: Getting dictionary value failed."

    # Test 10: Setting and getting values (Numpy Arrays)
    np_array = np.array([1, 2, 3])
    session.set('numpy_array', np_array)
    assert np.array_equal(session.get('numpy_array'), np_array), "Test 10 Failed: Getting numpy array value failed."

    # Test 11: Undoing a string value
    session.set('string', "Goodbye!")
    session.undo('string')
    assert session.get('string') == "Hello, World!", "Test 11 Failed: Undoing string value failed."

    # Test 12: Edge case - Setting None value
    session.set('none_value', None)
    assert session.get('none_value') is None, "Test 12 Failed: Getting None value failed."

    # Test 13: Remove hash function and check default behavior
    session.set_hash_func(pd.DataFrame, None)
    session.set('df', df1)  # Set again with default hash function
    assert session.get('df').equals(df1), "Test 13 Failed: Should be able to set value with default hash function."

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()