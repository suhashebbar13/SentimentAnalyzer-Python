import csv
import itertools
with open('Output Data Structure.csv','r') as f, open('Input.csv','r') as g:
    reader1= list(csv.reader(g))
    reader2 = list(csv.reader(f))
    for a, b in itertools.product(reader1[1:], reader2[1:]):
        if a[0]==b[0]:
            print(a[0])
