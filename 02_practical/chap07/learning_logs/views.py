from django.shortcuts import render, redirect

from .models import Topic
from .forms import TopicForm, EntryForm

def index(request):
    """学習ノートのホームページ"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """すべてのトピックを表示する"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """個別のトピックとそのすべてのエントリを表示する"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """新しいトピックを追加する"""
    if request.method != 'POST':
        # データが送信されていないので空のフォームを作成する
        form = TopicForm()
    else:
        # POSTデータが送信されたのでデータを処理する
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # 空または無効なフォームを表示する
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    """特定のトピックに新しい記事を追加する"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # データが送信されていないので空のフォームを作成する
        form = EntryForm()
    else:
        # POSTデータが送信されたのでデータを処理する
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # 空または無効なフォームを表示する
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
