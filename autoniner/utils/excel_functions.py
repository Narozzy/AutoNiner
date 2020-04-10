import pandas as pd
from openpyxl import Workbook, load_workbook
import xlrd
import datetime
import math
import fire
from collections import OrderedDict
import ast
import string

def select_rows_regex( raw_table, filter_column_str, regex_filter_str ):

    filtered_table = raw_table[ raw_table.loc[:,(filter_column_str) ].str.contains( regex_filter_str )].copy()

    return filtered_table

def partition_table( raw_table, filter_column_str, regex_filter_arr ):

    partitioned_tables = list()

    for regex_filter in regex_filter_arr:
        partitioned_tables.append( select_rows_regex( raw_table, filter_column_str, regex_filter ))

    return partitioned_tables

def dateFormat( raw_table, column_name, date_format ):
    formatted_table = raw_table.copy()
    # This is necessary to convert from excel DT format -> python DT.
    formatted_table[column_name] = pd.TimedeltaIndex(formatted_table[column_name].astype('float'), unit='d') + datetime.datetime(1899, 12, 30)
    # formatted_table[column_name] = formatted_table[column_name].dt.strftime( date_format )
    return formatted_table

def main():
    raw_data = pd.read_excel('test-doorcount.xlsx')

    filter_list = ['North|Coffee','^S']

    filtered_datatable_list = partition_table(raw_data, 'sensor_id', filter_list)

    south_table = filtered_datatable_list[1]

    copied_table = dateFormat(south_table,"start_time","%m/%d/%Y %I:%M %p")

    print(copied_table[['sensor_id','start_time','in_count','end_time','out_count']])

    copied_table = dateFormat(south_table,"end_time","%m/%d/%Y %I:%M %p")

    print(copied_table[['sensor_id','start_time','in_count','end_time','out_count']])

if __name__ == '__main__':
    fire.Fire(main)