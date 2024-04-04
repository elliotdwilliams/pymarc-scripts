"""Extracts and counts subject source codes from a set of MARC records, excluding records with LCSH subjects.

Iterates through a set of MARC records and checks to see if the record contains 
any LCSH subject terms. If there are no LCSH subjects, extracts the subject source 
codes from each 6XX $2 in that record. Output is a list of all $2 source codes and 
a count of the number of records they occur in (not a count of how many fields). 
Expects two arguments: the .mrc file to accept as input, and a .txt file to print 
output to.
"""

import sys
from collections import Counter
import pymarc

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

# Initialize empty Counter
subject_count = Counter()

# Start record count at 1 (useful for error checking)
record_no = 1

# Open file and start MARCReader
with open(INPUT_FILE, 'rb') as fh:
    reader = pymarc.MARCReader(fh, to_unicode=True, force_utf8=True)

    for record in reader:

        try:
            # Print title to command line (for error checking)
            try:
                print(str(record_no) + " " + record.title)
            except UnicodeEncodeError:
                print("Title error")

            # Create boolean 'lcsh' and set as false
            lcsh = False

            # Create empty subject codes list as a set
            subject_codes = set()

            # Get all subject fields in record
            subjects = record.get_fields('600', '610', '611', '630', '647', '648', '650', '651', '656', '657', '658', '662')

            # Check if any subjects have second indicator = 0
            for subject in subjects:
                if subject.indicator2 == '0':
                    lcsh = True
            
            print(lcsh)

            # If no lcsh terms in record, count subject codes in $2
            if lcsh == False:
                for subject in subjects:

                    # Get subfield 2 if it exists
                    code = subject.get_subfields('2')

                    # If $2 exists, add the value to subject_codes
                    if code:
                        subject_codes.add(code[0])

                print(subject_codes)

            # Add Counter of codes from current record to overall subject_count Counter
            subject_count.update(Counter(subject_codes))
            record_no += 1

        except Exception:
            print("ERROR: Invalid record, no. " + str(record_no))
            record_no += 1

# print(subject_count)
fh.close()

# Open output file and get ready to print results
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for subject, count in subject_count.items():

        # Print subject code and count, separated by a tab
        f.write(subject + '\t' + str(count) + '\n')
        # print(subject + '\t' + str(count))
f.close()
