import doctest
import pickle
from typing import Any, List

class Serializer:
    def serialize(self, input_data: Any) -> bytes:
        """
        Serializes Python objects to a binary format using pickle.

        Preconditions:
        - `input_data` must be a picklable Python object.

        Postconditions:
        - Returns the serialized binary data of the input object.
        - Raises ValueError if the input data is not picklable.

        >>> s = Serializer()
        >>> data = {'key': 'value'}
        >>> serialized_data = s.serialize(data)
        >>> type(serialized_data)
        <class 'bytes'>
        >>> deserialized_data = s.deserialize(serialized_data)
        >>> deserialized_data == data
        True
        >>> s.serialize(lambda x: x)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Input data is not picklable
        >>> s.deserialize(b'not a pickle')  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Could not deserialize the binary data
        """
        try:
            return pickle.dumps(input_data)
        except (pickle.PicklingError, AttributeError):
            raise ValueError("Input data is not picklable")

    def deserialize(self, serialized_data: bytes) -> Any:
        """
        Deserializes Python objects from a binary format using pickle.

        Preconditions:
        - `serialized_data` must be a valid pickle-serialized binary string.

        Postconditions:
        - Returns the deserialized Python object.
        - Raises ValueError if the binary data could not be deserialized.

        >>> s = Serializer()
        >>> data = {'key': 'value'}
        >>> serialized_data = s.serialize(data)
        >>> deserialized_data = s.deserialize(serialized_data)
        >>> deserialized_data == data
        True
        >>> s.deserialize(b'not a pickle')  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Could not deserialize the binary data
        """
        try:
            return pickle.loads(serialized_data)
        except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError):
            raise ValueError("Could not deserialize the binary data")
doctest.testmod(verbose=True)

#
#import pickle
#import doctest
#from typing import Any, Union, Callable
#import numpy as np
## import torch
#import pickle
#import time
#from typing import Callable, Any, Tuple, List
#from datetime import datetime
#import os
#import functools
#import inspect
#
## from ptycho import params
#
#
#class Serializer:
#    def serialize(self, input_data: Any) -> bytes:
#        """
#        Serializes Python objects to a binary format using pickle.
#        
#        >>> serializer = Serializer()
#        >>> test_data = {'key': 'value', 'number': 42}
#        >>> serialized_data = serializer.serialize(test_data)
#        >>> isinstance(serialized_data, bytes)
#        True
#
#        Args:
#            input_data: Any serializable Python object.
#
#        Returns:
#            bytes: Serialized binary data of the input object.
#
#        Raises:
#            ValueError: If the input data is not serializable.
#        """
#        try:
#            serialized_data = pickle.dumps(input_data)
#            return serialized_data
#        except pickle.PicklingError:
#            raise ValueError("Input data is not serializable")
#
#    def deserialize(self, serialized_data: bytes) -> Any:
#        """
#        Deserializes Python objects from a binary format using pickle.
#        
#        >>> serializer = Serializer()
#        >>> test_data = {'key': 'value', 'number': 42}
#        >>> serialized_data = serializer.serialize(test_data)
#        >>> deserialized_data = serializer.deserialize(serialized_data)
#        >>> deserialized_data == test_data
#        True
#
#        Args:
#            serialized_data: Binary data to be deserialized.
#
#        Returns:
#            any: The original Python object.
#
#        Raises:
#            ValueError: If the binary data could not be deserialized.
#        """
#        try:
#            data = pickle.loads(serialized_data)
#            return data
#        except pickle.UnpicklingError:
#            raise ValueError("Serialized data could not be deserialized")
#
#
#doctest.testmod(verbose=False)
#
#
