# @version 0.3.7
"""
@title L1 Optimism Governance Proxy
"""


interface CrossDomainMessenger:
    def sendMessage(_target: address, _message: Bytes[MAXSIZE], _gas_limit: uint32): nonpayable

interface CanonicalTransactionChain:
    def enqueueL2GasPrepaid() -> uint32: view


event CommitAdmins:
    future_admins: AdminSet

event ApplyAdmins:
    admins: AdminSet

event SetMessenger:
    messenger: CrossDomainMessenger

event SetTransactionChain:
    transaction_chain: CanonicalTransactionChain


struct AdminSet:
    ownership: address
    parameter: address
    emergency: address


MAXSIZE: constant(uint256) = 2**16 - 1


admins: public(AdminSet)
future_admins: public(AdminSet)

messenger: public(CrossDomainMessenger)
transaction_chain: public(CanonicalTransactionChain)


@external
def __init__(_admins: AdminSet, _messenger: CrossDomainMessenger, _transaction_chain: CanonicalTransactionChain):
    self.admins = _admins
    self.messenger = _messenger
    self.transaction_chain = _transaction_chain

    log ApplyAdmins(_admins)
    log SetMessenger(_messenger)
    log SetTransactionChain(_transaction_chain)


@external
def set_messenger(_messenger: CrossDomainMessenger):
    assert msg.sender in [self.admins.ownership, self.admins.emergency]

    self.messenger = _messenger
    log SetMessenger(_messenger)


@external
def set_transaction_chain(_transaction_chain: CanonicalTransactionChain):
    assert msg.sender in [self.admins.ownership, self.admins.emergency]

    self.transaction_chain = _transaction_chain
    log SetTransactionChain(_transaction_chain)


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
