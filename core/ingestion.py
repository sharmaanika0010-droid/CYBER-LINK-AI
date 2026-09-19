import json
from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".json",
    ".txt",
    ".log",
    ".eml"
}


def read_csv_file(file_path):
    return pd.read_csv(file_path)


def read_excel_file(file_path):
    return pd.read_excel(file_path)


def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        return file.read()


def read_eml_file(file_path):
    """
    Basic EML header extraction.
    Full email analysis will be added later.
    """
    headers = {}

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            line = line.rstrip()

            if not line:
                break

            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()

    return headers


def ingest_file(file_path):
    """
    Automatically read an evidence file according to its extension.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported evidence format: {extension}"
        )

    if extension == ".csv":
        data = read_csv_file(path)

    elif extension == ".xlsx":
        data = read_excel_file(path)

    elif extension == ".json":
        data = read_json_file(path)

    elif extension in {".txt", ".log"}:
        data = read_text_file(path)

    elif extension == ".eml":
        data = read_eml_file(path)

    else:
        raise ValueError("Unsupported file format")

    return {
        "file": path.name,
        "format": extension.replace(".", "").upper(),
        "data": data
    }


def ingest_evidence_folder(folder_path):
    """
    Ingest every supported evidence file in the folder.
    """

    folder = Path(folder_path)
    results = []

    for file_path in sorted(folder.iterdir()):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            evidence = ingest_file(file_path)

            results.append({
                "status": "SUCCESS",
                **evidence
            })

        except Exception as error:

            results.append({
                "status": "ERROR",
                "file": file_path.name,
                "format": file_path.suffix.lower(),
                "error": str(error)
            })

    return results