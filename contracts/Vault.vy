# @version 0.3.7
"""
@title Vault
@author CurveFi
"""


event CommitOwnership:
    future_owner: address

event ApplyOwnership:
    owner: address


MAX_BYTES: constant(uint256) = 512


owner: public(address)
future_owner: public(address)


@external
def __init__(_owner: address):
    self.owner = _owner

    log ApplyOwnership(_owner)


@payable
@external
def __default__():
    assert len(msg.data) == 0


@external
def execute(_target: address, _data: Bytes[MAX_BYTES], _value: uint256):
    assert msg.sender == self.owner

    raw_call(_target, _data, value=_value)


@external
def commit_future_owner(_future_owner: address):
    assert msg.sender == self.owner

    self.future_owner = _future_owner
    log CommitOwnership(_future_owner)


@external
def apply_future_owner():
    assert msg.sender == self.owner

    future_owner: address = self.future_owner
    self.owner = future_owner

    log ApplyOwnership(future_owner)
