"""Extracts subject field values  from a set of MARC records, based on a given subject source code.

"""

import sys
import pymarc

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]


def get_values(subject_values, subject_code, record_no, record):
    """Gets subject values if they match subject code"""

    # Print title to command line (for error checking)
    try:
        print(str(record_no) + ' ' + record.title)
    except UnicodeEncodeError:
        print('Title error')

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
                subject_value = (record_id + '\t' + str(subject.value()))
                print(subject_value)
                subject_values.append(subject_value)


def main():
    # Start record count at 1 (useful for error checking)
    record_no = 1

    # subject_code = 'gtt'
    subject_code = input('Subject code: ')
    print(subject_code)

    # Initialize empty list of subject values
    subject_values = []

    # Open file and start MARCReader
    with open(INPUT_FILE, 'rb') as fh:
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

    # # Open output file and print results
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for i in subject_values:
            f.write(f"{i}\n")
    f.close()


if __name__ == '__main__':
    main()
