class NotionPage:
    def __init__(self, parent: dict, title: str, blocks: list[any], properties: dict = None) -> None:
        self.object = "page"
        self.parent = parent
        self.title = title
        self.blocks = blocks
        self.properties = properties

    def to_dict(self) -> dict:
        data = {
            "parent": self.parent,
            "children": [block.to_dict() for block in self.blocks],
            "properties": self.properties
        }
        if self.title:
            data["properties"] = {
                "title": {
                    "title": [
                        {
                            "text": {"content": self.title}
                        }
                    ]
                }
            }
        return data