class MockUser:
    def __init__(self) -> None:
        """
        MOCK USERS
        """
        self._id: int = 1
        self._name: str = "SuperUser"
        self._name_updated: str = "SuperUser"
        self._email: str = "admin@gmail.com"
        self._password: str = "admin@2023"
        
        """
        MOCK HEADER - AUTH
        """
        self._token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjo0NTg0OTc5NjM1LCJpYXQiOjE2ODE5Mzk2MzUsInN1YiI6IjEifQ.-eT-foaFaLkTFpBhTz9l-FRoDJYLKu56kszOMKXz8rk"

    """
    GETTERS HEADERS
    """
    
    @property
    def header(self):
        try:
            header: dict = {
                "Authorization": "Bearer " + self.token,
                "Content-type": "application/json"
            }
            print("Header Getters ", header)
            return header 
        except TypeError as e:
            print("TypeError: Token não setado: ", e)
    
    @property
    def header_login(self):
        header: dict = {
            "Content-Disposition": "form-data",
        }
        print("Header Login Getters ", header)
        return header 

    """
    SETTERS AND GETTERS USERS
    """

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
    def name_updated(self):
        return self._name_updated
    
    @name_updated.setter
    def name_updated(self, name_updated):
        self._name_updated = name_updated
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = email
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        self._password = password

    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, token):
        self._token = token

    
    """
    PAYLOADS USER
    """
    
    def mock_user(self) -> dict:
        user: dict = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
        print("User Mock ", user)
        return user
    
    def payload_create_user(self) -> dict:
        payload: dict = {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
        print("Payload create user ", payload)
        return payload
    
    def payload_update_user(self, name) -> dict:
        self.name = name
        payload: dict = {
            "name": self.name
        }
        print("Payload update user ", payload)
        return payload
    
    def payload_login_with_wrong_password(self, password):
        payload: dict = {
            "username": self.email,
            "password": password
        }
        print("Payload login com erro de senha ", payload)
        return payload
    
    def payload_login(self):
        payload: dict = {
            "username": self.email,
            "password": self.password
        }
        print("Payload login ", payload)
        return payload
    
   