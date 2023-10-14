<h1 align='center'>JPX Crawler🌈</h1>
<p align='center'>
  JPX Crawlerは、JPX（日本取引所グループ）の新規上場企業情報をクロールし、AWS RDSに保存するプロジェクトです。<br><small>JPXサイトに対するクローリングを行う際は必ず<a href="https://www.jpx.co.jp/term-of-use/index.html">公式</a>を確認して下さい。</small>
</p>

## 機能
- 🐛 JPXサイトの新規上場企業情報をクロール
- 🔗 クロール対象はこちらの<a href="https://www.jpx.co.jp/listing/stocks/new/index.html">ページ</a>
- 📦 AWS RDSにデータを保存
- ✅ Slackに通知

## ローカル環境構築
1. `.env`を管理者から取得し、ルートにおく。
2. `docker compose build`
3. `docker compose up -d`

## 本番
1. `docker-compose -f docker-compose.prod.yml build`
2. `docker-compose -f docker-compose.prod.yml up -d`
3. `docker-compose -f docker-compose.prod.yml exec crawler_app bash`
4. `docker-compose -f docker-compose.prod.yml ps`
### 本番設定済みエイリアス
`alias dcps='docker-compose -f docker-compose.prod.yml ps'`
`alias dc='docker-compose -f docker-compose.prod.yml'`

## コンテナ内でcronを実行する方法
1. crawler_appコンテナに接続します。
`docker compose exec crawler_app bash`
2. `crontab -e`コマンドを実行し、以下のように記述します。
`* * * * * env POSTGRES_DB=sample_db POSTGRES_USER=sample POSTGRES_PASSWORD=sample_pass POSTGRES_HOST=sample_host  /usr/local/bin/python3 /app/data/script.py >> /app/data/logfile.log 2>> /app/data/error.log
`
<small>※ENVは適宜変更して下さい。</small>
<small>※pythonのパスに気をつけて下さい。
コンテナ内で`which python3`を実行して出力されたパスにして下さい。</small>

## 本番でcronを実行する
`crontab -e`
`* * * * * env POSTGRES_DB=sample POSTGRES_USER=sample POSTGRES_PASSWORD=sample POSTGRES_HOST=sample SLACK_WEBHOOK_URL=sample /usr/local/bin/python3 /app/data/script.py >> /app/data/logfile.log 2>> /app/data/error.log
`

## テーブルデータ削除
ローカルのテストで削除したいときに使う。
シーケンスも同時にリセットする。
`TRUNCATE companies RESTART IDENTITY;`

## 本番ソフトウェアVersion

### docker
`docker --version`
Docker version 20.10.23, build 7155243
### docker-compose
`docker-compose --version`
Docker Compose version v2.22.0

