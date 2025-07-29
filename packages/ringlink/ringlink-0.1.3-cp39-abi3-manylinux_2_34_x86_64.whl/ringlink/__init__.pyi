from .proxy.tcp import TcpProxyContext


async def auto(network_id: str, token: str) -> RingLink:
    pass


class NetId(object):
    def __init__(self, network_id: str):
        pass


class RingLink(object):
    def tcp_proxy(self, listen: str, target: str) -> TcpProxyContext:
        pass
