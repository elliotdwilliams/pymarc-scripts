"""Extracts record IDs and specific fields from a file of MARC records.

Iterates through a set of MARC records and outputs a tab-delimited file including record 
IDs (from field 001) and values of given fields. Accepts a command line argument of 
filename or filename pattern to use as input. If a pattern (e.g. 'subject*.mrc'), enclose 
it in single quotes when you execute the script.
"""

import sys
import os
import glob
import pymarc

INPUT_FILES = sys.argv[1]

# These are the fields you want to look for
FIELDS = ['773']


def get_fields(record, FIELDS, output_data):
    """Checks for MARC fields from FIELDS constant. If found, adds the MMS ID and 
    field to output list."""

    # Get MMS ID from 001
    for f in record.get_fields('001'):
        record_id = str(f.value())

    # Test to see if target fields are in record
    target_fields = record.get_fields(*FIELDS)

    for field in target_fields:
        print(record_id)
        print(field)
        output_data.append(record_id + '\t' + str(field))
        

def output_values(file, output_data):
    """Creates output file and prints identifiers + fields"""

    # Create output file name
    basename = os.path.splitext(file)[0]
    output_file = basename + '_export.txt'

    # Open output file and print results
    with open(output_file, 'w', encoding='utf-8') as f:
        for i in output_data:
            f.write(f"{i}\n")
    f.close()


def main():
    # Get all files that match input file pattern
    files = glob.glob(INPUT_FILES)
            
    for file in files:
        print(file)

        # Restart record count at 1 (useful for error checking)
        record_no = 1

        # Set output data list as empty
        output_data = []

        # Open file and start MARCReader
        with open(file, 'rb') as fh:
            reader = pymarc.MARCReader(fh, to_unicode=True, force_utf8=True)

            # Iterate through records
            for record in reader:

                try:
                    print(str(record_no))

                    get_fields(record, FIELDS, output_data)

                    record_no += 1

                except Exception as error:
                    print(str(record_no))
                    print(error)
                    record_no += 1

        fh.close()

        # If record_identifiers is not empty, create output file
        if output_data:
            output_values(file, output_data)


if __name__ == '__main__':
    main()
