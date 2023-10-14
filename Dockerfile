# 使用するベースイメージ
FROM python:3.9

# OSパッケージの更新、cron、vimのインストール
RUN apt-get update && apt-get install -y cron vim postgresql-client

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# start-cron.shをコピーして実行可能にする
COPY start-cron.sh /start-cron.sh
RUN chmod +x /start-cron.sh