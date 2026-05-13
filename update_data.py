import yfinance as yf
import json
import os
from datetime import datetime

# 定義要追蹤的金流指標
SYMBOLS = {
    "USD_Index": "DX-Y.NYB",   # 美元指數 (金流回流美國的指標)
    "Gold": "GC=F",           # 黃金 (避險情緒指標)
    "US_10Y_Bond": "^TNX",    # 美債 10 年收益率 (全球無風險利率基準)
    "Bitcoin": "BTC-USD",     # 比特幣 (風險資產流向)
    "TWD": "TWD=X"            # 匯率示例
}

def update_json():
    filename = 'data.json'
    data = {}

    # 如果已有檔案，先讀取
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)

    for name, ticker in SYMBOLS.items():
        # 決定抓取範圍：若無舊數據則抓 10 年，有則抓近 1 個月(含修復邏輯)
        period = "10y" if name not in data else "1mo"
        df = yf.Ticker(ticker).history(period=period)
        
        if name not in data: data[name] = {}
        
        for date, row in df.iterrows():
            date_str = date.strftime('%Y-%m-%d')
            data[name][date_str] = round(row['Close'], 2)

    # 寫回檔案
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    update_json()
