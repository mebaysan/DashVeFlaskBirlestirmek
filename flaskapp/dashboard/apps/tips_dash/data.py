"""Dash'e göndereceğimiz veri setini/setlerini okuduğumuz dosya"""

import pandas as pd
import os

def get_data():
    df = pd.read_csv(os.path.join(os.getcwd(), 'flaskapp', 'dashboard', 'apps', 'tips_dash', 'data.csv'))
    return df