class Checkbox:
    field: str
    value: bool
    
    def __init__(self, field: str, value: bool) -> None:
        self.field = field
        self.value = value
        
    def to_dict(self) -> dict:
        return {
            "type": "checkbox",
            "checkbox": self.value
        }