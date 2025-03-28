from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import numpy as np
from scipy import stats
from utils import ordinal_to_date

def register_callbacks(app, df):
    """コールバック関数を登録"""
    
    @app.callback(
        [Output('weekday-overview', 'figure'),
         Output('intraday-overview', 'figure'),
         Output('all-stocks-weekday-pattern', 'figure'),
         Output('heatmap', 'figure'),
         Output('weekday-stock-heatmap', 'figure'),
         Output('weekday-swarmplot', 'figure'),
         Output('stock-weekday-patterns', 'figure')],
        [Input('date-range-slider', 'value')]
    )
    def update_graphs(date_range):
        print(f"コールバックが呼び出されました。date_range: {date_range}")
        print(f"データフレームの形状: {df.shape}")
        
        if not date_range:
            print("date_rangeが空です")
            return {}, {}, {}, {}, {}, {}, {}
        
        # 日付範囲でデータをフィルタリング
        start_date = ordinal_to_date(date_range[0])
        end_date = ordinal_to_date(date_range[1])
        print(f"フィルタリング期間: {start_date} から {end_date}")
        
        # 日付の型を合わせる
        df['Date'] = pd.to_datetime(df['Date'])
        filtered_df = df[
            (df['Date'].dt.date >= start_date.date()) & 
            (df['Date'].dt.date <= end_date.date())
        ].copy()
        
        # 曜日情報の追加
        filtered_df['Weekday'] = filtered_df['Date'].dt.dayofweek
        filtered_df['WeekdayName'] = filtered_df['Date'].dt.day_name()
        
        # 日中の値動き率を計算
        filtered_df['IntraDayChange'] = (filtered_df['AfternoonAdjustmentClose'] / filtered_df['MorningAdjustmentClose'] - 1) * 100
        
        # 前日比を計算
        filtered_df = filtered_df.sort_values(['Code', 'Date'])
        filtered_df['DailyChange'] = filtered_df.groupby('Code')['AfternoonAdjustmentClose'].pct_change() * 100
        
        print(f"フィルタリング後のデータ数: {len(filtered_df)}")
        print(f"フィルタリング後の日付範囲: {filtered_df['Date'].min()} から {filtered_df['Date'].max()}")
        
        # 基本分析のグラフ
        # 1. 曜日ごとの平均値動き
        weekday_fig = go.Figure()
        for code in filtered_df['Code'].unique():
            company_data = filtered_df[filtered_df['Code'] == code]
            weekday_fig.add_trace(go.Scatter(
                x=company_data['Date'],
                y=company_data['AfternoonAdjustmentClose'],
                name=company_data['CompanyName'].iloc[0],
                mode='lines+markers'
            ))
        
        weekday_fig.update_layout(
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
        
        # 2. 曜日ごとの平均日中変動率
        intraday_data = filtered_df.sort_values('Date').drop_duplicates(
            subset=['Date', 'CompanyName'], 
            keep='last'
        )
        intraday_fig = px.imshow(
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
        intraday_fig.update_xaxes(tickformat='%Y-%m-%d', tickangle=45)
        
        # 3. 銘柄ごとの曜日パターン
        pattern_data = filtered_df.sort_values('Date').drop_duplicates(
            subset=['Date', 'CompanyName'], 
            keep='last'
        )
        pattern_fig = px.imshow(
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
        pattern_fig.update_xaxes(tickformat='%Y-%m-%d', tickangle=45)
        
        # 4. 銘柄別平均値動き率ヒートマップ
        heatmap_data = filtered_df.sort_values('Date').drop_duplicates(
            subset=['Date', 'CompanyName'], 
            keep='last'
        )
        heatmap_fig = px.imshow(
            heatmap_data.pivot(index='Date', columns='CompanyName', values='DailyChange'),
            title='銘柄別平均値動き率ヒートマップ',
            color_continuous_scale=[
                [0.0, '#E74C3C'],
                [0.5, '#F8F9F9'],
                [1.0, '#18BC9C']
            ],
            aspect='auto',
            height=400
        )
        heatmap_fig.update_xaxes(tickformat='%Y-%m-%d', tickangle=45)
        
        # 詳細分析のグラフ
        # 5. 曜日ごとの銘柄別平均値動き率ヒートマップ
        weekday_stock_heatmap_data = filtered_df.pivot_table(
            values='DailyChange',
            index='CompanyName',
            columns='WeekdayName',
            aggfunc='mean'
        )
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        weekday_stock_heatmap_data = weekday_stock_heatmap_data[weekday_order]
        
        weekday_stock_heatmap_fig = px.imshow(
            weekday_stock_heatmap_data,
            title='曜日ごとの銘柄別平均値動き率 (%)',
            color_continuous_scale='viridis',
            aspect='auto',
            height=400
        )
        
        # 6. 曜日ごとの値動き分布（Swarmplot）
        weekday_swarmplot_fig = px.strip(
            filtered_df,
            x='WeekdayName',
            y='DailyChange',
            title='曜日ごとの値動き分布',
            color='WeekdayName',
            color_discrete_sequence=px.colors.qualitative.Set3,
            height=400
        )
        weekday_swarmplot_fig.update_xaxes(categoryorder='array', categoryarray=weekday_order)
        
        # 7. 銘柄別曜日パターン分析
        stock_weekday_patterns_fig = go.Figure()
        
        for code in filtered_df['Code'].unique():
            stock_data = filtered_df[filtered_df['Code'] == code]
            company_name = stock_data['CompanyName'].iloc[0]
            
            # 曜日ごとの平均値を計算
            weekday_means = stock_data.groupby('WeekdayName')['DailyChange'].mean()
            
            # 色の設定（正の値は青、負の値は赤）
            colors = ['#1E88E5' if mean >= 0 else '#E53935' for mean in weekday_means]
            
            stock_weekday_patterns_fig.add_trace(go.Bar(
                x=weekday_means.index,
                y=weekday_means.values,
                name=company_name,
                marker_color=colors,
                text=weekday_means.values.round(2),
                textposition='auto',
                showlegend=False
            ))
        
        stock_weekday_patterns_fig.update_layout(
            title='銘柄別曜日パターン分析',
            xaxis_title='曜日',
            yaxis_title='平均変動率 (%)',
            height=600,
            xaxis=dict(categoryorder='array', categoryarray=weekday_order),
            showlegend=False
        )
        
        return (weekday_fig, intraday_fig, pattern_fig, heatmap_fig,
                weekday_stock_heatmap_fig, weekday_swarmplot_fig, stock_weekday_patterns_fig) 