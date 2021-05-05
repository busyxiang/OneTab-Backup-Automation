import os


def create_directory_if_not_exists(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)


def remove_directory_if_exists(dirPath):
    if os.path.exists(dirPath):
        shutil.rmtree(dirPath)
