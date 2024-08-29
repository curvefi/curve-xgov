# @version 0.3.10
"""
@title Gnosis Broadcaster
@author CurveFi
@notice Using Arbitrary Message Bridge (AMB)
"""


interface ArbitraryMessageBridge:
    def requireToPassMessage(_contract: address, _data: Bytes[(MAX_BYTES + 160) * MAX_MESSAGES], _gas: uint256) -> bytes32: nonpayable
    def maxGasPerTx() -> uint256: view


event ApplyAdmins:
    admins: AdminSet

event CommitAdmins:
    future_admins: AdminSet

event SetBridge:
    bridge: ArbitraryMessageBridge


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


MAX_BYTES: constant(uint256) = 1024
MAX_MESSAGES: constant(uint256) = 8

admins: public(AdminSet)
future_admins: public(AdminSet)

agent: HashMap[address, Agent]

bridge: public(ArbitraryMessageBridge)


@external
def __init__(_admins: AdminSet, _bridge: ArbitraryMessageBridge):
    assert _admins.ownership != _admins.parameter  # a != b
    assert _admins.ownership != _admins.emergency  # a != c
    assert _admins.parameter != _admins.emergency  # b != c

    self.admins = _admins

    self.agent[_admins.ownership] = Agent.OWNERSHIP
    self.agent[_admins.parameter] = Agent.PARAMETER
    self.agent[_admins.emergency] = Agent.EMERGENCY

    self.bridge = _bridge

    log ApplyAdmins(_admins)
    log SetBridge(_bridge)


@external
def broadcast(_messages: DynArray[Message, MAX_MESSAGES], _gas_limit: uint256=0):
    """
    @notice Broadcast a sequence of messages.
    @param _messages The sequence of messages to broadcast.
    @param _gas_limit The L2 gas limit required to execute the sequence of messages.
    """
    agent: Agent = self.agent[msg.sender]
    assert agent != empty(Agent)

    bridge: ArbitraryMessageBridge = self.bridge
    gas_limit: uint256 = _gas_limit if _gas_limit > 0 else bridge.maxGasPerTx()

    bridge.requireToPassMessage(
        self,
        _abi_encode(  # relay(uint256,(address,bytes)[])
            agent,
            _messages,
            method_id=method_id("relay(uint256,(address,bytes)[])"),
        ),
        gas_limit,
    )


@external
def set_bridge(_bridge: ArbitraryMessageBridge):
    """
    @notice Set ArbitraryMessageBridge contract proxy.
    """
    assert msg.sender == self.admins.ownership

    self.bridge = _bridge
    log SetBridge(_bridge)


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
