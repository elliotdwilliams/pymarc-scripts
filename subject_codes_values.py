"""Extracts subject field values  from a set of MARC records, based on a given subject source code.

Iterates through a set of MARC records and outputs subject terms with a given source code in $2.
Accepts a command line argument of filename or filename pattern to use as input. If a pattern 
(e.g. 'subject*.mrc'), enclose it in single quotes when you execute the script. Output file
includes MMS ID and all contents of subject field.
"""

import sys
import os
import glob
import pymarc

INPUT_FILES = sys.argv[1]

# Get all files that match input file pattern
files = glob.glob(INPUT_FILES)


def get_values(subject_values, subject_code, record_no, record):
    """Gets subject values if they match subject code"""

    # Print title to command line (for error checking)
    try:
        print(str(record_no) + ' ' + record.title)
    except UnicodeEncodeError:
        print(str(record_no) + '[Title error]')

    # Get MMS ID from 001
    for f in record.get_fields('001'):
        record_id = str(f.value())

    # Get all subject fields and iterate through them
    # Currently excludes 655
    for subject in record.get_fields(
        '600', '610', '611', '630', '647', '648', '650', '651', '656', '657', '658', '662'
    ):

        # Get subfield 2 if it exists
        code = subject.get_subfields('2')
        if code:
            code = str(code[0])
            # print(code)

            # If $2 matches subject_code print the record ID and entire subject field
            if code == subject_code:
                subject_value = (record_id + '\t' + subject.value())
                print(subject_value)
                subject_values.append(subject_value)


def output_values(file, subject_code, subject_values):
    """Creates output file and prints subject values"""

    # Create output file name
    basename = os.path.splitext(file)[0]
    output_file = basename + "_" + subject_code + ".txt"

    # Open output file and print results
    with open(output_file, 'w', encoding='utf-8') as f:
        for i in subject_values:
            f.write(f"{i}\n")
    f.close()

def main():

    subject_code = input('Subject code: ')
    # print(subject_code)

    print(files)

    for file in files:
        print(file)

        # Restart record count at 1 (useful for error checking)
        record_no = 1

        # Set subject values list as empty
        subject_values = []

        # Open file and start MARCReader
        with open(file, 'rb') as fh:
            reader = pymarc.MARCReader(fh, to_unicode=True, force_utf8=True)

            for record in reader:

                try:
                    get_values(subject_values, subject_code, record_no, record)
                    record_no += 1

                except Exception as error:
                    print(str(record_no))
                    print(error)
                    record_no += 1

        fh.close()

        # If subject_values is not empty, create output file
        if subject_values:
            output_values(file, subject_code, subject_values)


if __name__ == '__main__':
    main()
