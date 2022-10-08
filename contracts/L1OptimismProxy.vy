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


enum AdminType:
    OWNERSHIP
    PARAMETER
    EMERGENCY


struct AdminSet:
    ownership: address
    parameter: address
    emergency: address


MAXSIZE: constant(uint256) = 2**16 - 1
MAXSIZE_MESSAGE: constant(uint256) = 2**15 - 1


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
def send_message(_target: address, _message: Bytes[MAXSIZE_MESSAGE], _gas_limit: uint32 = 0):

    # NOTE: match statement would be nice
    admin_type: AdminType = empty(AdminType)
    if msg.sender == self.admins.ownership:
        admin_type = AdminType.OWNERSHIP
    elif msg.sender == self.admins.parameter:
        admin_type = AdminType.PARAMETER
    elif msg.sender == self.admins.emergency:
        admin_type = AdminType.EMERGENCY
    else:
        raise "Not allowed."

    # https://community.optimism.io/docs/developers/bridge/messaging/#for-l1-%E2%87%92-l2-transactions
    gas_limit: uint32 = _gas_limit
    if gas_limit == 0:
        gas_limit = self.transaction_chain.enqueueL2GasPrepaid()

    # receive_message(_admin_type: AdminType, _target: address, _message: Bytes[MAXSIZE]): nonpayable
    self.messenger.sendMessage(
        self,
        _abi_encode(
            admin_type,
            _target,
            _message,
            method_id=method_id("receive_message(uint256,address,bytes)")
        ),
        gas_limit
    )


@external
def set_messenger(_messenger: CrossDomainMessenger):
    assert msg.sender == self.admins.ownership

    self.messenger = _messenger
    log SetMessenger(_messenger)


@external
def set_transaction_chain(_transaction_chain: CanonicalTransactionChain):
    assert msg.sender == self.admins.ownership

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
