import pandas as pd
from openpyxl import Workbook, load_workbook
import fire
from collections import OrderedDict
import ast
import string

FUNCTIONS_W_PARAMS = ['DIVISION']
SUPPORTED_FUNCTIONS = {
    'AVERAGE': lambda x: (sum(x))/len(x),
    'DIVISION': lambda x,divisor: x.divide(divisor),
}

SUPPORTED_MODIFIERS = {
    'spaced': lambda x: x.apply(lambda x: ' '.join(x.split(' ')))
}

CONVERSIONS = {
    'int': lambda i: int(i),
}

def apply_conversions(arg):
    if arg.isdigit():
        return CONVERSIONS['int'](arg)
        
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


def main():
    wb_template = load_workbook('template.xlsx')
    df_data = pd.read_excel('mock_data.xlsx')
    ws_template = wb_template.active
    forms = construct_template_headers(ws_template)
    df = pd.DataFrame(columns=forms.keys())
    for col,item in forms.items():
        data = df_data[col]
        cols, feature = parse_item(item)
        if isinstance(feature, list) or feature in SUPPORTED_FUNCTIONS:
            if isinstance(feature,list):
                df[col] = SUPPORTED_FUNCTIONS[feature[0]](data, feature[1])
            else:
                df[col] = SUPPORTED_FUNCTIONS[feature](data)
        else:
            df[col] = SUPPORTED_MODIFIERS[feature](data)

if __name__ == '__main__':
    fire.Fire(main)