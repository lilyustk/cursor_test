from dash import Dash
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
from cursor.layout import create_layout
from cursor.constants import HTML_TEMPLATE
from cursor.callbacks import register_callbacks

def load_data():
    """データの読み込みと前処理を行う"""
    print("データを読み込み中...")
    
    try:
        # CSVファイルの読み込み
        print("CSVファイルを読み込み中: test_2409_250111.csv")
        df = pd.read_csv('test_2409_250111.csv', low_memory=False)
        print(f"CSVファイル読み込み完了。データ数: {len(df)}")
        
        # 日付列の変換
        df['Date'] = pd.to_datetime(df['Date'])
        
        # 欠損値の確認
        print("\n欠損値の数:")
        print(df.isnull().sum())
        
        # CompanyNameカラムの欠損値を確認
        if df['CompanyName'].isnull().any():
            print("\nCompanyNameカラムの欠損値を含む行を削除します")
            df = df.dropna(subset=['CompanyName'])
            print(f"欠損値を削除後のデータ数: {len(df)}")
        
        # 利用可能な銘柄を表示
        print("\n利用可能な銘柄:")
        print(sorted(df['CompanyName'].unique()))
        
        # 半導体銘柄のフィルタリング（実際の銘柄名に合わせて修正）
        semiconductor_stocks = [
            'アドバンテスト', 'ディスコ', 'レーザーテック', 'SCREEN HD', '東京エレクトロン',
            'ルネサスエレクトロニクス', 'ソニーグループ', '太陽誘電', 'TDK', '村田製作所',
            '日本電産', '日東電工', '信越化学工業', 'SUMCO', 'SUMCO'
        ]
        
        # カラム名の確認
        print("\n利用可能なカラム:", df.columns.tolist())
        
        # CompanyNameカラムが存在するか確認
        if 'CompanyName' not in df.columns:
            print("エラー: CompanyNameカラムが見つかりません")
            return None
            
        df = df[df['CompanyName'].isin(semiconductor_stocks)]
        print(f"\n半導体銘柄のデータ数: {len(df)}")
        
        if len(df) == 0:
            print("エラー: 半導体銘柄のデータが見つかりません")
            return None
            
        # 日付範囲の表示
        print(f"データの日付範囲: {df['Date'].min()} から {df['Date'].max()}")
        
        return df
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return None

def create_app():
    """Dashアプリケーションを作成"""
    print("アプリケーションを作成中...")
    
    # データの読み込み
    df = load_data()
    if df is None:
        print("データの読み込みに失敗しました")
        return None
        
    print(f"データ読み込み完了。データフレームの形状: {df.shape}")
    
    # 日付範囲の計算
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    min_ordinal = min_date.toordinal()
    max_ordinal = max_date.toordinal()
    
    print("レイアウトを設定中...")
    app = Dash(__name__, 
               external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    # HTMLテンプレートの設定
    app.index_string = HTML_TEMPLATE
    
    app.layout = create_layout(df, min_date, max_date, min_ordinal, max_ordinal)
    
    # コールバックの登録
    print("コールバックを登録中...")
    register_callbacks(app, df)
    
    return app

if __name__ == '__main__':
    print("アプリケーションを起動中...")
    app = create_app()
    if app is not None:
        app.run_server(debug=True)
    else:
        print("アプリケーションの起動に失敗しました") 