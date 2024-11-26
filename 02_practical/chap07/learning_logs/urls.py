"""learning_logsのURLパターンの定義"""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # ホームページ
    path('', views.index, name='index'),
    # すべてのトピックを表示するページ
    path('topics/', views.topics, name='topics'),
    # 個別のトピックを表示するページ
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # 新しいトピックを追加するページ
    path('new_topic/', views.new_topic, name='new_topic'),
    # 新規記事の追加ページ
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
]
