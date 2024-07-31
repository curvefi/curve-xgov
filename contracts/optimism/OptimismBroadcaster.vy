# pragma version 0.3.10
"""
@title Optimism Broadcaster
@author CurveFi
@license MIT
@custom:version 1.0.1
"""


version: public(constant(String[8])) = "1.0.1"


interface OVMChain:
    def enqueueL2GasPrepaid() -> uint32: view


event Broadcast:
    chain_id: indexed(uint256)
    agent: indexed(Agent)
    messages: DynArray[Message, MAX_MESSAGES]

event SetDestinationData:
    chain_id: indexed(uint256)
    data: DestinationData

event ApplyAdmins:
    admins: AdminSet

event CommitAdmins:
    future_admins: AdminSet


enum Agent:
    OWNERSHIP
    PARAMETER
    EMERGENCY


struct AdminSet:
    ownership: address
    parameter: address
    emergency: address

struct Message:
    target: address
    data: Bytes[MAX_BYTES]


struct DestinationData:
    ovm_chain: OVMChain  # CanonicalTransactionChain
    ovm_messenger: address  # CrossDomainMessenger
    relayer: address


MAX_BYTES: constant(uint256) = 1024
MAX_MESSAGES: constant(uint256) = 8


admins: public(AdminSet)
future_admins: public(AdminSet)

destination_data: public(HashMap[uint256, DestinationData])
agent: HashMap[address, Agent]


@external
def __init__(_admins: AdminSet):
    assert _admins.ownership != _admins.parameter  # a != b
    assert _admins.ownership != _admins.emergency  # a != c
    assert _admins.parameter != _admins.emergency  # b != c

    self.admins = _admins

    self.agent[_admins.ownership] = Agent.OWNERSHIP
    self.agent[_admins.parameter] = Agent.PARAMETER
    self.agent[_admins.emergency] = Agent.EMERGENCY

    log ApplyAdmins(_admins)


@external
def broadcast(_chain_id: uint256, _messages: DynArray[Message, MAX_MESSAGES], _gas_limit: uint32 = 0, _destination_data: DestinationData=empty(DestinationData)):
    """
    @notice Broadcast a sequence of messages.
    @param _chain_id Chain ID of L2
    @param _messages The sequence of messages to broadcast.
    @param _gas_limit The L2 gas limit required to execute the sequence of messages.
    @param _destination_data Specific DestinationData (self.destination_data by default)
    """
    agent: Agent = self.agent[msg.sender]
    assert agent != empty(Agent)
    destination: DestinationData = _destination_data
    if destination.relayer == empty(address):
        destination = self.destination_data[_chain_id]
    assert destination.relayer != empty(address)

    # https://community.optimism.io/docs/developers/bridge/messaging/#for-l1-%E2%87%92-l2-transactions
    gas_limit: uint32 = _gas_limit
    if gas_limit == 0:
        gas_limit = destination.ovm_chain.enqueueL2GasPrepaid()

    raw_call(
        destination.ovm_messenger,
        _abi_encode(  # sendMessage(address,bytes,uint32)
            destination.relayer,
            _abi_encode(  # relay(uint256,(address,bytes)[])
                agent,
                _messages,
                method_id=method_id("relay(uint256,(address,bytes)[])"),
            ),
            gas_limit,
            method_id=method_id("sendMessage(address,bytes,uint32)"),
        ),
    )


@external
def set_destination_data(_chain_id: uint256, _destination_data: DestinationData):
    """
    @notice Set destination data for child chain.
    """
    assert msg.sender == self.admins.ownership
    self.destination_data[_chain_id] = _destination_data
    log SetDestinationData(_chain_id, _destination_data)


@external
def commit_admins(_future_admins: AdminSet):
    """
    @notice Commit an admin set to use in the future.
    """
    assert msg.sender == self.admins.ownership

    assert _future_admins.ownership != _future_admins.parameter  # a != b
    assert _future_admins.ownership != _future_admins.emergency  # a != c
    assert _future_admins.parameter != _future_admins.emergency  # b != c

    self.future_admins = _future_admins
    log CommitAdmins(_future_admins)


@external
def apply_admins():
    """
    @notice Apply the future admin set.
    """
    admins: AdminSet = self.admins
    assert msg.sender == admins.ownership

    # reset old admins
    self.agent[admins.ownership] = empty(Agent)
    self.agent[admins.parameter] = empty(Agent)
    self.agent[admins.emergency] = empty(Agent)

    # set new admins
    future_admins: AdminSet = self.future_admins
    self.agent[future_admins.ownership] = Agent.OWNERSHIP
    self.agent[future_admins.parameter] = Agent.PARAMETER
    self.agent[future_admins.emergency] = Agent.EMERGENCY

    self.admins = future_admins
    log ApplyAdmins(future_admins)
