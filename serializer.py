import pickle
import doctest
from typing import Any, Union, Callable
import numpy as np
# import torch
import pickle
import time
from typing import Callable, Any, Tuple, List
from datetime import datetime
import os
import functools
import inspect

# from ptycho import params


class Serializer:
    def serialize(self, input_data: Any) -> bytes:
        """
        Serializes Python objects to a binary format using pickle.
        
        >>> serializer = Serializer()
        >>> test_data = {'key': 'value', 'number': 42}
        >>> serialized_data = serializer.serialize(test_data)
        >>> isinstance(serialized_data, bytes)
        True

        Args:
            input_data: Any serializable Python object.

        Returns:
            bytes: Serialized binary data of the input object.

        Raises:
            ValueError: If the input data is not serializable.
        """
        try:
            serialized_data = pickle.dumps(input_data)
            return serialized_data
        except pickle.PicklingError:
            raise ValueError("Input data is not serializable")

    def deserialize(self, serialized_data: bytes) -> Any:
        """
        Deserializes Python objects from a binary format using pickle.
        
        >>> serializer = Serializer()
        >>> test_data = {'key': 'value', 'number': 42}
        >>> serialized_data = serializer.serialize(test_data)
        >>> deserialized_data = serializer.deserialize(serialized_data)
        >>> deserialized_data == test_data
        True

        Args:
            serialized_data: Binary data to be deserialized.

        Returns:
            any: The original Python object.

        Raises:
            ValueError: If the binary data could not be deserialized.
        """
        try:
            data = pickle.loads(serialized_data)
            return data
        except pickle.UnpicklingError:
            raise ValueError("Serialized data could not be deserialized")


doctest.testmod(verbose=False)


