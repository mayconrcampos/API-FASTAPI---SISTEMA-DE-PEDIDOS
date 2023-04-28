class MockProduct:
    def __init__(self) -> None:
        self._id: int = 1
        self._name: str = "Vara Marine Sports - 3m 40lbs"
        self._description: str = "Vara para pesca de praia ou costão"
        self._price: float = 690.00
    
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

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        self._description = description
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        self._price = price
    

    def payload_create_or_update_product(self, name: str = None, description: str = None, price: float = None): 
        payload: dict = {
            "name": name if name else self.name,
            "description": description if description else self.description,
            "price": price if price else self.price
        }

        print("Payload Product Create ", payload)
        return payload
    