import os


def list_files(path):
    files = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        for item in os.listdir(path):
            item = os.path.join(path, item)
            files.extend(list_files(item))

    return files
