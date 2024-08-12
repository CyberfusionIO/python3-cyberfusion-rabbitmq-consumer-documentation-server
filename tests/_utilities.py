import os


def get_first_file_in_directory(directory: str) -> str:
    for item in os.listdir(directory):
        if not os.path.isfile(os.path.join(directory, item)):
            continue

        return item

    raise Exception("No files in directory")
