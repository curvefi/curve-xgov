# @version 0.3.7
"""
@title L1 Optimism Governance Proxy
"""


event CommitAdmins:
    future_admins: AdminSet

event ApplyAdmins:
    admins: AdminSet


struct AdminSet:
    ownership: address
    parameter: address
    emergency: address


admins: public(AdminSet)
future_admins: public(AdminSet)


@external
def __init__(_admins: AdminSet):
    self.admins = _admins

    log ApplyAdmins(_admins)


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
