"""accounts用のURLパターンの定義"""

from django.urls import path, include

app_name = 'accounts'
urlpatterns = [
    # デフォルトの認証URLを取り込む
    path('', include('django.contrib.auth.urls')),
]
