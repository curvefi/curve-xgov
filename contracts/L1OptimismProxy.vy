# @version 0.3.7
"""
@title L1 Optimism Governance Proxy
"""


interface CrossDomainMessenger:
    def sendMessage(_target: address, _message: Bytes[MAXSIZE], _gas_limit: uint32): nonpayable


event CommitAdmins:
    future_admins: AdminSet

event ApplyAdmins:
    admins: AdminSet

event SetMessenger:
    messenger: CrossDomainMessenger


struct AdminSet:
    ownership: address
    parameter: address
    emergency: address


MAXSIZE: constant(uint256) = 2**16 - 1


admins: public(AdminSet)
future_admins: public(AdminSet)

messenger: public(CrossDomainMessenger)


@external
def __init__(_admins: AdminSet, _messenger: CrossDomainMessenger):
    self.admins = _admins
    self.messenger = _messenger

    log ApplyAdmins(_admins)
    log SetMessenger(_messenger)


@external
def set_messenger(_messenger: CrossDomainMessenger):
    assert msg.sender in [self.admins.ownership, self.admins.emergency]

    self.messenger = _messenger
    log SetMessenger(_messenger)


@external
def commit_admins(_admins: AdminSet):
    assert msg.sender == self.admins.ownership

    self.future_admins = _admins
    log CommitAdmins(_admins)


@external
def apply_admins():
    assert msg.sender == self.admins.ownership

    future_admins: AdminSet = self.future_admins
    self.admins = future_admins
    log ApplyAdmins(future_admins)
