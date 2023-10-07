# 使用するベースイメージ
FROM python:3.9

# OSパッケージの更新、cron、vimのインストール
RUN apt-get update && apt-get install -y cron vim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt