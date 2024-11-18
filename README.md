This repository is a collection of relatively simple pymarc scripts that I've written to analyze MARC data.  I created each one for specific use cases, but wanted to have one central place to keep track of them.

**1. toc_length.py** - Calculates the average length of tables of contents in the 505 field for a set of MARC records.

**2. encoding_level.py** - Counts the number of unique values in the encoding level fixed field (LDR/18) for a set of records.

**3. record_set_compare.py** - Takes two files of MARC records, and outputs a list of which record identifiers are unique in each file (i.e. found in one file but not the other). Uses field 001 as unique identifier.

**4. subject_codes.py** - Extracts the subject source codes from 6XX $2 from a set of records, and counts the number of records (not the number of fields) that have each code.

**5. subject_codes_noLCSH.py** - Similar to subject_codes.py, but excludes all records that have LCSH subjects in a 6XX field.

**6. subject_codes_values.py** - You give it a subject code (e.g. "fast"), and it extracts all 6XX fields from a set of records where that code appears in $2.

**7. subject_values_uniq.py** - Similar to subject_codes_values, but it deduplicates subjects so outputs a list of unique subjects for a given subject code.

**8. subject_codes_identifiers.py** - Again, similar to the other subject scripts, but this one returns all 001 fields (MMS ID) where a given subject codes appears in the record.

**9. mmsid_export.py** - Exports a plain list of all MMS IDs in a given set of MARC records. Useful for getting a list of MMS IDs to paste into Alma Analytics.

**10. field_export.py** - Exports the MMS ID and complete field value for a given MARC field.  (E.g., exports all 710 fields along with their MMS ID)

Some scripts accept input and output files as command line arguments, and others have filenames encoded as variables.
