# Utilities for writing to and reading from CSV
import pandas as pd
import logging
from datetime import datetime, time
from typing import List, Dict, Union

logging.basicConfig(level=logging.INFO)


"""
    Save the RF signal data to a CSV file using Pandas DataFrame.

    :param data: A list of dictionaries containing RF signal data.
    Each dictionary should contain:
        - start_time
        - end_time
        - frequency (Hz)
        - min_amplitude (dBm)
        - max_amplitude (dBm)
        - avg_amplitude (dBm)

    :param output_file: Path to the output CSV file. (e.g. 'output.csv')
"""


def save_as_csv(
    data: List[Dict[str, Union[datetime, float]]], output_file: str
) -> None:
    try:
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Ensure correct column order
        columns_order = [
            "timestamp",
            "min_amplitude",
            "max_amplitude",
            "average_amplitude",
            "frequency",
        ]
        df = df[columns_order]

        # Save the DataFrame to a CSV file
        df.to_csv(data / output_file, index=False)
        logging.info(f"Data successfully saved to {output_file}")

    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")


"""
    Read the RF signal data from a CSV file and return it as a list of dictionaries.

    :param input_file: Path to the input CSV file. (e.g 'output.csv')
    :return: List of dictionaries with the RF signal data.
"""


def read_from_csv(
    input_file: str,
) -> List[Dict[str, Union[str, float, datetime, time]]]:
    try:
        df = pd.read_csv(input_file)
        return df.to_dict(orient="records")

    except Exception as e:
        logging.error(f"Error reading from CSV: {e}")
        return []
