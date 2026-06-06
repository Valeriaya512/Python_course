import csv

with open("考試分數_3年6班.csv","r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)