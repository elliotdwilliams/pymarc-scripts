This repository is a collection of relatively simple pymarc scripts that I've written to analyze MARC data.  I created each one for specific use cases, but wanted to have one central place to keep track of them.

**1. toc_length.py** - Calculates the average length of tables of contents in the 505 field for a set of MARC records.

**2. encoding_level.py** - Counts the number of unique values in the encoding level fixed field (LDR/18) for a set of records.

**3. record_set_compare.py** - Takes two files of MARC records, and outputs a list of which record identifiers are unique in each file (i.e. found in one file but not the other). Uses field 001 as unique identifier.

**4. subject_codes.py** - Extracts the subject source codes from 6XX $2 from a set of records, and counts the number of records (not the number of fields) that have each code.

Currently, subject_codes accepts input and output files as command line arguments; the other scripts have filenames encoded as variables.
