class User:
    def __init__(self, full_name: str, phone_number: str) -> None:
        self.id = 0 # auto increment
        self.full_name = full_name
        self.phone_number = phone_number