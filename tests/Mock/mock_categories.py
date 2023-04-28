class MockCategory:
    def __init__(self) -> None:
        self._id: int = 1
        self._name: str = "Material para pesca"
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    

    def payload_create_or_update_category(self, category = None): 
        payload: dict = {
            "name": category if category else self.name
        }

        print("Payload Category Create ", payload)
        return payload