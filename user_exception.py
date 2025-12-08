# user_exception.py

class UserException(Exception):
    """Vlastní výjimka pro chyby související s uživatelem."""
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"Chyba: {self.args[0]}"
