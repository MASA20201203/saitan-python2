from operator import itemgetter

import requests

# API呼び出しを作成してそのレスポンスを格納する
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# 各投稿についての情報を処理する
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:5]:
    # 投稿ごとに、API呼び出しを作成する
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    submission_r = requests.get(url)
    print(f"id: {submission_r.status_code}")
    response_dict = submission_r.json()

    submission_dict = {
        "title": response_dict["title"],
        "link": f"http://news.ycombinator.com/item?id={submission_id}",
        "comments": response_dict['descendants'],
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter("comments"),
                            reverse=True)

for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dict['title']}")
    print(f"Discussion link: {submission_dict['link']}")
    print(f"Comments: {submission_dict['comments']}")
