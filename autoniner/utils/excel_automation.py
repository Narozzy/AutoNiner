import pandas as pd
from openpyxl import Workbook, load_workbook
import fire
from collections import OrderedDict

SUPPORTED_FUNCTIONS = {
    'AVERAGE': lambda x: (sum(x))/len(x),
    'DIVISION': lambda x,divisor: x/divisor,

}

SUPPORTED_MODIFIERS = {
    'spaced': lambda x: ' '.join(x)
}

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
        it = it[5:-1]
        args = it.split(',')
    else:
        args = it.split(':')
    return args


def main():
    wb_template = load_workbook('template.xlsx')
    wb_data = pd.read_excel('mock_data.xlsx')
    ws_template = wb_template.active
    forms = construct_template_headers(ws_template)
    for col,item in forms.items():
        a = parse_item(item)
        print()

    print()

if __name__ == '__main__':
    fire.Fire(main)