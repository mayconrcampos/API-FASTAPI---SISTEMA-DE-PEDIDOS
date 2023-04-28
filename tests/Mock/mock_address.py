class MockAddress:
    def __init__(self) -> None:
        self._id: int = 1
        self._user_id: int = 1
        self._description: str = "Terra da baleia Franca"
        self._postal_code: str = "88780-000"
        self._street: str = "Av Renato Ramos da Silva"
        self._complement: str = "Nº 3013 - AP05"
        self._neighborhood: str = "Vila Nova"
        self._city: str = "Imbituba"
        self._state: str = "SC"
    
    """
    GETTERS AND SETTERS - ADDRESS
    """
    
    @property
    def id(self):
        print("Getter Address id ", self._id)
        return self._id
    
    @id.setter
    def id(self, id):
        print("Setter id ", id)
        self._id = id
    
    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        self._description = description
    
    @property
    def postal_code(self):
        return self._postal_code
    
    @postal_code.setter
    def postal_code(self, postal_code):
        self._postal_code = postal_code
    
    @property
    def street(self):
        return self._street
    
    @street.setter
    def street(self, street):
        self._street = street
    
    @property
    def complement(self):
        return self._complement
    
    @complement.setter
    def complement(self, complement):
        self._complement = complement
    
    @property
    def neighborhood(self):
        return self._neighborhood
    
    @neighborhood.setter
    def neighborhood(self, neighborhood):
        self._neighborhood = neighborhood

    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self, city):
        self._city = city
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        self._state = state

    """
    PAYLOADS ADDRESS
    """
    def payload_create_address(self, id):
        payload: dict = {
            "user_id": id,
            "description": self.description,
            "postal_code": self.postal_code,
            "street": self.street,
            "complement": self.complement,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "state": self.state
        }
        print(payload)
        return payload
    
    def payload_create_address_wrong_CEP(self, id,  cep):
        payload: dict = {
            "user_id": id,
            "description": self.description,
            "postal_code": cep,
            "street": self.street,
            "complement": self.complement,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "state": self.state
        }
        print(payload)
        return payload
    
    def payload_update_address(
            self, 
            description: str = None, 
            postal_code: str = None,
            street: str = None, 
            complement: str = None,
            neighborhood: str = None):
        self.description = description
        self.postal_code = postal_code
        self.street = street
        self.complement = complement
        self.neighborhood = neighborhood

        payload: dict = {
            "description": description if description else self.description,
            "postal_code": postal_code if postal_code else self.postal_code,
            "street": street if street else self.street,
            "complement": complement if complement else self.complement,
            "neighborhood": neighborhood if neighborhood else self.neighborhood
        }
        print("Payload Update Address ", payload, self.id)
        return payload

