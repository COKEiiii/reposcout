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

def search_github_repositories(query):
    # 搜索条件：关键词和返回的仓库数量
    params = {
        "q": query,
        "per_page": 5,
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

    return data

def display_repositories(repos):
    # 遍历搜索结果中的每个仓库
    for repo in repos["items"]:
        print()
        print("Name:", repo["full_name"])
        print("Stars:", repo["stargazers_count"])
        print("URL:", repo["html_url"])
query = input("Please enter a keyword to search for GitHub repositories: ")

repos = search_github_repositories(query)
display_repositories(repos)