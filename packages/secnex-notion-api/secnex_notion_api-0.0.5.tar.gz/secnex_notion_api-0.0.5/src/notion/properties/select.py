class SelectOption:
    name: str
    color: str
    
    def __init__(self, name: str, color: str = None) -> None:
        self.name = name
        self.color = color
        
    def to_dict(self) -> dict:
        data = {
            "name": self.name
        }
        if self.color:
            data["color"] = self.color
        return data

class Select:
    field: str
    value: SelectOption
    
    def __init__(self, field: str, value: SelectOption) -> None:
        self.field = field
        self.value = value
        
    def to_dict(self) -> dict:
        return {
            "select": self.value.to_dict()
        }