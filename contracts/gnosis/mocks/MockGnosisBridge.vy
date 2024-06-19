# pragma version 0.3.10


MAX_LEN: constant(uint256) = 1024

contract: public(address)
data: public(Bytes[MAX_LEN])
gas: public(uint256)


@view
@external
def maxGasPerTx() -> uint256:
    return 4_000_000


@external
def requireToPassMessage(_contract: address, _data: Bytes[MAX_LEN], _gas: uint256) -> bytes32:
    assert _gas >= 100
    assert _gas <= 4_000_000

    self.contract = _contract
    self.data = _data
    self.gas = _gas
    return convert(101, bytes32)
