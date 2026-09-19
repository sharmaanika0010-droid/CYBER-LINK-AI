import hashlib
from pathlib import Path


def calculate_sha256(file_path):
    """
    Calculate the SHA-256 hash of a single evidence file.

    SHA-256 creates a unique digital fingerprint of the file.
    If the file content changes, its hash will also change.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        for block in iter(
            lambda: file.read(8192),
            b""
        ):

            sha256.update(block)

    return sha256.hexdigest()


def hash_evidence_folder(folder_path):
    """
    Calculate SHA-256 hashes for all files
    present inside the evidence folder.

    Returns:
        list of dictionaries containing:
        - file name
        - SHA-256 hash
        - file size in bytes
    """

    folder = Path(folder_path)

    results = []

    # Check whether evidence folder exists
    if not folder.exists():

        return results

    # Process files in alphabetical order
    for file_path in sorted(folder.iterdir()):

        if not file_path.is_file():

            continue

        try:

            file_hash = calculate_sha256(
                file_path
            )

            file_size = file_path.stat().st_size

            results.append({

                "file":
                    file_path.name,

                "sha256":
                    file_hash,

                "size_bytes":
                    file_size
            })

        except Exception as error:

            results.append({

                "file":
                    file_path.name,

                "sha256":
                    "ERROR",

                "size_bytes":
                    0,

                "error":
                    str(error)
            })

    return results


def verify_file_hash(file_path, expected_hash):
    """
    Verify whether the current SHA-256 hash
    of a file matches an expected hash.

    Returns:
        True  -> file is unchanged
        False -> file content differs
    """

    current_hash = calculate_sha256(
        file_path
    )

    return (
        current_hash.lower()
        ==
        expected_hash.lower()
    )


def create_integrity_manifest(folder_path):
    """
    Create a simple evidence integrity manifest.

    This can be used by the dashboard/report
    to show which evidence files were processed
    and their SHA-256 fingerprints.
    """

    evidence_hashes = hash_evidence_folder(
        folder_path
    )

    manifest = {

        "evidence_folder":
            str(folder_path),

        "total_files":
            len(evidence_hashes),

        "files":
            evidence_hashes
    }

    return manifest