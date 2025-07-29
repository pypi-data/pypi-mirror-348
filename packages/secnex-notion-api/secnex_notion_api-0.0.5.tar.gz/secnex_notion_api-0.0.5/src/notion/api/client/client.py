import requests

from ...components.page import Page
from .endpoints import NOTION_SEARCH, NOTION_PAGE

class Client:
    def __init__(self, token: str) -> None:
        self.token = token

    def new(self, page: Page) -> dict:
        url = NOTION_PAGE
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        print(page.to_dict())
        response = requests.post(url, headers=headers, json=page.to_dict())
        return response.json()
    
    def get_page_by_id(self, page_id: str) -> dict:
        url = f"{NOTION_PAGE}/{page_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        response = requests.get(url, headers=headers)
        return response.json()
    
    def search(self, query: str, filter: dict = None) -> dict:
        url = NOTION_SEARCH
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
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
    def search_pages(self, query: str) -> dict:
        url = NOTION_SEARCH
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        data = {
            "query": query,
            "filter": {
                "property": "object",
                "value": "page"
            }
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
    def search_databases(self, query: str) -> dict:
        url = NOTION_SEARCH
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        data = {
            "query": query,
            "filter": {
                "property": "object",
                "value": "database"
            }
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()