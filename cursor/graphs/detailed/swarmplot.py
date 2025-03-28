import plotly.express as px

def create_swarmplot(filtered_df):
    """曜日ごとの値動き分布グラフを生成"""
    # 曜日の順序を設定
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    fig = px.strip(
        filtered_df,
        x='WeekdayName',
        y='DailyChange',
        title='曜日ごとの値動き分布',
        color='WeekdayName',
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=400
    )
    
    fig.update_xaxes(categoryorder='array', categoryarray=weekday_order)
    
    return fig 