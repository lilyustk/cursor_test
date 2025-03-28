from dash import Input, Output
from ..graphs.basic import (
    create_weekday_overview,
    create_intraday_overview,
    create_stock_patterns
)
import pandas as pd

def register_basic_callbacks(app, df):
    """基本的な分析用のコールバックを登録"""
    
    @app.callback(
        [Output('weekday-overview', 'figure'),
         Output('intraday-overview', 'figure'),
         Output('all-stocks-weekday-pattern', 'figure')],
        [Input('date-range-slider', 'value')]
    )
    def update_basic_graphs(date_range):
        if date_range is None:
            return {}, {}, {}
            
        # 日付範囲でデータをフィルタリング
        filtered_df = df[
            (df['Date'].dt.date >= pd.Timestamp.fromordinal(date_range[0]).date()) &
            (df['Date'].dt.date <= pd.Timestamp.fromordinal(date_range[1]).date())
        ].copy()
        
        # 日中変動率の計算
        filtered_df['IntraDayChange'] = (filtered_df['Close'] / filtered_df['Open'] - 1) * 100
        
        # 日次変化率の計算
        filtered_df = filtered_df.sort_values(['CompanyName', 'Date'])
        filtered_df['DailyChange'] = filtered_df.groupby('CompanyName')['Close'].pct_change() * 100
        
        # グラフの生成
        weekday_fig = create_weekday_overview(filtered_df)
        intraday_fig = create_intraday_overview(filtered_df)
        pattern_fig = create_stock_patterns(filtered_df)
        
        return weekday_fig, intraday_fig, pattern_fig 