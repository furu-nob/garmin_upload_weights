import sys
import os
import pandas as pd
import datetime
import time
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
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

# --- Garminログイン ---
def get_garmin_client():
    try:
        client = Garmin()
        print("✅ トークンでログイン成功")
        return client
    except FileNotFoundError:
        print("🔄 トークンがないのでログイン処理へ")
        try:
            client = Garmin(EMAIL, PASSWORD)
            client.login()
            print("✅ 初回ログイン成功、トークン保存済み")
            return client
        except GarminConnectAuthenticationError:
            print("❌ 認証エラー（メールアドレス・パスワード確認）")
        except GarminConnectConnectionError:
            print("❌ 通信エラー（ネットワークかGarmin側）")
        except GarminConnectTooManyRequestsError:
            print("❌ アクセス過多（しばらく待って再試行）")
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")
    return None

client = get_garmin_client()
if client is None:
    print("Garminログイン失敗、終了します")
    sys.exit(1)

# --- CSV読み込み ---
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"CSV読み込み失敗: {e}")
    sys.exit(1)

# --- 登録処理（体重のみ） ---
date_col = "年月日"
weight_col = "体組成計 - 体重[kg]"

for index, row in df.iterrows():
    try:
        date_obj = datetime.datetime.strptime(row[date_col], "%Y/%m/%d")
        weight = float(row[weight_col])
        timestamp = int(date_obj.timestamp() * 1000)
    except Exception as e:
        print(f"データ変換エラー（{row}）: {e}")
        continue

    try:
        client.upload_body_composition(
            weight=weight,
            percent_fat=None,
            percent_hydration=None,
            bone_mass=None,
            muscle_mass=None,
            bmi=None,
            timestamp=timestamp
        )
        print(f"{date_obj.date()} - {weight}kg をアップロードしました")
    except Exception as e:
        print(f"{date_obj.date()} アップロード失敗: {e}")
