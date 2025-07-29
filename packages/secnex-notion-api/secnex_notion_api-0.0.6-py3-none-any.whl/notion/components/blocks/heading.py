class Heading:
    parent_type: str
    level: int
    type: str
    text: list[str]

    def __init__(self, level: int, text: list[str]) -> None:
        self.level = level
        self.type = f"heading_{level}"
        self.text = text

    def to_dict(self) -> dict:
        return {
            "object": "block",
            "type": self.type,
            self.type: {
                "rich_text": [{"type": "text", "text": {"content": self.text}}]
            }
        }