class Page:
    def __init__(self, parent: dict, blocks: list[any], properties: list[dict] = None, parent_type: str = "page", icon: str = None) -> None:
        self.object = "page"
        self.parent = parent
        self.parent_type = parent_type
        self.blocks = blocks
        self.properties = properties or {}
        self.icon = icon
    def to_dict(self) -> dict:
        data = {
            "parent": {
                f"{self.parent_type}_id": self.parent["id"]
            },
            "children": [block.to_dict() for block in self.blocks],
            "properties": self.parent["properties"]
        }
        __properties = {}
        for property in self.properties:
            __properties[property.field] = property.to_dict()
        data["properties"] = __properties
        if self.icon:
            data["icon"] = {
                "emoji": self.icon
            }
        return data