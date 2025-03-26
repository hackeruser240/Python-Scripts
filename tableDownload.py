# This script downloads tables from a wikipedia website

import pandas as pd 
import argparse as ag

url = "https://en.wikipedia.org/wiki/List_of_bomber_aircraft"

table=pd.read_html(url)

df=table[0] #this downloads the first occurence of the table found on the page

df.to_csv('sample.csv',index=True)

print("sample.csv saved")