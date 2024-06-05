# ADIF to CSV

This is an improved version based on https://github.com/timseed/adif_to_csv

This version differs with the following:
- that removes some of the strong assumptions of the original implementation where all the ADIF lines have the same
  amount of fields
- add reprocessing to the out to fix and format some fields and generate new ones

## Usage

```
ADIF=/path/to/adif/file.adif
python main.py $ADIF
```

The resulting CSV will be shown as output and save as a new file with the .csv extension.
