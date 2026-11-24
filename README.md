# mini-ticket-app

[チケット管理 / チケットを受け取って優先順位別に管理するアプリ]

## 背景・ゴール（完了基準）
- **背景**: タスクをチケットとして受け取ってチーム内で管理する
- **MVPのゴール**:
  - [ ] チケットの作成・一覧表示・ステータス更新ができる
  - [ ] 担当者ごとにフィルタリングできる

## 技術スタック
- **Frontend**: [無し]
- **Backend**: []
- **Infrastructure / Tools**: [GitHub Actions]

## ディレクトリ構成
※AIや開発者が参照先を迷わないよう、主要なフォルダの役割を記載します。

```text
mini-ticket-app/
├─.pytest_cache
│  │  .gitignore
│  │  CACHEDIR.TAG
│  │  README.md
│  │
│  └─v
│      └─cache
│              lastfailed
│              nodeids
│              stepwise
│
├─app                              # 画面・ルーティング
│  │  database.py
│  │  main.py
│  │  models.py
│  │
│  ├─templates
│  │      index.html
│  │
│  └─__pycache__
│          database.cpython-312.pyc
│          main.cpython-312.pyc
│          models.cpython-312.pyc
│
├─static
│      app.js
│
└─tests                          # テストコード
    │  test_tickets.py
    │
    ├─.pytest_cache
    │  │  .gitignore
    │  │  CACHEDIR.TAG
    │  │  README.md
    │  │
    │  └─v
    │      └─cache
    │              lastfailed
    │              nodeids
    │              stepwise
    │
    └─__pycache__
            test_tickets.cpython-312-pytest-8.3.3.pyc

```

## 環境構築・起動手順

### 1. リポジトリのクローン
```bash
git clone https://github.com:fubukioguri1-bit/mini-ticket-app.git
cd mini-ticket-app
```

### 2. 環境変数の設定
```bash
cp .env.example .env
# .env ファイルを開き、必要なAPIキーやDB接続情報を設定してください
```

### 3. 依存パッケージのインストールと起動
```bash
npm install
npm run dev
```
ブラウザで `http://localhost:3000` にアクセスして動作を確認します。

## 開発ルール・運用
- 作業は **Issue単位** で分割し、1つずつ完了させてから次の作業へ進む。
- 機密情報（APIキーやパスワード）は絶対にコミットせず、`.env` で管理する。
- プルリクエスト作成前にテストとセキュリティチェックを通す。