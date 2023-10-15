<h1 align='center'>JPX Crawler🌈</h1>
<p align='center'>
  JPX Crawlerは、JPX（日本取引所グループ）の
  <a href="https://www.jpx.co.jp/listing/stocks/new/index.html">新規上場企業情報</a>をクローリングし、スラックに通知をしてくれるプロジェクトです。
  <br>
  <small>
    JPXサイトに対するクローリングを行う際は必ず
    <a href="https://www.jpx.co.jp/term-of-use/index.html">サイトのご利用上の注意と免責事項</a>
    を確認して下さい。
  </small>
</p>

## 機能
- 🐛 JPXサイトの新規上場企業情報をクロール
- 🔗 クロール対象はこちらの<a href="https://www.jpx.co.jp/listing/stocks/new/index.html">ページ</a>
- 📡 上場日、会社名、会社URL、市場区分を取得
- 🔔 スラックに通知
- 📦 AWS RDSにデータを保存
- 🔵 crontabにて定期実行

## インフラ構成図
ざっくりインフラ構成図です。
RDSが不要や、Lambdaの方がいいなど思うところはいろいろありますが、業務の構成に近かったこともありこの構成にしています。
<img src="https://github.com/i-am-ethan/images/blob/main/jpx-crawler/aws-architecture.jpg?raw=true" />

## 開発環境構築
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

## cronを実行する方法
### 開発環境
1. crawler_appコンテナに接続します。
`docker compose exec crawler_app bash`
2. `crontab -e`コマンドを実行し、以下のように記述します。
`* * * * * env POSTGRES_DB=sample_db POSTGRES_USER=sample POSTGRES_PASSWORD=sample_pass POSTGRES_HOST=sample_host  /usr/local/bin/python3 /app/data/script.py >> /app/data/logfile.log 2>> /app/data/error.log
`
<small>※ENVは適宜変更して下さい。</small>
<small>※pythonのパスに気をつけて下さい。
コンテナ内で`which python3`を実行して出力されたパスにして下さい。</small>

## 本番環境
crontabを開きます。
`crontab -e`
以下のように記述します。
<small>※envの内容は適宜書き換えて下さい。</small>
`* * * * * env POSTGRES_DB=sample POSTGRES_USER=sample POSTGRES_PASSWORD=sample POSTGRES_HOST=sample SLACK_WEBHOOK_URL=sample /usr/local/bin/python3 /app/data/script.py >> /app/data/logfile.log 2>> /app/data/error.log
`

## 本番ソフトウェアVersion

### docker
`docker --version`
Docker version 20.10.23, build 7155243
### docker-compose
`docker-compose --version`
Docker Compose version v2.22.0

## やっていないこと
- 自動デプロイ
- テストコード

## 開発環境でよく実行したコマンドなど

### テーブルデータ削除
ローカルのテストで削除したいときに使う。
シーケンスも同時にリセットする。
`TRUNCATE companies RESTART IDENTITY;`

### git
`git stash --include-untracked`
`git fetch origin`
`git diff main..origin/main`
`git pull origin main`

### cronが動かない時
`service cron status`でcronが動いているか確認する
cron is not running ... failed!
だった場合は、cronを起動する
`service cron start`を実行する
参考:https://qiita.com/jerrywdlee/items/d4468f076bdea236bf3b

### Slack APIで通知する
参考:https://qiita.com/to3izo/items/c2d16f8b3e52b09e543e

