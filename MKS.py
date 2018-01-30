import csv
import numpy
import pandas as pd

df = pd.read_csv('MKS.csv', header=None)

dup = []
loc = []
name = input('Input name: ')
charts = []

for i in range(len(df)):
    dup.append(df[0][i])
    
loc =([k for k, j in enumerate(dup) if j == name])
    
for i in loc:
    charts.append(df[1][i])


        