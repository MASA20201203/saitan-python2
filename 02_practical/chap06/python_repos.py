import requests

# API呼び出しを作成してレスポンスを確認する
url = "https://api.github.com/search/repositories"
url += "?q=language:python+sort:stars+stars:>10000"

headers = {"Accept": "application/vnd.github.v3+json"}
r = requests.get(url, headers=headers)
print(f"ステータスコード: {r.status_code}")

# レスポンスのオブジェクトを辞書に変換する
response_dict = r.json()

print(f"合計リポジトリ数: {response_dict['total_count']}")
print(f"完全な結果: {not response_dict['incomplete_results']}")

# リポジトリについての情報を調べる
repo_dicts = response_dict["items"]
print(f"情報が返されたリポジトリ数: {len(repo_dicts)}")

# 1つ目のリポジトリについて調べる
repo_dict = repo_dicts[0]

print("\n各リポジトリの情報の抜粋:")
for repo_dict in repo_dicts:
    print(f"\n名前: {repo_dict['name']}")
    print(f"所有者: {repo_dict['owner']['login']}")
    print(f"スター数: {repo_dict['stargazers_count']}")
    print(f"リポジトリ: {repo_dict['html_url']}")
    print(f"作成日時: {repo_dict['created_at']}")
    print(f"最終更新日時: {repo_dict['updated_at']}")
    print(f"説明: {repo_dict['description']}")
