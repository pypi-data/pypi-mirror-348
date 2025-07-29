from ringlink import RingLink


class TcpProxyContext(object):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


async def run(ringlink: RingLink, listen: str, target: str):
    pass
