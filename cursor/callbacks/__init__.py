from .basic_analysis import register_basic_callbacks
from .detailed_analysis import register_detailed_callbacks

def register_callbacks(app, df):
    """全てのコールバックを登録"""
    register_basic_callbacks(app, df)
    register_detailed_callbacks(app, df) 