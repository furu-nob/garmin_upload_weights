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

# --- CSV読み込み ---
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"CSV読み込み失敗: {e}")
    sys.exit(1)

# --- 登録処理（体重のみ） ---
element_weight_scale = {
    'date_col' : "年月日",
    'weight_col' : "体組成計 - 体重[kg]",
    'percent_fat_col' : "体組成計 - 体脂肪率[%]",
    'percent_hydration_col' : None,
    'visceral_fat_mass_col' : None,
    'bone_mass_col' : "体組成計 - 推定骨量[kg]",
    'muscle_mass_col' : "体組成計 - 筋肉量[kg]",
    'basal_met_col' : "体組成計 - 基礎代謝量[kcal]",
    'active_met_col' : None,
    'physique_rating_col' : None,
    'metabolic_age_col' : "体組成計 - 体内年齢[才]",
    'visceral_fat_rating_col' : "体組成計 - 内臓脂肪レベル[]",
    'bmi_col' : None
}

# date_col = "年月日"                                     # timestamp タイムスタンプ
# weight_col = "体組成計 - 体重[kg]"                      # weight 体重
# percent_fat_col = "体組成計 - 体脂肪率[%]"              # percent_fat 体脂肪率
# percent_hydration_col = None                            # percent_hydration 水分率
# visceral_fat_mass_col = "体組成計 - 内臓脂肪レベル[]"   # visceral_fat_mass 内臓脂肪量
# bone_mass_col = "体組成計 - 推定骨量[kg]"               # bone_mass 骨量
# muscle_mass_col = "体組成計 - 筋肉量[kg]"               # muscle_mass 筋肉量
# basal_met_col = "体組成計 - 基礎代謝量[kcal]"           # basal_met 基礎代謝量
# active_met_col = None                                   # active_met 活動量
# physique_rating_col = None                              # physique_rating 体格評価
# metabolic_age_col = "体組成計 - 体内年齢[才]"           # metabolic_age 代謝年齢
# visceral_fat_rating_col = None                          # bmi BMI
# bmi_col = None

for index, row in df.iterrows():
    try:
        date_obj = datetime.datetime.strptime(row[element_weight_scale['date_col']], "%Y/%m/%d")
        timestamp = date_obj.isoformat()
        
        if element_weight_scale['weight_col'] is not None:
            weight = float(row[element_weight_scale['weight_col']])
        else:
            weight = None
        if element_weight_scale['percent_fat_col'] is not None:
            percent_fat = float(row[element_weight_scale['percent_fat_col']])
        else:
            percent_fat = None
        if element_weight_scale['percent_hydration_col'] is not None:
            percent_hydration = float(row[element_weight_scale['percent_hydration_col']])
        else:
            percent_hydration = None
        if element_weight_scale['visceral_fat_mass_col'] is not None:
            visceral_fat_mass = float(row[element_weight_scale['visceral_fat_mass_col']])
        else:
            visceral_fat_mass = None
        if element_weight_scale['bone_mass_col'] is not None:
            bone_mass = float(row[element_weight_scale['bone_mass_col']])
        else:
            bone_mass = None
        if element_weight_scale['muscle_mass_col'] is not None:
            muscle_mass = float(row[element_weight_scale['muscle_mass_col']])
        else:
            muscle_mass = None
        if element_weight_scale['basal_met_col'] is not None:
            basal_met = float(row[element_weight_scale['basal_met_col']])
        else:
            basal_met = None
        if element_weight_scale['active_met_col'] is not None:
            active_met = float(row[element_weight_scale['active_met_col']])
        else:
            active_met = None
        if element_weight_scale['physique_rating_col'] is not None:
            physique_rating = float(row[element_weight_scale['physique_rating_col']])
        else:
            physique_rating = None
        if element_weight_scale['metabolic_age_col'] is not None:
            metabolic_age = float(row[element_weight_scale['metabolic_age_col']])
        else:
            metabolic_age = None
        if element_weight_scale['visceral_fat_rating_col'] is not None:
            visceral_fat_rating = float(row[element_weight_scale['visceral_fat_rating_col']])
        else:
            visceral_fat_rating = None
        if element_weight_scale['bmi_col'] is not None:
            bmi = float(row[element_weight_scale['bmi_col']])
        else:
            bmi = None

    except Exception as e:
        print(f"データ変換エラー（{row}）: {e}")
        continue

    try:
        client.add_body_composition(
    #         weight=weight,
    #         percent_fat=None,
    #         percent_hydration=None,
    #         bone_mass=None,
    #         muscle_mass=None,
    #         bmi=None,
    #         timestamp=timestamp
             
            timestamp=timestamp,
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
        print(f"✅ {timestamp} の体組成データをアップロードしました")
        print('weight : '+ str(weight))
        print('percent_fat : '+ str(percent_fat))
        print('percent_hydration : '+ str(percent_hydration))
        print('visceral_fat_mass : '+ str(visceral_fat_mass))
        print('bone_mass : '+ str(bone_mass))
        print('muscle_mass : '+ str(muscle_mass))
        print('basal_met : '+ str(basal_met))
        print('active_met : '+ str(active_met))
        print('physique_rating : '+ str(physique_rating))
        print('metabolic_age : '+ str(metabolic_age))
        print('visceral_fat_rating : '+ str(visceral_fat_rating))
        print('bmi : '+ str(bmi))

    except Exception as e:
        print(f"❌ アップロード失敗: {e}")
