# このスクリプトは、
# 指定されたURLから上場日、会社名、市場区分を取得し、Printで出力します。

import os
import requests
import json
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
import re  # 正規表現モジュールをインポート

# 新しいデータが追加されたかどうかをトラッキングするフラグ
new_data_added = False  

# 環境変数からDB設定を読み込む
db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_host = os.environ.get('POSTGRES_HOST')

def send_slack_notification(message):
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    headers = {'Content-Type': 'application/json'}
    data = {'text': message}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f'Error: Slack notification failed: {response.text}')

# PostgreSQLに接続
try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host
    )
    cursor = conn.cursor()
    if conn.status == psycopg2.extensions.STATUS_READY:
        print("Database connection successful")
    else:
        print(f"Database connection error: {conn.status}")
except Exception as e:
    print(f"Database connection error: {e}")
    sys.exit(1)  # スクリプトを終了

# DBから最も新しい上場日(listing_date)を取得
cursor.execute("SELECT MAX(listing_date) FROM companies")
latest_date_in_db = cursor.fetchone()[0]

# 最も新しいlisting_dateに対応するすべてのcompany_nameを取得
cursor.execute("SELECT company_name FROM companies WHERE listing_date = %s", (latest_date_in_db,))
existing_names = [row[0] for row in cursor.fetchall()]

# JPXの新規上場企業ページからデータを取得
target_url = "https://www.jpx.co.jp/listing/stocks/new/index.html"
response = requests.get(target_url)
response.encoding = 'utf-8'  # エンコーディングをUTF-8に設定
soup = BeautifulSoup(response.text, 'html.parser')

# データを取得
rows = iter(soup.select('.widetable tbody tr'))  # tbody内のtr要素をイテレータに変換

for row in rows:
    first_columns = row.select('td')
    listing_date = first_columns[0].text.strip()
    company_name = first_columns[1].text.strip()
    company_url = first_columns[1].find('a')['href'] if first_columns[1].find('a') else None

    # 上場日の取得
    listing_date_text = first_columns[0].text.strip()
    listing_date_match = re.search(r'(\d{4}/\d{2}/\d{2})', listing_date_text)
    if listing_date_match:
        listing_date = listing_date_match.group(1).replace('/', '-')
    else:
        print(f"正規表現エラー(上場日):開発者に連絡して下さい: {listing_date_text}")
        continue  # マッチしなかった場合、ループの次のイテレーションに進みます

    # 次の行（市場区分が含まれる行）を取得
    next_row = next(rows)
    second_columns = next_row.select('td')
    market = second_columns[0].text.strip()

    # 新しいデータとデータベース内の最新のデータを比較
    if latest_date_in_db is None:
        print("Log:empty_database(0):テーブルにデータがありませんでした。")
        pass
    elif listing_date < latest_date_in_db:
        print("Log:already_exists_data(1):最新のデータはありませんでした。")
        continue
    elif listing_date == latest_date_in_db:
        if company_name in existing_names:
            print("Log:already_exists_data(2):最新のデータはありませんでした。")
            continue

    print(f"データを保存しました。: 上場日: {listing_date}, 会社名: {company_name}, URL: {company_url}, 市場区分: {market}")
    new_data_added = True # 新しいデータが追加されたことを示すフラグを立てる
    # Slack通知を送信
    send_slack_notification(f"データが追加されました。: 上場日: {listing_date}, 会社名: {company_name}, URL: {company_url}, 市場区分: {market}")

    # データベースに保存
    insert = sql.SQL("INSERT INTO companies (listing_date, company_name, company_url, market, created_at, updated_at) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
    cursor.execute(insert, (listing_date, company_name, company_url, market))

# 変更をコミット
conn.commit()

# 新しいデータが追加されていない場合にSlackに通知を送信
if not new_data_added:
    send_slack_notification("新しいデータの追加はありませんでした。")

# データベース接続を閉じる
cursor.close()
conn.close()
