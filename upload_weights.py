import sys
import os
import pandas as pd
import datetime
from garminconnect import Garmin
from dotenv import load_dotenv

# --- 環境変数読み込み ---
load_dotenv()
EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")

if not EMAIL or not PASSWORD:
    print("エラー: .env に GARMIN_EMAIL / GARMIN_PASSWORD を設定してください")
    sys.exit(1)

# --- 引数チェック ---
if len(sys.argv) != 2:
    print("使い方: python upload_weights.py <CSVファイルパス>")
    sys.exit(1)

csv_path = sys.argv[1]

# --- CSV読み込み ---
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"CSV読み込み失敗: {e}")
    sys.exit(1)

# --- Garminログイン ---
try:
    client = Garmin(EMAIL, PASSWORD)
    client.login()
except Exception as e:
    print(f"Garminログイン失敗: {e}")
    sys.exit(1)

# --- 既存の体重データ取得（日付だけ記録） ---
existing_dates = set()
try:
    today = datetime.date.today()
    past = today - datetime.timedelta(days=365 * 2)  # 過去2年分
    weights = client.get_body_composition(past.isoformat(), today.isoformat())
    existing_dates = {w["samplePk"]["calendarDate"] for w in weights}
except Exception as e:
    print(f"既存データ取得失敗（続行）: {e}")

# --- 登録処理（重複はスキップ） ---
date_col = "年月日"
weight_col = "体組成計 - 体重[kg]"

for index, row in df.iterrows():
    try:
        date_obj = datetime.datetime.strptime(row[date_col], "%Y/%m/%d")
        date_str = date_obj.strftime("%Y-%m-%d")
        weight = float(row[weight_col])
    except Exception as e:
        print(f"データ変換エラー（{row}）: {e}")
        continue

    if date_str in existing_dates:
        print(f"{date_str} はすでに登録済み、スキップします")
        continue

    try:
        client.upload_weight(date_obj, weight)
        print(f"{date_str} - {weight}kg をアップロードしました")
    except Exception as e:
        print(f"{date_str} アップロード失敗: {e}")
