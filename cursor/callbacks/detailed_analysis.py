from dash import Input, Output
from ..graphs.detailed import (
    create_weekday_heatmap,
    create_swarmplot,
    create_stock_patterns
)
import pandas as pd

def register_detailed_callbacks(app, df):
    """詳細分析のコールバックを登録"""
    
    @app.callback(
        [Output('weekday-stock-heatmap', 'figure'),
         Output('weekday-swarmplot', 'figure'),
         Output('stock-weekday-patterns', 'figure')],
        [Input('date-range-slider', 'value')]
    )
    def update_detailed_graphs(date_range):
        if date_range is None:
            return {}, {}, {}
        
        # 日付範囲でデータをフィルタリング
        filtered_df = df[
            (df['Date'].dt.date >= pd.Timestamp.fromordinal(date_range[0]).date()) &
            (df['Date'].dt.date <= pd.Timestamp.fromordinal(date_range[1]).date())
        ].copy()
        
        # 曜日情報の追加
        filtered_df['WeekdayName'] = filtered_df['Date'].dt.day_name()
        filtered_df['Weekday'] = filtered_df['Date'].dt.dayofweek
        
        # 日次変化率の計算
        filtered_df['DailyChange'] = filtered_df.groupby('CompanyName')['Close'].pct_change()
        
        # グラフの生成
        heatmap_fig = create_weekday_heatmap(filtered_df)
        swarmplot_fig = create_swarmplot(filtered_df)
        patterns_fig = create_stock_patterns(filtered_df)
        
        return heatmap_fig, swarmplot_fig, patterns_fig 