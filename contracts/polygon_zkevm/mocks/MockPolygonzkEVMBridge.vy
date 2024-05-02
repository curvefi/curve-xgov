# @version 0.3.10


origin_address: public(address)
destination_address: public(address)
origin_network: public(uint32)
metadata: public(Bytes[9000])

force_updated: public(bool)

count: public(uint256)


@external
def _set_origin_network(_origin_network: uint32):
    self.origin_network = _origin_network

@external
def _set_origin_address(_origin_address: address):
    self.origin_address = _origin_address

@external
def _set_destination_address(_destination_address: address):
    self.destination_address = _destination_address


@payable
@external
def bridgeMessage(_destination_network: uint32, _destination_address: address, _force_update: bool, _metadata: Bytes[9000]):
    assert _destination_network == 3, "DestinationNetworkInvalid"

    self.origin_address = msg.sender
    self.destination_address = _destination_address
    self.metadata = _metadata

    self.force_updated = _force_update

    self.count += 1


@payable
@external
def claimMessage():
    raw_call(
        self.destination_address,
        _abi_encode(
            self.origin_address, self.origin_network, self.metadata,
            method_id=method_id("onMessageReceived(address,uint32,bytes)"),
        ),
        value=msg.value,
        revert_on_failure=True,
    )
