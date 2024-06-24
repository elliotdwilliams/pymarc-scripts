"""Extracts record IDs & language values for records contains a given subject source code.

Iterates through a set of MARC records and outputs record IDs (field 001) and language of
the material (008 and 041), if the record contains any subject terms with a given source
code in $2. Accepts a command line argument of filename or filename pattern to use as input.
If a pattern (e.g. 'subject*.mrc'), enclose it in single quotes when you execute the script.
Output file includes MMS IDs from 001, language values, and an overall count of the number
of records with each language.
"""

import sys
import os
import glob
from collections import Counter
import pymarc


def subject_test(subject_codes, record):
    """Tests 6XX fields to see if codes in $2 match given codes"""

    # Get all subject fields and iterate through them
    # Currently excludes 655
    for subject in record.get_fields(
        '600', '610', '611', '630', '647', '648', '650', '651', '656', '657', '658', '662'
    ):

        # Get subfield 2 if it exists
        code = subject.get_subfields('2')
        if code:
            code = str(code[0])

            # If $2 matches any of the codes in subject_codes, return True
            if code in subject_codes:
                return True
        else:
            continue

    # If no matching subjects found, return False
    return False


def get_identifier(record):
    """Gets MMS ID from 001"""
    for f in record.get_fields('001'):
        record_id = str(f.value())

    return record_id


def get_languages(record):
    """Gets languages from 008 and 041"""
    # Set record_lang as empty list
    record_lang = []

    # Get language from 008
    for f in record.get_fields('008'):
        record_lang.append(str(f.value())[35:38])

    # Get languages from 041 (only subfield a)
    for f in record.get_fields('041'):
        lang_041 = f.get_subfields('a')

        for lang in lang_041:
            # Only add language from 041 if it isn't in 008
            if lang not in record_lang:
                record_lang.append(lang)

    return record_lang


def output_values(lang_name, record_identifiers, lang_count):
    """Creates output file and prints subject values"""

    # Create output file name
    #basename = os.path.splitext(files[0])[0]
    output_file = lang_name + "-subject-ids.txt"

    # Open output file and print results
    with open(output_file, 'w', encoding='utf-8') as f:
        # Print overall counts of languages
        for lang, count in lang_count.items():
            f.write(lang + '\t' + str(count) + '\n')

        f.write("\n" + ("~" * 40) + "\n\n")

        # Print MMS IDs and languages
        for i in record_identifiers:
            f.write(f"{i}\n")
    f.close()


def main():
    # Get input file name/pattern
    INPUT_FILES = sys.argv[1]

    # Get all files that match input file pattern
    files = glob.glob(INPUT_FILES)

    subject_codes = input('Subject codes (separate with commas): ')
    subject_codes = subject_codes.split(",")  # Split input on commas
    subject_codes = [x.strip(" ") for x in subject_codes]  # Trim whitespace from subject codes
    print(subject_codes)

    lang_name = input('Language name (used for output filename): ')

    # Initialize empty record ID list
    record_identifiers = []

    # Initialize empty language counter
    lang_count = Counter()

    for file in files:
        # print(file)

        # Start record count at 1 (useful for error checking)
        record_no = 1

        # Open file and start MARCReader
        with open(file, 'rb') as fh:
            reader = pymarc.MARCReader(fh, to_unicode=True, force_utf8=True)

            # Iterate through records
            for record in reader:

                # Print title to command line (for error checking)
                try:
                    print(str(record_no) + ' ' + record.title)
                except UnicodeEncodeError:
                    print(str(record_no) + '[Title error]')

                try:
                    # Test to see if subject codes found in 6XX fields
                    subject_found = subject_test(subject_codes, record)

                    # If record had a matching subject, add ID and language to record_identifiers
                    if subject_found:
                        record_id = get_identifier(record)
                        record_lang = get_languages(record)

                        record_data = record_id + '\t' + ",".join(str(lang) for lang in record_lang)
                        record_identifiers.append(record_data)
                        print(record_data)

                        # Also add counter of languages to overall language Counter
                        lang_count.update(Counter(record_lang))

                    # print(record_identifiers)
                    record_no += 1

                except Exception as error:
                    print(error)
                    record_no += 1

        fh.close()

    print(lang_count)

    # If record_identifiers is not empty, create output file
    if record_identifiers:
        output_values(lang_name, record_identifiers, lang_count)


if __name__ == '__main__':
    main()


# def get_record_data(subject_codes, record_no, record):
#     """Gets record id if any subject in record matches subject code"""

#     # Print title to command line (for error checking)
#     try:
#         print(str(record_no) + ' ' + record.title)
#     except UnicodeEncodeError:
#         print(str(record_no) + '[Title error]')

#     # Get all subject fields and iterate through them
#     # Currently excludes 655
#     for subject in record.get_fields(
#         '600', '610', '611', '630', '647', '648', '650', '651', '656', '657', '658', '662'
#     ):

#         # Get subfield 2 if it exists
#         code = subject.get_subfields('2')
#         if code:
#             code = str(code[0])

#             # If $2 matches any of the codes in subject_codes, return the record id and language
#             if code in subject_codes:
#                 record_id = get_identifier(record)
#                 record_lang = get_languages(record)

#                 return record_id, record_lang
#         else:
#             continue

#     # If no matching subjects found, return null value
#     return None, None
