class MultiSelectOption:
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

class MultiSelect:
    field: str
    value: list[MultiSelectOption]
    
    def __init__(self, field: str, value: list[MultiSelectOption]) -> None:
        self.field = field
        self.value = value
        
    def to_dict(self) -> dict:
        return {
            "multi_select": [option.to_dict() for option in self.value]
        }