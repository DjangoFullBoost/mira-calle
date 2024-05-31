from django.urls import path
from.views import Signup, login_view, challenge_create, challenge_list, challenge_detail

urlpatterns = [
    # 登録
    path('Signup/', Signup, name='register'),
    # ログイン
    path('login/', login_view, name='login'),
    # チャレンジ一覧
    path('challenges/', challenge_list, name='challenge-create'),
    # チャレンジ作成
    path('challenges/create/', challenge_create, name='challenge-list'),
    # チャレンジ詳細ページ
    path('challenges/xxxx/', challenge_detail, name='challenge-detail'),
]
