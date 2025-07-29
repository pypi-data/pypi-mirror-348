from datetime import datetime
from typing import Any

import numpy as np

from databricks.ml_features_common.entities.data_type import DataType


def deserialize_default_value_to_data_type(
    value_string: str, data_type: DataType
) -> Any:
    """
    Deserialize a default value string representation to the specified data type.
    :param value_string: The string representation of the default value.
    :param data_type: The data type to which the value should be deserialized.
    :return: The deserialized value in the specified data type.
    """
    if not value_string or not data_type:
        return np.nan

    if data_type in (
        DataType.INTEGER,
        DataType.LONG,
        DataType.SHORT,
        DataType.TIMESTAMP,
    ):
        return int(value_string)
    elif data_type in (DataType.FLOAT, DataType.DOUBLE, DataType.DECIMAL):
        return float(value_string)
    elif data_type == DataType.BOOLEAN:
        return value_string.lower() == "true"
    elif data_type == DataType.STRING:
        return value_string
    elif data_type == DataType.DATE:
        return datetime.strptime(value_string, "%Y-%m-%d").date()
    else:
        raise ValueError(f"Unsupported data type: {data_type} for default value")
