"""
Dash uygulamalarımıza ait CONFIG sabitlerini bu dosyada URL_PATHS'e ekleyeceğiz
"""
from flaskapp.dashboard.apps.tips_dash import app as tips_dash

URL_PATHS = [
    tips_dash.CONFIG,
]