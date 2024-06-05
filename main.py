from adif2csv import adif2csv
import sys
import csv
import tempfile
from datetime import datetime
import re

file = tempfile.NamedTemporaryFile(suffix='.csv',delete=True)
filename = file.name

# convert the adif to csv into a temp file
if len(sys.argv)!=2:
    print("Error: Missing arguments")
    print("Usage: main.py <ADIF>")
    exit(1)
else:
    cvt=adif2csv()
    input=sys.argv[1]
    target=re.sub('.adi.*', '.csv', input)
    cvt.process(input)

    for a in cvt.dump():
        print(''+a, end='')
        file.write(a.encode("utf-8"))
    file.flush()

date_format = '%Y%m%d'
time_format = '%H%M%S'

csvfile = open(filename, newline='')
target = open(target, 'w', newline='')

# augment and transform
csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
writer = csv.DictWriter(target, fieldnames=csv_reader.fieldnames)

csv_reader.fieldnames.append("qso_date_fmt")
csv_reader.fieldnames.append("time_on_fmt")
csv_reader.fieldnames.append("time_off_fmt")
csv_reader.fieldnames.append("rx")
csv_reader.fieldnames.append("tx")
csv_reader.fieldnames.append("call_fs")

writer.writeheader()

for row in csv_reader:
    row["qso_date_fmt"]= datetime.strptime(row["qso_date"], date_format).strftime('%-d %B %Y')
    row["time_on_fmt"]= datetime.strptime(row["time_on"], time_format).strftime('%H:%M:%S')
    row["time_off_fmt"]= datetime.strptime(row["time_off"], time_format).strftime('%H:%M:%S')
    row["tx"]= "{:+03d}".format(int(row["rst_sent"]))
    row["rx"]= "{:+03d}".format(int(row["rst_rcvd"]))
    row["call_fs"]= row["call"].replace("/", "_")
    row["name"] = row["name"].title()
    if row["name"] == "":
        row["name"] == row["call"]
    writer.writerow(row)

# display location of the converted file
print("Converted file:", target.name)
