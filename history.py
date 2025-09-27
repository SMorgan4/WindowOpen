import csv
from datetime import datetime
import os


def write_row(sources, file_name="history.csv"):
    row_dict = make_dict(sources)

    is_empty = check_if_empty(file_name)

    with open(file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=row_dict.keys())

        if is_empty:
            writer.writeheader()

        writer.writerow(row_dict)

        file.close()


def check_if_empty(file_name):
    with open(file_name, mode='r', newline='') as file:
        reader = csv.reader(file)
        try:
            next(reader)
            file.close()
            return False
        except StopIteration:
            file.close()
            return True


def make_dict(sources):
    row_dict = {"Time": datetime.now()}
    for source in sources:
        row_dict.update(source.get_state_dict())
    return row_dict
