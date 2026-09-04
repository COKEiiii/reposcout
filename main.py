import os
import requests
from dotenv import load_dotenv


# 读取项目目录下 .env 文件中的环境变量
load_dotenv()

# 获取 GitHub 访问令牌
token = os.getenv("GITHUB_TOKEN")

# GitHub 搜索仓库的接口地址
url = "https://api.github.com/search/repositories"

# 请求头：告诉 GitHub 请求格式，并提供访问令牌
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
}

def search_github_repositories(query, api_sort="stars"):
    if api_sort not in ["stars", "forks", "updated"]:
        print(f"Invalid API sorting criteria '{api_sort}'. Defaulting to 'stars'.")
        api_sort = "stars"
    # 搜索条件：关键词和返回的仓库数量
    params = {
        "q": query,
        "per_page": 5,
        "sort": api_sort,
        "order": "desc"
    }

    # 发送 GET 请求，timeout 表示最多等待 10 秒
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10,
    )

    # 查看请求是否成功，200 表示成功
    print("Status code:", response.status_code)

    # 把 GitHub 返回的 JSON 数据转换成 Python 字典
    data = response.json()
    return data["items"]

def sort_repositories(repos, sort_by):
    if sort_by == "stars":
        # 按星标数量排序
        sorted_repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)
    elif sort_by == "forks":
        # 按分支数量排序
        sorted_repos = sorted(repos, key=lambda x: x["forks_count"], reverse=True)
    elif sort_by == "updated":
        # 按更新时间排序
        sorted_repos = sorted(repos, key=lambda x: x["updated_at"], reverse=True)
    else:
        # 如果输入的排序条件不在预设范围内，默认按星标数量排序
        sorted_repos = sorted(repos, key=lambda x: x["stargazers_count"], reverse=True)
        sort_by = "stars"
    print(f"Repositories sorted by {sort_by}:")
    return sorted_repos

def display_repositories(repos):
    # 遍历搜索结果中的每个仓库
    for repo in repos:
        print()
        print("Name:", repo["full_name"])
        print("Stars:", repo["stargazers_count"])
        print("Forks:", repo["forks_count"])
        print("Updated at:", repo["updated_at"])
        print("URL:", repo["html_url"])

query = input("Please enter a keyword to search for GitHub repositories: ")
sort_by = input("Please enter the sorting criteria (e.g., stars, forks, updated): ").strip().lower()
api_sort = input("Please enter the API sorting criteria (e.g., stars, forks, updated): ").strip().lower()
display_repositories(sort_repositories(search_github_repositories(query, api_sort), sort_by))