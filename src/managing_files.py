from csv import DictReader
import json
import os
import pickle
import pandas as pd
import requests
from typing import Any, Dict, List


def csv_column_as_list(file_path: str, column: str) -> List[Any]:
    """
    Get a list from a csv file column.
    :param file_path:
    :param column: name of the column to retrieve
    :return: list of items on that column
    """
    items = []
    with open(file_path) as csv_file:
        reader = DictReader(csv_file)
        for line in reader:
            items.append(line[column])
    return items


def list_dict_from_csv(file_path: str, encoding: str = "utf8"):
    """
    Get a objects from a csv file.
    :param file_path:
    :param encoding:
    :return: rows as objects
    """
    with open(file_path, encoding) as csv_file:
        reader = DictReader(csv_file)
        for line in reader:
            if line:
                yield line


def csv_as_dict(
    file_path: str, key_column: str, value_column: str = ""
) -> Dict[str, Any]:
    """
    Get a dict from a csv file.
    :param file_path:
    :param key_column: name of the column to be the key
    :return: dict with selected column as key
    """
    items = {}
    with open(file_path, encoding="utf8") as csv_file:
        reader = DictReader(csv_file)
        if value_column:
            for line in reader:
                items[line[key_column]] = line[value_column]
        else:
            for line in reader:
                items[line[key_column]] = line
    return items


def unzip_files(zipped_file_path: str, destination_folder: str):
    """
    Unzip a zipped file.
    :param zipped_file_path: path to the zipped file
    :param destination_folder: path for the destination
    """
    import zipfile

    with zipfile.ZipFile(zipped_file_path, "r") as zipped_file:
        zipped_file.extractall(destination_folder)


def save_file(destination_file_path: str, content: Any, join_list: bool = False):
    """
    Save content to a file.
    :param destination_file_path: path to save the file
    :param content: content to be saved
    :param join_list: join list with line breaks
    """
    if join_list and isinstance(content, list):
        content = "\n".join(content)
    content = str(content)
    with open(destination_file_path, "w") as destination_file:
        destination_file.write(content)


def create_csv(
    destination_file_path: str, content: List[Dict[str, Any]], columns: list = []
):
    """
    Save data as a csv file.
    :param destination_file_path: path to save the file
    :param content: content to be saved
    :param columns: list of column names
    """
    if columns:
        df = pd.DataFrame(content, columns=columns)
    else:
        df = pd.DataFrame(content)
    if not destination_file_path.endswith(".csv"):
        destination_file_path = destination_file_path + ".csv"
    df.to_csv(destination_file_path)


def read_file(file_path: str) -> str:
    """
    Open file and return contend.
    :param file_path:
    :return: file contend
    """
    with open(file_path, "r") as reader:
        return reader.read()


def read_json_file(file_path):
    """
    Open json file and return contend.
    :param file_path:
    :return: file contend
    """
    with open(file_path) as json_file:
        contend = json.load(json_file)
        return contend


def load_pickle_file(file_path):
    """
    Open pickle file and return contend.
    :param file_path:
    :return: file contend
    """
    with open(file_path, "rb") as pickle_file:
        return pickle.load(pickle_file)


def download_file(url: str, destination_folder: str = "", return_bytes: bool = True):
    """
    Download file and save it or return bytes.
    :param url:
    :param destination_folder:
    :param return_bytes: return file bytes
    :return: file name or bytes
    """
    try:
        response = requests.get(url, allow_redirects=True)
        if return_bytes:
            return response.content
        file_name = url.split("/")[-1]
        file_path = os.path.join(destination_folder, file_name)
        open(file_path, "wb").write(response.content)
        return file_name
    except Exception as e:
        print(e)


# if __name__ == "__main__":
