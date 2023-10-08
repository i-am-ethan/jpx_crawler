# このスクリプトは、
# 指定されたURLから上場日、会社名、市場区分を取得し、Printで出力します。

import os
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
import re  # 正規表現モジュールをインポート

# 環境変数からDB設定を読み込む
db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_host = os.environ.get('POSTGRES_HOST')

# PostgreSQLに接続
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host
)
cursor = conn.cursor()

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

    # 上場日の不要な部分を取り除く
    listing_date = re.sub(r'（.*?）', '', listing_date).strip()
    # スラッシュをハイフンに置き換える
    listing_date = listing_date.replace('/', '-')
    # 会社名から「代表者インタビュー」を取り除く
    company_name = re.sub(r'代表者インタビュー', '', company_name).strip()

    # 次の行（市場区分が含まれる行）を取得
    next_row = next(rows)
    second_columns = next_row.select('td')
    market = second_columns[0].text.strip()

    # 新しいデータとデータベース内の最新のデータを比較
    if listing_date < latest_date_in_db:
        print("Log:already_exists_data(1):最新のデータはありませんでした。")
        continue
    elif listing_date == latest_date_in_db:
        if company_name in existing_names:
            print("Log:already_exists_data(2):最新のデータはありませんでした。")
            continue

    print(f"データを保存しました。: 上場日: {listing_date}, 会社名: {company_name}, 市場区分: {market}")

    # データベースに保存
    insert = sql.SQL("INSERT INTO companies (listing_date, company_name, market, created_at, updated_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)")
    cursor.execute(insert, (listing_date, company_name, market))

# 変更をコミット
conn.commit()

# データベース接続を閉じる
cursor.close()
conn.close()
