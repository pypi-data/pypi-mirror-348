class Title:
    field: str
    title: str
    
    def __init__(self, title: str, field: str = "title") -> None:
        self.field = field
        self.title = title
        
    def to_dict(self) -> dict:
        return {
            "title": [ { "text": { "content": self.title } } ]
        }
