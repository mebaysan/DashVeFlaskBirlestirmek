"""Bu dosya sayesinde bu Dash için kullanacağım veri setini çekiyorum ve gerekiyorsa işliyorum"""
import pandas as pd
import os

def fetch_data():
    df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv')
    df.to_csv(os.path.join(os.getcwd(), 'flaskapp', 'dashboard', 'apps', 'tips_dash', 'data.csv'))
    