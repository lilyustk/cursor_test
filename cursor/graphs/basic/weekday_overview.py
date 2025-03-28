import plotly.graph_objects as go

def create_weekday_overview(filtered_df):
    """曜日ごとの平均値動きグラフを生成"""
    fig = go.Figure()
    
    for code in filtered_df['Code'].unique():
        company_data = filtered_df[filtered_df['Code'] == code]
        fig.add_trace(go.Scatter(
            x=company_data['Date'],
            y=company_data['AfternoonAdjustmentClose'],
            name=company_data['CompanyName'].iloc[0],
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title='曜日ごとの平均値動き',
        xaxis_title='日付',
        yaxis_title='株価（円）',
        template='plotly_white',
        showlegend=True,
        height=500,
        xaxis=dict(
            tickformat='%Y-%m-%d',
            tickangle=45
        )
    )
    
    return fig 