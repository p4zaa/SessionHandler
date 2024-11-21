import hashlib
import pickle

class Session:
    def __init__(self, max_versions=5, hash_funcs=None):
        """
        Initialize a Session with undo capabilities and custom hash functions.

        Args:
        max_versions (int): Maximum number of previous versions to store for undo functionality.
        hash_funcs (dict, optional): A dictionary mapping data types to custom hash functions.
        """
        self._data = {}
        self._hashes = {}  # Store the hash of each key's value
        self._key_history = {}  # to store history for each key
        self.max_versions = max_versions
        self.hash_funcs = hash_funcs if hash_funcs else {}

    def set(self, key, value):
        """
        Set a variable in the session and save the current state for undo, only if the value differs.

        Args:
        key (str): The variable name.
        value: The value to store.
        """
        # Compute the hash of the new value
        new_hash = self._compute_hash(value)

        # Only save the state if the new value has a different hash
        if self._hashes.get(key) != new_hash:
            self._save_state(key)
            self._data[key] = value
            self._hashes[key] = new_hash

    def get(self, key, default):
        """
        Get a variable's value from the session.

        Args:
        key (str): The variable name.

        Returns:
        The value associated with the key, or None if the key doesn't exist.
        """
        return self._data.get(key, default)

    def undo(self, key):
        """
        Undo the last operation for a specific key.

        Args:
        key (str): The specific variable name to undo.
        """
        if key in self._key_history and self._key_history[key]:
            # Revert to the last saved state for the specific key
            self._data[key] = self._key_history[key].pop()
            # Recompute and store the hash for the restored value
            self._hashes[key] = self._compute_hash(self._data[key])
        else:
            print(f"No more undos available for key: {key}")

    def _save_state(self, key):
        """
        Save the current state to the history for the specific key.

        Args:
        key (str): The key whose value is being updated.
        """
        # Save history for the specific key
        if key not in self._key_history:
            self._key_history[key] = []

        # Save the current value of the key before updating it
        self._key_history[key].append(self._data.get(key))
        # Limit the key-specific history size to max_versions
        if len(self._key_history[key]) > self.max_versions:
            self._key_history[key].pop(0)

    def _compute_hash(self, value):
        """
        Compute a hash for the given value.

        If a custom hash function is provided for the data type of the value, it is used.
        Otherwise, it defaults to using pickle and MD5 hashing.
        
        Args:
        value: The value to hash.

        Returns:
        str: The hash of the value.
        """
        value_type = type(value)
        
        # Check if a custom hash function is defined for the value's type
        if value_type in self.hash_funcs:
            hash_func = self.hash_funcs.get(value_type)
            if hash_func:
                try:
                    return hash_func(value)
                except Exception as e:
                    print(f"Error using custom hash function for {value_type}: {e}")
        
        # Default to pickle and MD5 hash if no custom hash function is provided
        try:
            value_bytes = pickle.dumps(value)
            return hashlib.md5(value_bytes).hexdigest()
        except Exception as e:
            # If hashing fails, return None to treat as different
            print(f"Could not compute hash for value: {e}")
            return None

    def set_hash_func(self, data_type, hash_func):
        """
        Add, modify, or remove the hash function for a specific data type.

        Args:
        data_type (type): The data type to associate with the custom hash function.
        hash_func (callable or None): The custom hash function that takes a value of the data type and returns a hash string.
                                       If None, it will revert to the default hash function.
        """
        if hash_func is None:
            if data_type in self.hash_funcs:
                del self.hash_funcs[data_type]
                print(f"Custom hash function for {data_type} removed, using default.")
        else:
            self.hash_funcs[data_type] = hash_func
            print(f"Hash function for {data_type} has been added/modified.")

    def show(self):
        """
        Display the current state of stored data.
        """
        return self._data