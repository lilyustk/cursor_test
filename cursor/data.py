import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import jquantsapi
import warnings

warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)

# 定数定義
SEMICONDUCTOR_CODES = [
    '80350',  # 東京エレクトロン
    '67230',  # ルネサスエレクトロニクス
    '40630',  # 信越化学工業
    '68570',  # アドバンテスト
    '61460',  # ディスコ
    '68710',  # 日本マイクロニクス
    '65260'   # ソシオネクスト
]

CODE_TO_NAME = {
    '80350': '東京エレクトロン',
    '67230': 'ルネサスエレクトロニクス',
    '40630': '信越化学工業',
    '68570': 'アドバンテスト',
    '61460': 'ディスコ',
    '68710': '日本マイクロニクス',
    '65260': 'ソシオネクスト'
}

# J-Quants API認証情報
MY_MAIL_ADDRESS = "lilyustk@yahoo.co.jp"
MY_PASSWORD = "Lizerable333"
CSV_FILE_PATH = "test_2409_250111.csv"

def load_data():
    """CSVを読み込み、最新日付～本日までのデータをjquantsapiで取得し更新したうえで返す"""
    try:
        print(f"CSVファイルを読み込み中: {CSV_FILE_PATH}")
        df = pd.read_csv(CSV_FILE_PATH, low_memory=False)
        print(f"CSVファイル読み込み完了。データ数: {len(df)}")
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません: {CSV_FILE_PATH}")
        return None

    # 半導体銘柄のみ
    df['Date'] = pd.to_datetime(df['Date'])
    df['Code'] = df['Code'].astype('str')
    semi_df = df[df['Code'].isin(SEMICONDUCTOR_CODES)].copy()
    print(f"半導体銘柄のデータ数: {len(semi_df)}")
    print(f"データの日付範囲: {semi_df['Date'].min()} から {semi_df['Date'].max()}")

    if semi_df.empty:
        print("エラー: 半導体銘柄のデータが見つかりません")
        return None

    # 最新日付と本日を比較して差分があれば更新
    max_date = semi_df['Date'].max().date()
    today = datetime.now().date()
    if max_date < today:
        update_start = max_date + timedelta(days=1)
        update_end = today
        start_str = update_start.strftime("%Y%m%d")
        end_str = update_end.strftime("%Y%m%d")
        print(f"データ更新: {start_str} ~ {end_str}")

        try:
            cli = jquantsapi.Client(mail_address=MY_MAIL_ADDRESS, password=MY_PASSWORD)
            new_data = cli.get_price_range(start_dt=start_str, end_dt=end_str)
            if new_data is not None and not new_data.empty:
                new_data['Date'] = pd.to_datetime(new_data['Date'])
                # 既存データと結合
                df = pd.concat([df, new_data], ignore_index=True)
                df.drop_duplicates(subset=['Date','Code'], inplace=True)
                # CSV上書き
                df.to_csv(CSV_FILE_PATH, index=False)
                # 再度半導体銘柄のみ抽出
                semi_df = df[df['Code'].isin(SEMICONDUCTOR_CODES)].copy()
                print("新規データを追加しました。")
            else:
                print("新規データはありません。")
        except Exception as e:
            print(f"データ更新エラー: {e}")

    # 前処理
    semi_df = preprocess_data(semi_df)
    return semi_df

def preprocess_data(semi_df):
    """前処理: 各種列の作成とソート"""
    semi_df['Weekday'] = semi_df['Date'].dt.dayofweek
    semi_df['WeekdayName'] = semi_df['Date'].dt.day_name()
    if 'CompanyName' not in semi_df.columns:
        semi_df['CompanyName'] = semi_df['Code'].map(CODE_TO_NAME)

    # 欠損除外
    for col in ['MorningAdjustmentClose', 'AfternoonAdjustmentClose']:
        semi_df.dropna(subset=[col], inplace=True)

    # 日中変動率
    semi_df['IntraDayChange'] = (
        semi_df['AfternoonAdjustmentClose'] / semi_df['MorningAdjustmentClose'] - 1
    ) * 100

    # 前日比
    semi_df.sort_values(['Code', 'Date'], inplace=True)
    semi_df['DailyChange'] = semi_df.groupby('Code')['AfternoonAdjustmentClose'].pct_change() * 100

    return semi_df

def generate_sample_data():
    """サンプルデータを生成する関数"""
    print("サンプルデータを生成します")
    data = []
    
    # 現在の日付から3ヶ月前を開始日とする
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)  # 約3ヶ月前
    
    # 営業日のみの日付リストを生成
    all_dates = pd.date_range(start=start_date, end=end_date, freq='B')  # 営業日ベース

    base_prices = {
        '80350': 20000,
        '67230': 1800,
        '40630': 16000,
        '68570': 7500,
        '61460': 35000,
        '68710': 1200,
        '65260': 3000
    }

    for code in SEMICONDUCTOR_CODES:
        price = base_prices[code]
        for d in all_dates:
            daily_change = np.random.normal(0, 1)
            morning_price = price * (1 + np.random.normal(0, 0.3)/100)
            afternoon_price = morning_price * (1 + daily_change/100)
            data.append({
                'Date': d,
                'Code': code,
                'MorningAdjustmentClose': morning_price,
                'AfternoonAdjustmentClose': afternoon_price
            })
            price = afternoon_price
    
    df = pd.DataFrame(data)
    df = preprocess_data(df)
    print(f"サンプルデータ生成完了。期間: {df['Date'].min()} から {df['Date'].max()}")
    return df 