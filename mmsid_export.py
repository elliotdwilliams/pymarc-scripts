"""Extracts MMS IDs from field 001 for a set of MARC records

Iterates through a set of MARC records and outputs all values found in 001 fields. Useful for
generating a list of MMS IDs from a MARC export which can then be input into Alma Analytics.
Accepts a command line argument of filename or filename pattern to use as input. If a pattern
(e.g. 'subject*.mrc'), enclose it in single quotes when you execute the script.
"""

import sys
import os
import glob
import pymarc

INPUT_FILES = sys.argv[1]

# Get all files that match input file pattern
files = glob.glob(INPUT_FILES)


def get_ids(mms_ids, record_no, record):
    """Gets MMS id value from 001"""

    # # Print title to command line (for error checking)
    # try:
    #     print(str(record_no) + ' ' + record.title)
    # except UnicodeEncodeError:
    #     print(str(record_no) + '[Title error]')

    # Get MMS ID from 001
    for f in record.get_fields('001'):
        record_id = str(f.value())
        # print(record_id)
        mms_ids.append(record_id)


def output_values(file, mms_ids):
    """Creates output file and prints MMS ids"""

    # Create output file name
    basename = os.path.splitext(file)[0]
    output_file = basename + "_MMSids.txt"

    # Open output file and print results
    with open(output_file, 'w', encoding='utf-8') as f:
        for i in mms_ids:
            f.write(f"{i}\n")
    f.close()


def main():

    for file in files:
        print(file)

        # Restart record count at 1 (useful for error checking)
        record_no = 1

        # Set MMS ID values list as empty
        mms_ids = []

        # Open file and start MARCReader
        with open(file, 'rb') as fh:
            reader = pymarc.MARCReader(fh, to_unicode=True, force_utf8=True)

            for record in reader:

                try:
                    get_ids(mms_ids, record_no, record)
                    record_no += 1

                except Exception as error:
                    print(str(record_no))
                    print(error)
                    record_no += 1

        fh.close()

        # If mms_ids list is not empty, create output file
        if mms_ids:
            output_values(file, mms_ids)


if __name__ == '__main__':
    main()
