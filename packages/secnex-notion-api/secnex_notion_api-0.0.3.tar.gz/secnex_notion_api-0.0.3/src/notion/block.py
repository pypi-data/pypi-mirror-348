class NotionParagraph:
    parent_type: str
    type: str
    text: list[str]

    def __init__(self, parent_type: str, text: list[str], link: str = None) -> None:
        self.parent_type = parent_type
        self.type = "paragraph"
        self.text = text
        self.link = link

    def to_dict(self) -> dict:
        blocks = []
        for text in self.text:
            i = {
                "type": "text",
                "text": {
                    "content": text,
                }
            }
            if self.link:
                i["text"]["link"] = {
                    "url": self.link
                }
            blocks.append(i)

        print(blocks)

        return {
            "object": "block",
            "type": self.type,
            self.type: {
                "rich_text": blocks
            }
        }
