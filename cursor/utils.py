from datetime import datetime, timedelta

def ordinal_to_date(num):
    """ordinal（整数）を日付に変換"""
    return datetime.fromordinal(int(num))

def generate_date_marks(min_date, max_date):
    """
    min_date から max_date の各日付に対し、RangeSlider 用のマークを生成。
    月初のみ表示し、それ以外は非表示にする。
    ただしハンドル上では全日付とも 'YYYY/MM/DD' が表示される。
    """
    marks = {}
    current = min_date
    while current <= max_date:
        # ハンドルに表示したい文字列
        label_str = current.strftime('%Y/%m/%d')

        if current.day == 1:
            # 月が変わるタイミング(1日)のみトラックに表示
            marks[current.toordinal()] = {
                'label': label_str,
                'style': {}  # ラベルを表示
            }
        else:
            # それ以外の日付は非表示（ハンドルには表示される）
            marks[current.toordinal()] = {
                'label': label_str,
                'style': {'display': 'none'}
            }

        current += timedelta(days=1)

    return marks 