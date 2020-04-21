import datetime
import numpy as np
import pandas as pd
import matplotlib as mpl

def construct_visualization(instances, task_type: str):
    if task_type == 'DOOR':
        construct_door_viz(instances)

def construct_door_viz(instances):
    df = pd.DataFrame.from_records(instances)
    