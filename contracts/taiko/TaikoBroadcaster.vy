# pragma version 0.4.0
"""
@title CurveXGovTaikoBroadcaster
@author Curve.Fi
@license Copyright (c) Curve.Fi, 2020-2024 - all rights reserved
@custom:version 0.0.1
@notice Taiko governance message broadcaster
"""

version: public(constant(String[8])) = "0.0.1"

import contracts.Broadcaster as Broadcaster

initializes: Broadcaster


interface Bridge:
    def sendMessage(_message: Message) -> (bytes32, Message): payable


event SetDestinationData:
    chain_id: indexed(uint256)
    destination_data: DestinationData


struct Message:
    id: uint64  # Message ID whose value is automatically assigned.
    fee: uint64  # The max processing fee for the relayer. This fee has 3 parts:
                 # - the fee for message calldata.
                 # - the minimal fee reserve for general processing, excluding function call.
                 # - the invocation fee for the function call.
                 # Any unpaid fee will be refunded to the destOwner on the destination chain.
                 # Note that fee must be 0 if gasLimit is 0, or large enough to make the invocation fee
                 # non-zero.
    gasLimit: uint32  # gasLimit that the processMessage call must have.
    _from: address  # The address, EOA or contract, that interacts with this bridge.
                    # The value is automatically assigned.
    srcChainId: uint64  # Source chain ID whose value is automatically assigned.
    srcOwner: address  # The owner of the message on the source chain.
    destChainId: uint64  # Destination chain ID where the `to` address lives.
    destOwner: address  # The owner of the message on the destination chain.
    to: address  # The destination address on the destination chain.
    value: uint256  # value to invoke on the destination chain.
    data: Bytes[MAX_MESSAGE_RECEIVED]  # callData to invoke on the destination chain.


struct DestinationData:
    gas_price: uint256
    gas_limit: uint256
    dest_owner: address  # FeeCollector or Curve Vault
    relayer: address
    allow_manual_parameters: bool

struct ManualParameters:
    dest_owner: address


MAX_MESSAGE_RECEIVED: constant(uint256) = 9400

BRIDGE: public(constant(Bridge)) = Bridge(0xd60247c6848B7Ca29eDdF63AA924E53dB6Ddd8EC)

destination_data: public(HashMap[uint256, DestinationData])

manual_parameters: transient(ManualParameters)


@deploy
def __init__(_admins: Broadcaster.AdminSet):
    Broadcaster.__init__(_admins)

exports: Broadcaster.__interface__


@external
def __default__():
    pass


@internal
def _applied_destination_data(data: DestinationData) -> DestinationData:
    """
    @notice Apply manual parameters
    """
    if data.allow_manual_parameters:
        dest_owner: address = self.manual_parameters.dest_owner
        if dest_owner != empty(address):
            data.dest_owner = dest_owner

    return data


@payable
@external
def broadcast(_chain_id: uint256, _messages: DynArray[Broadcaster.agent_lib.Message, Broadcaster.agent_lib.MAX_MESSAGES], _destination_data: DestinationData=empty(DestinationData)):
    """
    @notice Broadcast a sequence of messages.
    @dev Save `depositCount` from POLYGON_ZKEVM_BRIDGE.BridgeEvent to claim message on destination chain
    @param _chain_id Chain ID of L2
    @param _messages The sequence of messages to broadcast.
    @param _destination_data Specific DestinationData (self.destination_data by default)
    """
    agent: Broadcaster.agent_lib.Agent = Broadcaster._broadcast_check(_chain_id, _messages)

    destination: DestinationData = _destination_data
    if destination.relayer == empty(address):
        destination = self.destination_data[_chain_id]
    assert destination.relayer != empty(address)

    data: DestinationData = self._applied_destination_data(destination)

    fee: uint256 = data.gas_price * data.gas_limit
    extcall BRIDGE.sendMessage(
        Message(
            id=0,  # Message ID whose value is automatically assigned.
            fee=convert(fee, uint64),
            gasLimit=convert(data.gas_limit, uint32),
            _from=empty(address),  # The value is automatically assigned.
            srcChainId=0,  # Source chain ID whose value is automatically assigned.
            srcOwner=msg.sender,
            destChainId=convert(_chain_id, uint64),
            destOwner=data.dest_owner,
            to=data.relayer,
            value=0,
            data=abi_encode(
                abi_encode(  # relay(uint256,(address,bytes)[])
                    agent,
                    _messages,
                ),
                method_id=method_id("onMessageInvocation(bytes)")
            ),  # callData to invoke on the destination chain.
        ),
        value=fee,
    )


@view
@external
def cost(_chain_id: uint256) -> uint256:
    """
    @notice Cost in ETH to bridge
    """
    data: DestinationData = self.destination_data[_chain_id]
    return data.gas_price * data.gas_limit


@external
def set_manual_parameters(_manual_parameters: ManualParameters):
    """
    @notice Set manual parameters that will be actual within current transaction
    """
    self.manual_parameters = _manual_parameters


@external
def set_destination_data(_chain_id: uint256, _destination_data: DestinationData):
    """
    @notice Set custom destination data. In order to turn off chain id set bridge=0xdead
    """
    assert msg.sender == Broadcaster.admins.ownership
    self.destination_data[_chain_id] = _destination_data
    log SetDestinationData(_chain_id, _destination_data)
