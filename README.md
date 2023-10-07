# 概要
jpxCrawlerは、JPX（日本取引所グループ）の新規上場企業情報をクロールし、AWS RDSに保存するプロジェクトです。

# ローカル環境構築
1. `.env`を管理者に連絡してもらってディレクトリのルートにおいて下さい。
2. `docker compose build`
3. `docker compose up -d`



# コンテナ内でcronを実行する方法
1. crawler_appコンテナに接続します。
`docker compose exec crawler_app bash`
2. `crontab -e`コマンドを実行し、以下のように記述します。
`* * * * * env POSTGRES_DB=sample_db POSTGRES_USER=sample POSTGRES_PASSWORD=sample_pass POSTGRES_HOST=sample_host  /usr/local/bin/python3 /app/data/script.py >> /app/data/logfile.log 2>> /app/data/error.log
`
※pythonのパスに気をつけて下さい。
コンテナ内で`which python3`を実行して出力されたパスにして下さい。

