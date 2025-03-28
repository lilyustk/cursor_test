import plotly.express as px

def create_intraday_overview(filtered_df):
    """曜日ごとの平均日中変動率グラフを生成"""
    # 重複を処理するために、最新のデータのみを使用
    intraday_data = filtered_df.sort_values('Date').drop_duplicates(
        subset=['Date', 'CompanyName'], 
        keep='last'
    )
    
    fig = px.imshow(
        intraday_data.pivot(index='Date', columns='CompanyName', values='IntraDayChange'),
        title='曜日ごとの平均日中変動率',
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