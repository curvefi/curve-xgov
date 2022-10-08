# @version 0.3.7
"""
@title L1 Optimism Governance Proxy
"""


struct AdminSet:
    ownership: address
    parameter: address
    emergency: address


admins: public(AdminSet)
future_admins: public(AdminSet)


@external
def __init__(_admins: AdminSet):
    self.admins = _admins
