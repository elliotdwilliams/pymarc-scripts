"""Extracts unique subject field values from a set of MARC records, based on a given subject source code.

Iterates through a set of MARC records and outputs subject terms with a given source code in $2.
Subject terms are de-duplicated, so output will only include each unique term once. Accepts a
command line argument of filename or filename pattern to use as input, and a filename to use as
the output file. If a pattern given for input files (e.g. 'subject*.mrc'), enclose it in single
quotes when you execute the script.
"""

import sys
import glob
from collections import Counter
import pymarc

INPUT_FILES = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

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
    # for f in record.get_fields('001'):
    #     record_id = str(f.value())

    # Get all subject fields and iterate through them
    # Currently excludes 655
    for subject in record.get_fields(
        '600', '610', '611', '630', '647', '648', '650', '651', '656', '657', '658', '662'
    ):

        # Get subfield 2 if it exists
        code = subject.get_subfields('2')
        if code:
            code = str(code[0])

            # If $2 matches subject_code, add to subject_values set
            if code == subject_code:
                subject_value = (subject.value())
                print(subject_value)
                subject_values.add(subject_value)


def main():

    subject_code = input('Subject code: ')
    # print(subject_code)

    print(files)

    # Initialize empty Counter
    subject_count = Counter()

    for file in files:
        print(file)

        # Restart record count at 1 (useful for error checking)
        record_no = 1

        # Open file and start MARCReader
        with open(file, 'rb') as fh:
            reader = pymarc.MARCReader(fh, to_unicode=True, force_utf8=True)

            for record in reader:

                # Set subject_values as empty set
                subject_values = set()

                try:
                    get_values(subject_values, subject_code, record_no, record)
                    record_no += 1

                except Exception as error:
                    print(str(record_no))
                    print(error)
                    record_no += 1
                
                # Add subjects from current record to overall subject_count Counter
                subject_count.update(Counter(subject_values))
                # print(subject_count)

        fh.close()

    # Open output file and get ready to print results
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for subject, count in subject_count.items():

            # Print subject code and count, separated by a tab
            f.write(subject + '\t' + str(count) + '\n')
            print(subject + '\t' + str(count))
    f.close()


if __name__ == '__main__':
    main()