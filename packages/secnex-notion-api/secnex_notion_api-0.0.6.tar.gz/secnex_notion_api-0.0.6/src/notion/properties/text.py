class Text:
    field: str
    value: str
    
    def __init__(self, field: str, value: str) -> None:
        self.field = field
        self.value = value

    def to_dict(self) -> dict:
        return {
            "title": [
                {
                    "text": {
                        "content": self.value
                    }
                }
            ]
        }