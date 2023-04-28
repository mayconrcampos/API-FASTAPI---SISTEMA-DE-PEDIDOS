class MockOrderItem:
    def __init__(self) -> None:
        """ 
        ORDER
        """
        self._id: int = 1
        self._user_id: int = 1
        self._status: str = "Pendente"

        """ 
        ORDER ITEM
        """
        self._quantity: int = 10

    """ 
    ORDER
    """

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        self._status = status

    """ 
    Order Item
    """
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity
    

    def payload_insert_or_update_order(self, user_id: int = None, status: str = None):
        payload: dict = {
            "user_id": user_id if user_id else self.user_id,
            "status": status if status else self.status
        }
        print("Payload Order Create ", payload)
        return payload
    
    def payload_insert_or_update_order_item_quantity(self, quantity: int = None):
        payload: dict = {
            "quantity": quantity if quantity else self.quantity
        }
        print("Payload insert order item ", payload)
        return payload
    
    def payload_update_status(self, status: str = "Pendente"):
        payload: dict = {
            "status": status
        }
        print("Payload Update Status ", payload)
        return payload
