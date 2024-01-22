import os
import shutil
import csv


def create_folders(*folder_names):
    for folder_name in folder_names:
        # creating folders for csv files
        os.makedirs(folder_name, exist_ok=True)


def remove_folders(*folder_names):
    for folder_name in folder_names:
        try:
            # removing folders after merging data
            shutil.rmtree(folder_name)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def get_folder_contents(folder_name):
    return [os.path.join(folder_name, file) for file in sorted(os.listdir(folder_name))]


def write_csv(data, csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
