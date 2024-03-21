from collections import Counter
import pymarc

FILE = 'Scores M1495 2023-11-01.mrc'

Desc = []

with open(FILE, 'rb') as fh:
    reader = pymarc.MARCReader(fh, to_unicode=True)
    for record in reader:
        # print(record.leader)
        if record.leader[18] == ' ':
            Desc.append('#')
        else:
            Desc.append(record.leader[18])
    print(Desc)
    print(Counter(Desc))
