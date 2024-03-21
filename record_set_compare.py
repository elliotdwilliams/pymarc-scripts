import pymarc

# Set filename variables
FILE1 = 'NAL_auth_vocab.mrc'
FILE2 = 'NAL_sec_ind_3.mrc'
OUTPUT_FILE = 'record-set-differences.txt'

# Create lists of identifiers
ids1 = []
ids2 = []

# Open file1 and open MARCReader
with open(FILE1, 'rb') as fh:
    reader = pymarc.MARCReader(fh, to_unicode=True)
    for record in reader:

        # Get MMS ID from 001 and append to ids1 list
        for f in record.get_fields('001'):
            record_id = str(f.value())
            ids1.append(record_id)
fh.close()

# Open file2 and open MARCReader
with open(FILE2, 'rb') as fh:
    reader = pymarc.MARCReader(fh, to_unicode=True)
    for record in reader:

        # Get MMS ID from 001 and append to ids1 list
        for f in record.get_fields('001'):
            record_id = str(f.value())
            ids2.append(record_id)
fh.close()

print(ids1)
print(ids2)

# Compare two lists of identifiers
# First, look for ids in file1 that are not in file2
id1_not_2 = []
for element in ids1:
    if element not in ids2:
        id1_not_2.append(element)

# Next, look for ids in file2 that are not in file1
id2_not_1 = []
for element in ids2:
    if element not in ids1:
        id2_not_1.append(element)

print(id1_not_2)
print(id2_not_1)

# Print results to output file
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('File1 = ' + FILE1 + '; ' + str(len(ids1)) + ' records\n')
    f.write('File2 = ' + FILE2 + '; ' + str(len(ids2)) + ' records\n\n')
    f.write('Ids in File1 that are not in File2: \n')
    f.write('\n'.join(str(item) for item in id1_not_2) +
            '\nCount: ' + str(len(id1_not_2)) + ' records\n\n')
    f.write('Ids in File2 that are not in File1: \n')
    f.write('\n'.join(str(item) for item in id2_not_1) +
            '\nCount: ' + str(len(id2_not_1)) + ' records\n')
f.close()
