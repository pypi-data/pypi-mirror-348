# SecNex Notion API Wrapper

This is a wrapper for the Notion API. You can use it to create, update, and delete pages, blocks, and more.

## Features

### Blocks

- [x] Paragraph
- [x] Callout
- [x] Headings
- [x] Code
- [ ] Image
- [ ] Video
- [ ] File
- [ ] To-do
- [ ] Toggle
- [ ] Table
- [ ] Divider

### Properties

- [x] Property
- [x] Checkbox
- [x] Multi-select
- [x] Select
- [x] Text
- [x] Title
- [x] Description

### Pages

## Installation

```bash
pip install secnex-notion-api
```

## Usage

```python
from notion import Client, Components, Properties

import os

def main():
    client = Client(token=os.getenv("NOTION_API_KEY"))

    template_page = client.search(query="Tickets", filter={"property": "object", "value": "database"})

    page = Components.Page(
        parent=template_page["results"][0],
        parent_type="database",
        icon="👋",
        properties=[
            Properties.Property(field="Name", value="Test"),
            Properties.Checkbox(field="Checkbox", value=True),
            Properties.MultiSelect(field="Multi-select", value=[
                Properties.MultiSelectOption(name="Test"),
                Properties.MultiSelectOption(name="Test One", color="blue")
            ]),
            Properties.Select(field="Priority", value=Properties.SelectOption(name="Wow", color="blue"))
        ],
        blocks=[
            Components.Paragraph(text=["Hello, world!"]),
            Components.Callout(text="Hello, world!", icon="👋", color="default")
        ]
    )

    print(client.new(page))

if __name__ == "__main__":
    main()
```
