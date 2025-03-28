from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime
from constants import HTML_TEMPLATE, WEEKDAY_JAPANESE
from utils import generate_date_marks

def create_layout(df, min_date, max_date, min_ordinal, max_ordinal):
    """ダッシュボードのレイアウトを定義"""
    return html.Div([
        # ヘッダー
        html.Div([
            html.H1('半導体関連銘柄の曜日別パフォーマンス分析', 
                    style={'textAlign': 'center', 'padding': '20px 0', 'margin': 0, 'color': 'white'})
        ], className='header'),
        
        # RangeSliderと表示用テキスト、Store
        html.Div([
            html.Label("表示する日付範囲:"),
            dcc.RangeSlider(
                id='date-range-slider',
                min=min_ordinal,
                max=max_ordinal,
                value=[min_ordinal, max_ordinal],
                step=1,
                marks=generate_date_marks(min_date, max_date),
                allowCross=False,
                tooltip={
                    'placement': 'bottom',
                    'always_visible': False
                }
            ),
            html.Div(id='slider-date-display', style={'margin-top': '10px', 'fontWeight': 'bold'}),
            dcc.Store(id='filtered-data'),  # フィルタ済みデータを保持
        ], style={'margin': '20px 0'}),

        # メインコンテンツ
        html.Div([
            # タブコンポーネント
            dcc.Tabs([
                # タブ1: 基本分析
                dcc.Tab(label='基本分析', children=[
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H3('曜日ごとの平均値動き', className='card-header'),
                                dcc.Graph(id='weekday-overview', config={'displayModeBar': False})
                            ], className='card')
                        ], md=6),
                        dbc.Col([
                            html.Div([
                                html.H3('曜日ごとの平均日中変動率', className='card-header'),
                                dcc.Graph(id='intraday-overview', config={'displayModeBar': False})
                            ], className='card')
                        ], md=6)
                    ]),
                    html.Div([
                        html.H3('銘柄ごとの曜日パターン', className='card-header'),
                        dcc.Graph(id='all-stocks-weekday-pattern', config={'displayModeBar': 'hover'})
                    ], className='card'),
                    html.Div([
                        html.H3('銘柄別平均値動き率ヒートマップ', className='card-header'),
                        dcc.Graph(id='heatmap', config={'displayModeBar': 'hover'})
                    ], className='card')
                ]),
                
                # タブ2: 詳細分析
                dcc.Tab(label='詳細分析', children=[
                    html.Div([
                        html.H3('曜日ごとの銘柄別平均値動き率', className='card-header'),
                        dcc.Graph(id='weekday-stock-heatmap', config={'displayModeBar': 'hover'})
                    ], className='card'),
                    html.Div([
                        html.H3('曜日ごとの値動き分布', className='card-header'),
                        dcc.Graph(id='weekday-swarmplot', config={'displayModeBar': 'hover'})
                    ], className='card'),
                    html.Div([
                        html.H3('銘柄別曜日パターン分析', className='card-header'),
                        dcc.Graph(id='stock-weekday-patterns', config={'displayModeBar': 'hover'})
                    ], className='card')
                ])
            ]),
            
            # 統計情報
            html.Div([
                html.Div("※ p値が0.05未満の場合、曜日による値動きに統計的有意差があることを示します"),
                html.Div("※ データソース: test_2409_250111.csv + jquantsapi", style={'fontStyle': 'italic'})
            ], className='footer')
        ], className='dashboard-container')
    ]) 