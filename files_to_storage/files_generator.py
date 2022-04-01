#!/usr/local/bin/python3.10

import argparse
import time
from pathlib import Path
from random import randint

parser = argparse.ArgumentParser()
parser.add_argument("-l", dest="lines", default=100, type=int, help="Quantity of lines in the file (default = 100)")
parser.add_argument("-p", dest="period", required=False, type=int, help="Files creation period in seconds. "
                                                                        "If none is specified, the program runs once. ")
parser.add_argument("-fn", dest="files_number", default=3, required=False, type=int, help="Quantity of files created "
                                                                                          "per one iteration")
parser.add_argument("-wd", dest="work_dir", required=True, help="Directory to which the files will go")

options = parser.parse_args()


def generate_new_file():
    in_loop = True
    while in_loop:
        if not options.period:
            in_loop = False
        for i in range(options.files_number):
            print("Starting new file creation...")
            new_filename = f"{str(time.time_ns())}.txt"
            to_file = ""
            for _ in range(options.lines):
                to_line = f"{randint(100, 999)} {randint(10000, 99999)}\n"
                to_file += to_line
            with open(f"{options.work_dir}/{new_filename}", "w") as f:
                f.write(to_file)
            print(f"File '{new_filename}' has been created")

        if in_loop:
            print(f"Sleeping for {options.period}...")
            time.sleep(options.period)


if __name__ == '__main__':
    generate_new_file()
