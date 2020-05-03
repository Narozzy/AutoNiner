#Install python using anaconda because it installs pandas and other valuable libraries without additional work
#pip install tkinter
#pip install pandas if not found, should be installed when install anaconda/python

import tkinter as tk
from tkinter import simpledialog
import pandas as pd
import numpy as np
import datetime 
import calendar

ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
# Add filepath in this format: C:\\Users\\hratn\\OneDrive\\Documents\\Desktop\\School\\Checkouts_2019.07.01 through 2020.04.23.xlsx - CheckOuts (1).csv
file_path = simpledialog.askstring(title="File Path", prompt="What's your Filepath?")
# check it out
print(file_path)

if file_path.endswith('.csv'):
	df = pd.read_csv(file_path)
else:
	df = pd.read_excel(file_path)

cols_to_add = ['Event Branch', 'Event Type', 'Borrower Category', 'Item OCLC Number', 'Item Title', 'Item Material Format', 'Item Branch', 'Item Permanent Shelving Location', 'Patron Barcode']

for element in cols_to_add:
	df[element] = np.nan

df['Event Date/Time'] = pd.to_datetime(df['Loan Date'] +' ' + df['Loan Time'])

df = df.rename(columns={'Barcode':'Item Barcode', 'Call Number':'Item Call Number', 'Item Title': 'Title'})
 
  
def findDay(date): 
    born = datetime.datetime.strptime(date, '%m/%d/%Y').weekday() 
    return (calendar.day_name[born]) 
df['Event Day Name'] = df['Loan Date'].apply(findDay)

df.to_csv('{} Updated.csv'.format(file_path.split('\\')[-1]))
