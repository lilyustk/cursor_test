import plotly.graph_objects as go

def create_stock_patterns(filtered_df):
    """銘柄別曜日パターン分析グラフを生成"""
    fig = go.Figure()
    
    # 曜日の順序を設定
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    for code in filtered_df['Code'].unique():
        stock_data = filtered_df[filtered_df['Code'] == code]
        company_name = stock_data['CompanyName'].iloc[0]
        
        # 曜日ごとの平均値を計算
        weekday_means = stock_data.groupby('WeekdayName')['DailyChange'].mean()
        
        # 色の設定（正の値は青、負の値は赤）
        colors = ['#1E88E5' if mean >= 0 else '#E53935' for mean in weekday_means]
        
        fig.add_trace(go.Bar(
            x=weekday_means.index,
            y=weekday_means.values,
            name=company_name,
            marker_color=colors,
            text=weekday_means.values.round(2),
            textposition='auto',
            showlegend=False
        ))
    
    fig.update_layout(
        title='銘柄別曜日パターン分析',
        xaxis_title='曜日',
        yaxis_title='平均変動率 (%)',
        height=600,
        xaxis=dict(categoryorder='array', categoryarray=weekday_order),
        showlegend=False
    )
    
    return fig 