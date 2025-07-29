"""This module defines the functions to help ang check the providing of data for the mater data framework"""

import logging
import os
from typing import Dict, Literal

import pandas as pd


def metadata_definition(link: str, source: str, project: str) -> Dict[str, str]:
    """Returns a dictionary with all the keys necessary for the mater database metadata table schema.

    :param link: Link to find the raw dataset
    :type link: str
    :param source: Source name
    :type source: str
    :param project: Name of the project you are working on
    :type project: str
    :return: One metadata table entry
    :rtype: Dict[str, str]
    """
    return {"link": link, "source": source, "project": project}


def provider_definition(
    first_name: str, last_name: str, email_address: str
) -> Dict[str, str]:
    """Returns a dictionary with all the keys necessary for the mater database provider table schema.

    :param first_name: Your first name
    :type first_name: str
    :param last_name: Your last name
    :type last_name: str
    :param email_address: Your email address
    :type email_address: str
    :return: One provider table entry
    :rtype: Dict[str, str]
    """
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email_address": email_address,
    }


def to_json(
    df: pd.DataFrame,
    folder: Literal["input_data", "dimension", "variable_dimension"],
    name: str,
    mode: Literal["w", "a"] = "w",
):
    """Writes data from a dataframe to a json file into a specific directory structure.

    This structure is the one used by the mater library to run a simulation from local json data.

    :param df: Dataframe to dump into json
    :type df: pd.DataFrame
    :param folder: The table name corresponding to the data to dump
    :type folder: Literal[&quot;input_data&quot;, &quot;dimension&quot;, &quot;variable_dimension&quot;]
    :param name: The name of the json file
    :type name: str
    :param mode: _description_, defaults to "w"
    :type mode: Literal[&quot;w&quot;, &quot;a&quot;], optional
    """
    # Define the directory path
    data_path = os.path.join("data")

    # Check if the directory exists, if not, create it
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        logging.info(f"Directory {data_path} created.")

    # Define the directory path
    dir_path = os.path.join("data", folder)

    # Check if the directory exists, if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logging.info(f"Directory {dir_path} created.")

    # Save the DataFrame to JSON
    #### ToDo: find a way to automatically set name to the python script name importing this function
    df.to_json(
        os.path.join(dir_path, name + ".json"),
        orient="records",
        indent=2,
        mode=mode,
    )


def replace_equivalence(df: pd.DataFrame) -> pd.DataFrame:
    """Replaces the dimension elements of a dataframe according to the data\dimension\dimension.json file.

    :param df: Initial dataframe
    :type df: pd.DataFrame
    :return: Uniformed dataframe
    :rtype: pd.DataFrame
    """
    dimension = pd.read_json(
        os.path.join("data", "dimension", "dimension.json"), orient="records"
    )
    try:
        # Ensure multiple keys in 'equivalence' dictionaries are handled correctly
        df_filtered = dimension.dropna(
            subset=["equivalence"]
        )  # Keep rows with non-null equivalence

        # Expand 'equivalence' dictionary into separate columns
        df_exploded = (
            df_filtered["equivalence"]
            .apply(pd.Series)
            .stack()
            .reset_index(level=1, drop=True)
        )

        # Map each source equivalence key to its corresponding vehicle name
        equivalence_dict = (
            df_exploded.to_frame()
            .join(df_filtered["value"])
            .set_index(0)["value"]
            .to_dict()
        )
        df.replace(equivalence_dict, inplace=True)
    except KeyError:
        pass
    return df
