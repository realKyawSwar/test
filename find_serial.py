import pandas as pd
import re


df = pd.read_csv('regen_conversion300.csv')
df = df.drop(columns=['PROCESS_ID', 'PROCESS_DESC', 'EQUIP_ID', 'EQUIP_DESC',
                      'TROUBLE_ID', 'MACHINE_ID', 'UPDATED_DATE',
                      'UPDATED_BY', 'UPDATED_TIME', 'TROUBLE_STIME',
                      'TROUBLE_ETIME', 'DURATION', 'ATTEND_BY', 'CAUSES'])
df = df.dropna(axis=1, how='all')
# df.columns.tolist()
# get a cell value from action
stringy = df.iloc[33]["ACTION"]

stringy = re.compile("\n").sub(".", stringy)
regex = re.compile(r'\bChange[^\.]*\b | \bChg[^\.]*\b | \bService[^\.]*\b', flags=re.I | re.X)
regex.findall(stringy)

print(regex.findall(stringy))
# '([^.]*apple[^.]*)'
# "\.?([^\.]*parking[^\.]*)"
