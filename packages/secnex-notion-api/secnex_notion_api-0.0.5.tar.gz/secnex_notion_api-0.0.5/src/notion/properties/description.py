class Description:
    field: str
    description: str
    
    def __init__(self, description: str, field: str = "description") -> None:
        self.field = field
        self.description = description
        
    def to_dict(self) -> dict:
        return {
            "description": [{"text": {"content": self.description}}]
        }
