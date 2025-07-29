import requests

from notion.page import NotionPage

class NotionApiClient:
    def __init__(self, token: str) -> None:
        self.token = token

    def new(self, page: NotionPage) -> None:
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        print(page.to_dict())
        response = requests.post(url, headers=headers, json=page.to_dict())
        return response.json()
    
    def get_page_by_id(self, page_id: str) -> dict:
        url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        response = requests.get(url, headers=headers)
        return response.json()
    
    def search(self, query: str, filter: dict = None) -> dict:
        url = "https://api.notion.com/v1/search"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        data = {
            "query": query,
        }
        if filter:
            data["filter"] = filter
        print(data)
        response = requests.post(url, headers=headers, json=data)
        return response.json()