import ast
import string
import matplotlib as mpl
import numpy as np
import datetime
import pandas as pd
import fire
import utils.excel_functions as ef
from openpyxl import Workbook, load_workbook
from collections import OrderedDict

jobTypeToDateTimeColsMap = {
    'DOOR': ['start_time', 'end_time', 'tmestamp'],
}

jobTypeColumnsToSave = {
    'DOOR': ['sensor_id', 'tmestamp', 'in_count', 'out_count']
}

master_template_cols = ['Location', 'Time', 'DayOfWeek', 'Month', 'Day', 'Month+Day', 'Term', 'Calendar', 'Semester', 'AY']

master_template_wb = load_workbook(filename='utils/master_lookup.xlsx')
# master_template_wb = load_workbook(filename='autoniner/utils/master_lookup.xlsx')
semesterMap, academicMap, termMap, locationMap = {}, {}, {}, {} # Maps in place of VLOOKUPs

semester_ws = master_template_wb['SemesterLookUp']
academic_ws = master_template_wb['AcadYrLookUp']
term_ws = master_template_wb['TermLookUp']
location_ws = master_template_wb['LocationLookUp']

for r_idx, rval in enumerate(semester_ws.iter_rows(min_row=2, max_row=semester_ws.max_row), start=2):
    semesterMap.update({semester_ws.cell(row=r_idx, column=1).value : semester_ws.cell(row=r_idx, column=2).value})

for r_idx, rval in enumerate(academic_ws.iter_rows(min_row=2, max_row=academic_ws.max_row), start=2):
    academicMap.update({academic_ws.cell(row=r_idx, column=1).value : {'year': academic_ws.cell(row=r_idx, column=2).value, 'order': academic_ws.cell(row=r_idx, column=3).value}})
        
for r_idx, rval in enumerate(term_ws.iter_rows(min_row=2, max_row=term_ws.max_row), start=2):
    termMap.update({term_ws.cell(row=r_idx, column=1).value : term_ws.cell(row=r_idx, column=2).value})

for r_idx, rval in enumerate(location_ws.iter_rows(min_row=2, max_row=location_ws.max_row), start=2):
    locationMap.update({location_ws.cell(row=r_idx, column=1).value : location_ws.cell(row=r_idx, column=2).value})


job_transform_lambdas = {
    'Location': lambda x: locationMap[x['sensor_id']],
}

def door_job_transform(df):
    location_col = []
    term_col = []
    for v in df['sensor_id']:
        location_col.append(locationMap[v])
    df['Location'] = location_col
    df['Time'] = pd.DatetimeIndex(df['tmestamp']).hour
    df['DayOfWeek'] = df['tmestamp'].dt.day_name()
    df['Month'] = df['tmestamp'].dt.strftime('%b')
    return df

def door_job_transform_viz(df):
    location_col = []
    term_col = []
    for v in df['sensor_id']:
        location_col.append(locationMap[v])
    df['Location'] = location_col
    return df

""" @description: to accept a xlsx/csv file and modify the data based on the format encoded within """
def construct_template_headers(ws):
    """ @description: returns an OrderedDict of headers/the encoded value """
    d = OrderedDict()
    for header,encoding in zip(ws[1],ws[2]):
        d.update({header.value:encoding.value})
    return d

def parse_item(i):
    it = i[2:-2] # remove << >>
    if 'FORM' in it:
        it = it[5:-1] # Remove FORM()
        args = it.split(',')
        if ':' in args[0]: # Check if this is suppose to be a list
            args[0] = ast.literal_eval(','.join(args[0].split(':')))
        if args[1][:args[1].find('(')] in FUNCTIONS_W_PARAMS:
            params = args[1][args[1].find('(')+1:args[1].find(')')]
            params = apply_conversions(params)
            funct = args[1][:args[1].find('(')]
            args[1] = [funct,params]
    else:
        args = it.split(':')
    return args


def csv_transform(query_set, task_type):
    df_data = pd.DataFrame.from_records(query_set)
    for col in jobTypeToDateTimeColsMap[task_type]:
        df_data = ef.dateFormat(df_data, col, '%Y-%m-%d')
    df_data = df_data[jobTypeColumnsToSave[task_type]]
    if task_type == 'DOOR':
        df_data = door_job_transform(df_data)
    return df_data

def construct_visualization(instances, task_type: str):
    if task_type == 'DOOR':
        return construct_door_viz(instances)

def construct_door_viz(instances):
    df = pd.DataFrame.from_records(instances)
    df = door_job_transform_viz(df)
    breakpoint()
    return df.plot(x = 'Location', y = 'in_count')