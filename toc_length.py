import re
import pymarc

# Import file
FILE = 'Scores 505 test.mrc'

# Create empty list to hold TOC lengths
toc_all = []

# Open file and open MARCReader
with open(FILE, 'rb') as fh:
    reader = pymarc.MARCReader(fh, to_unicode=True)

    # Iterate through records
    for record in reader:

        print(record['035']['a'])

        # Create record-TOC length counter
        record_toc = 0

        # Get all 505 fields in record
        for f in record.get_fields('505'):
            toc = f.value()

            # Use regex to get word count in the 505 value
            res = len(re.findall(r'\w+', toc))

            # Add 505 length to record-TOC counter
            record_toc += res

        print(record_toc)

        # Add record-TOC length to list
        toc_all.append(record_toc)

    # Get average of all lengths in toc_all
    toc_average = sum(toc_all) / len(toc_all)
    print("The average TOC length is: " + str(toc_average))
