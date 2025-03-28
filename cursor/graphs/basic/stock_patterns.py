import plotly.express as px

def create_stock_patterns(filtered_df):
    """銘柄ごとの曜日パターングラフを生成"""
    # 重複を処理するために、最新のデータのみを使用
    pattern_data = filtered_df.sort_values('Date').drop_duplicates(
        subset=['Date', 'CompanyName'], 
        keep='last'
    )
    
    fig = px.imshow(
        pattern_data.pivot(index='Date', columns='CompanyName', values='DailyChange'),
        title='銘柄ごとの曜日パターン',
        color_continuous_scale=[
            [0.0, '#E74C3C'],
            [0.5, '#F8F9F9'],
            [1.0, '#18BC9C']
        ],
        aspect='auto',
        height=400
    )
    fig.update_xaxes(tickformat='%Y-%m-%d', tickangle=45)
    
    return fig 