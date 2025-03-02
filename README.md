# mira-calle

みらチャレ

1. env ファイルの作成

- 開発用の env ファイル「.env.dev」ファイルを docker-compose.dev.yml と同じ階層に作成する。
- 本番用の env ファイル「.env.prod」ファイルを docker-compose.prod.yml と同じ階層に作成する。

【例】

```
# MYSQLのルートパスワードがないとコンテナが起動しない
# MYSQL_ROOT_PASSWORD="任意のルートパスワード"
MYSQL_ROOT_PASSWORD=root
# MYSQL_DATABASE="任意のデータベース名"
MYSQL_DATABASE=djangodb
# MYSQL_USER="任意のユーザ名"
MYSQL_USER=django
# MYSQL_PASSWORD="任意のパスワード"
MYSQL_PASSWORD=django
# MYSQL_HOST="MySQLのサービス名"
MYSQL_HOST=db
# MYSQL_PORT="MySQLのポート番号"
MYSQL_PORT=3306

PMA_ARBITRARY=1
# MySQLのサービス名を指定
PMA_HOST=db
PMA_USER=root
# MySQLのrootユーザのパスワード
PMA_PASSWORD=root
```

2. Django のプロジェクト構成を作成する。（最後の「.」ドットを忘れずに！）

```
docker compose -f docker-compose.dev.yml run app django-admin startproject <プロジェクト名> .
```

3. <プロジェクト名>/settings.py を編集する。

- os のモジュールをインポート

```
import os
```

- 全ての場所からアクセス出来るように設定

```
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']
```

- templates ディレクトリの場所を設定

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

- データベースへの接続方法を設定

```
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# MySQLのパラメータを.envから取得
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        # コンテナ内の環境変数をDATABASESのパラメータに反映
        "NAME": os.environ.get("MYSQL_DATABASE"),
        "USER": os.environ.get("MYSQL_USER"),
        "PASSWORD": os.environ.get("MYSQL_PASSWORD"),
        "HOST": os.environ.get("MYSQL_HOST"),
        "PORT": os.environ.get("MYSQL_PORT"),
    }
}
```

- 使用言語とロケーションを設定

```
# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# 言語を日本語に設定
LANGUAGE_CODE = 'ja'
# タイムゾーンをAsia/Tokyoに設定
TIME_ZONE = 'Asia/Tokyo'
```

- static 回りを設定

```
# STATIC_ROOTを設定
# Djangoの管理者画面にHTML、CSS、Javascriptが適用されます
STATIC_ROOT = "/static/"
STATIC_URL = "/static/"
```

4. Django アプリ構成を作成する。

```
docker compose -f docker-compose.dev.yml run app python manage.py startapp <アプリ名>
```

5. <プロジェクト名>/settings.py にアプリを追加する。

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '<アプリ名>',
]
```

6. Docker を削除する。

```
# docker-compose.dev.ymlのコンテナを一括で停止・削除
docker compose -f docker-compose.dev.yml down -v

# Dockerコンテナを一括で削除
docker container rm $(docker ps -a -q)

# Dockerイメージを一括で削除
docker image rm $(docker images -q)

# Dockerのシステムなどを削除（実行後、yを入力）
docker system prune

```

7. Docker を起動する。

```
docker compose -f docker-compose.dev.yml up -d --build
```

8. 起動確認する。

```
http://localhost:8000
```

9. 各 Django のコマンド実行方法。

```
# マイグレーションを実行
docker compose -f docker-compose.dev.yml exec app python manage.py makemigrations <アプリ名> --noinput
docker compose -f docker-compose.dev.yml exec app python manage.py migrate --noinput

# staticのファイルをsettings.pyで指定した場所に集める
docker compose -f docker-compose.dev.yml exec app python manage.py collectstatic --noinput

# スーパーユーザー作成
docker compose -f docker-compose.dev.yml exec app python manage.py createsuperuser
```

10. 本番用の設定

- django/uwsgi.ini をアプリ用に修正する。
- 本番用 Docker を起動する。

```
docker compose -f docker-compose.prod.yml up -d --build
```

11. 開発のルール

#### 新しい機能を追加/既存のソースを修正する時

修正に入る前に、feature ブランチを新しく作成します。  
ブランチ名は、修正内容が分かるように命名をしてください。

```
git checkout develop
git checkout -b "feature/(ブランチ名)"
```

ブランチ名の記述例(ルーティング先を追加する修正をする場合)

```
git checkout -b "feature/add_routes"
```

※このように作成した feature ブランチで作業を開始します。

#### ソース修正完了後

ソースの修正が完了したら、ステージングした後にコミット、push をしていきます。

```
git add .
git commit -m "(コミットメッセージ)"
git push -u origin feature/(ブランチ名)
```

(ブランチ名は改修内容が伝わるように記述)  
例: feature/config.py にルーティング先を追加  
※その後、github 上で PR を作成する。  
→ 相互レビュー？？
