import os
import datetime
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
from dotenv import load_dotenv

# Garminアカウントのメールアドレスとパスワードを取得
# --- 環境変数読み込み ---
load_dotenv()
EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")

if not EMAIL or not PASSWORD:
    print("エラー: .env に GARMIN_EMAIL / GARMIN_PASSWORD を設定してください")
    sys.exit(1)

# 過去の日付（例：2025年5月14日）に登録したい
target_date = datetime.datetime(2025, 5, 14, 23, 22)
#timestamp = int(target_date.timestamp() * 1000)  # ミリ秒に変換
#timestamp = target_date.strftime("%Y-%m-%d")
timestamp = target_date.isoformat()
print(timestamp)

# 登録したい体組成データ
weight = 70.2                   # 体重
percent_fat = 25.3              # 体脂肪率
percent_hydration = 70.2        # 水分量
visceral_fat_mass = 4.5         # 脂肪量
bone_mass = 3.4                 # 骨量
muscle_mass = 20.3              # 筋肉量
basal_met = 1500                # 基礎代謝
active_met = None                   # 
physique_rating = None              # 
metabolic_age = 40              # 肉体年齢
visceral_fat_rating = 40        # 内臓脂肪率
bmi = 25.3                      # bmi

# --- Garminにログイン ---
try:
    client = Garmin(EMAIL, PASSWORD)
    client.login()
    print("✅ Garminログイン成功")
except GarminConnectAuthenticationError:
    print("❌ 認証エラー：メールアドレスまたはパスワードが間違っています")
    exit(1)
except GarminConnectConnectionError:
    print("❌ 接続エラー：ネットワークまたはGarmin側の障害")
    exit(1)
except GarminConnectTooManyRequestsError:
    print("❌ アクセス過多：しばらく待ってください")
    exit(1)
except Exception as e:
    print(f"❌ その他のエラー: {e}")
    exit(1)

# --- 体組成データをアップロード ---
try:
    client.add_body_composition(
        timestamp=timestamp,  # 過去日付の指定
        weight=weight,
        percent_fat=percent_fat,
        percent_hydration=percent_hydration,
        visceral_fat_mass=visceral_fat_mass,
        bone_mass=bone_mass,
        muscle_mass=muscle_mass,
        basal_met=basal_met,
        active_met=active_met,
        physique_rating=physique_rating,
        metabolic_age=metabolic_age,
        visceral_fat_rating=visceral_fat_rating,
        bmi=bmi
    )
    print(f"✅ {target_date.date()} の体組成データをアップロードしました")
except Exception as e:
    print(f"❌ アップロード失敗: {e}")

