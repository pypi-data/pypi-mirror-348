# SecNex Notion API Wrapper

This is a wrapper for the Notion API. You can use it to create, update, and delete pages, blocks, and more.

## Features

### Pages

- [x] Create a page
- [x] Search for pages
- [x] Get a page by id
- [ ] Update a page
- [ ] Delete a page

### Blocks

- [x] Create a block

## Installation

```bash
pip install secnex-notion-api
```

## Usage

```python
from secnex_notion_api.api.client import NotionApiClient
from secnex_notion_api.page import NotionPage
from secnex_notion_api.block import NotionParagraph

import os

client = NotionApiClient(token=os.getenv("NOTION_API_KEY"))

def main():
    pages = client.search(query="Site Name", filter={"value": "page", "property": "object"})
    print(pages)

    page_id = pages["results"][0]["id"]
    print(page_id)
    page = client.get_page_by_id(page_id)
    print(page)

    paragraph = NotionParagraph(parent_type="page", text=["Hello, world!"])
    page = NotionPage(parent={"page_id": page_id}, title="Hello, world!", blocks=[paragraph], properties=pages["results"][0]["properties"])
    print(page)
    print(client.new(page))

if __name__ == "__main__":
    main()
```
