# 曜日関連の定数
WEEKDAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
WEEKDAY_JAPANESE = {
    'Monday': '月曜日',
    'Tuesday': '火曜日',
    'Wednesday': '水曜日',
    'Thursday': '木曜日',
    'Friday': '金曜日'
}

# グラフのスタイル設定
GRAPH_TEMPLATE = 'plotly_white'
AXIS_FONT = dict(family="Segoe UI, Arial, sans-serif", size=12, color="#555")
GRID_COLOR = "rgba(230, 230, 230, 0.5)"
POSITIVE_COLOR = '#18BC9C'
NEGATIVE_COLOR = '#E74C3C'
NEUTRAL_COLOR = '#3498DB'
HEATMAP_COLORSCALE = [
    [0.0, '#E74C3C'],
    [0.5, '#F8F9F9'],
    [1.0, '#18BC9C']
]

# HTMLテンプレート
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
            }
            .dashboard-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background-color: #2C3E50;
                color: white;
                padding: 20px 0;
                margin-bottom: 30px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .card {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 25px;
                padding: 20px;
                transition: all 0.3s ease;
            }
            .card:hover {
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
            }
            .card-header {
                border-bottom: 1px solid #eee;
                padding-bottom: 15px;
                margin-bottom: 15px;
                color: #2C3E50;
            }
            .table-container {
                overflow-x: auto;
            }
            .footer {
                text-align: center;
                padding: 20px 0;
                color: #777;
                font-size: 0.9em;
                margin-top: 40px;
                border-top: 1px solid #eee;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
''' 