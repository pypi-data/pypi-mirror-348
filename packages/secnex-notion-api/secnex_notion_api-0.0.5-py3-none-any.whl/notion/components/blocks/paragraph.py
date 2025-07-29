class Paragraph:
    type: str
    text: list[str]

    def __init__(self, text: list[str], link: str = None) -> None:
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
