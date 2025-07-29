from ringlink import RingLink

from ringlink.identity import Identity


class Builder:
    def __init__(self, identity: Identity, network: str):
        pass

    def set_token(self, token: str):
        pass

    async def build(self) -> RingLink:
        pass
