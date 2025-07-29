class Code:
    def __init__(self, language: str, code: list[str], caption: str = None) -> None:
        self.language = language
        self.code = code
        self.caption = caption
        
    def to_dict(self) -> dict:
        blocks = []
        for text in self.code:
            blocks.append({
                "type": "text",
                "text": {
                    "content": text
                }
            })

        data = {
            "object": "block",
            "type": "code",
            "code": {
                "caption": [],
                "rich_text": blocks,
                "language": self.language
            }
        }
        if self.caption:
            data["code"]["caption"] = [
                {
                    "type": "text",
                    "text": {
                        "content": self.caption
                    }
                }
            ]
        return data
