"""Converts an excel file to csv."""

import argparse
import pandas as pd

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=('''\
        Converts an excel file to csv.
    '''))
parser.add_argument('in_file')
parser.add_argument('out_dir')

args = parser.parse_args()

INPUT_FILE = args.in_file
OUTPUT_DIRECTORY = args.out_dir
FILE_NAME = INPUT_FILE.split('.xls')[0].split('/')[-1]
OUTPUT_FILE = '{}{}.csv'.format(OUTPUT_DIRECTORY, FILE_NAME)
print("\nInput: {}".format(INPUT_FILE))
print("\nOutput: {}\n".format(OUTPUT_FILE))

df = pd.read_excel(INPUT_FILE)
df.to_csv(OUTPUT_FILE, index=False)
