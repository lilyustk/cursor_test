import plotly.express as px

def create_weekday_heatmap(filtered_df):
    """曜日ごとの銘柄別平均値動き率ヒートマップを生成"""
    # 曜日ごとの銘柄別平均値を計算
    weekday_stock_heatmap_data = filtered_df.pivot_table(
        values='DailyChange',
        index='CompanyName',
        columns='WeekdayName',
        aggfunc='mean'
    )
    
    # 曜日の順序を調整
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekday_stock_heatmap_data = weekday_stock_heatmap_data[weekday_order]
    
    fig = px.imshow(
        weekday_stock_heatmap_data,
        title='曜日ごとの銘柄別平均値動き率 (%)',
        color_continuous_scale='viridis',
        aspect='auto',
        height=400
    )
    
    return fig 