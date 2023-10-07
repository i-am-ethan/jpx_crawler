# このスクリプトは、
# 指定されたURLから上場日、会社名、市場区分を取得し、Printで出力します。

import os
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql

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

    # 次の行（市場区分が含まれる行）を取得
    next_row = next(rows)
    second_columns = next_row.select('td')
    market = second_columns[0].text.strip()

    print(f"上場日: {listing_date}, 会社名: {company_name}, 市場区分: {market}")
