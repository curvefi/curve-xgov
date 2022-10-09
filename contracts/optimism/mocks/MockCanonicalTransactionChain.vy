# @version 0.3.7
"""
@title Mock Optimism Canonical Transaction Chain
"""


prepaid: address


@external
def _set_prepaid(_prepaid: uint32):
    self.prepaid = _prepaid


@view
@external
def enqueueL2GasPrepaid() -> uint32:
    return self.prepaid
