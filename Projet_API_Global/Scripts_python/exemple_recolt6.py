import requests

url = "https://api.github.com/user"

headers = {
    "Authorization": "token YOUR_GITHUB_TOKEN",
    "User-Agent": "Mon App Python"
}

response = requests.get(url, headers=headers)
print(response.json())