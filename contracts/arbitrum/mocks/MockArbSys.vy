# @version 0.3.7


wasMyCallersAddressAliased: public(bool)
myCallersAddressWithoutAliasing: public(address)


@external
def _set_l1_caller(_caller: address):
    self.wasMyCallersAddressAliased = convert(_caller, uint256) != 0
    self.myCallersAddressWithoutAliasing = _caller
