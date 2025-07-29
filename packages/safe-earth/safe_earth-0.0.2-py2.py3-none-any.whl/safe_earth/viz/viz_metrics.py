import plotly.express as px
import pandas as pd

def territories(metrics):

    if type(metrics) == dict:
        metrics = [metrics]
    if not type(metrics) == list:
        raise ValueError('Passed in argument must be a dictionary of metrics or a list of them')

    
