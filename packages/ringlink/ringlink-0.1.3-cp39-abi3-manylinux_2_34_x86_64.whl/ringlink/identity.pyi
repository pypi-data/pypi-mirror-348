class Identity(object):
    def __init__(self, private_key: bytes, encryption_key: bytes):
        pass

    @staticmethod
    def generate() -> Identity:
        pass

    def private_key(self) -> bytes:
        pass

    def encryption_key(self) -> bytes:
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass
