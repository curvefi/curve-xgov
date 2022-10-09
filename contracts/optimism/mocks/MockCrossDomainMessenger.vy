# @version 0.3.7
"""
@title Mock Optimism Cross Domain Messenger
"""


sender: address


@external
def _set_sender(_sender: address):
    self.sender = _sender


@view
@external
def xDomainMessageSender() -> address:
    return self.sender
