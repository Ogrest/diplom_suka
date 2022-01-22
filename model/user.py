class User:
    def __init__(self,  phone_number: str, full_name: str, password: str, type: int) -> None:
        self.full_name = full_name
        self.phone_number = phone_number
        self.password = password
        self.type = type
