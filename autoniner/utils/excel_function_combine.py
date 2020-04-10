#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

#Filter for all north entrances
#df_northentrance = df[df['sensor_id'] == 'North Entrance' && df[df['sensor_id'] == 'Exit']
#print('In count:', df_northentrance['in_count'].sum())
#print('Out count:', df_northentrance['out_count'].sum())

#df_northentrance = df[df['sensor_id'] == 'SE Entrance']
#print('In count:', df_northentrance['in_count'].sum())
#print('Out count:', df_northentrance['out_count'].sum())
# Filter function
def get_count_for_1val(df, col, filterby):
    new_df = df[df[col] == filterby]
    print('In count:', new_df['in_count'].sum())
    print('Out count:', new_df['out_count'].sum())

def get_count_for_2val(df, col, filterby1, filterby2):
    l1 = [filterby1, filterby2]
    new_df = df[df[col].isin(l1)]
    print('In count:', new_df['in_count'].sum())
    print('Out count:', new_df['out_count'].sum())


def filter_equals_cols(df, col_name, value):
    df = df[df[col_name] == value]
    display_df(df)
def filter_greaterthan_cols(df, col_name, value):
    df = df[df[col_name] >= value]
    display_df(df)
def filter_lessthan_cols(df, col_name, value):
    df = df[df[col_name] <= value]
    display_df(df)
# Display function
def display_df(df):
    ddf_html = df.to_html()
    text_file = open("index.html", "w")
    text_file.write(ddf_html)
    text_file.close()

# filter_col = function for a text box
# filter_val = function for a text box

get_count_for_2val(df, 'sensor_id', 'North Entrance', 'North Exit')
print('---------------------------------------------------------')
get_count_for_2val(df, 'sensor_id', 'SE Entrance', 'SE Exit')
print('---------------------------------------------------------')
get_count_for_1val(df, 'sensor_id', 'SW Exit')
print('---------------------------------------------------------')
get_count_for_1val(df, 'sensor_id', 'Coffee Shop')
print('---------------------------------------------------------')
get_count_for_1val(df, 'sensor_id', 'ARC')
