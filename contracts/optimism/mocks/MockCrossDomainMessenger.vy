# @version 0.3.7
"""
@title Mock Optimism Cross Domain Messenger
"""


sender: address
count: public(uint256)

data: public(Bytes[1024])


@external
def _set_sender(_sender: address):
    self.sender = _sender


@view
@external
def xDomainMessageSender() -> address:
    return self.sender


@external
def sendMessage(_target: address, _data: Bytes[1024], _gas_limit: uint32):
    self.data = _data
    self.count += 1
