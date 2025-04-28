# @version 0.3.10
"""
@title XYZ Broadcaster
@author CurveFi
@license MIT
@custom:version 0.0.2
@custom:security security@curve.fi
"""

version: public(constant(String[8])) = "0.0.2"

event Broadcast:
    agent: indexed(Agent)
    chain_id: indexed(uint256)
    nonce: uint256
    digest: bytes32
    deadline: uint256

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


MAX_BYTES: constant(uint256) = 1024
MAX_MESSAGES: constant(uint256) = 8

DAY: constant(uint256) = 86400
WEEK: constant(uint256) = 7 * DAY

admins: public(AdminSet)
future_admins: public(AdminSet)

agent: HashMap[address, Agent]

nonce: public(HashMap[Agent, HashMap[uint256, uint256]])  # agent -> chainId -> nonce
digest: public(HashMap[Agent, HashMap[uint256, HashMap[uint256, bytes32]]])  # agent -> chainId -> nonce -> messageDigest
deadline: public(HashMap[Agent, HashMap[uint256, HashMap[uint256, uint256]]])  # agent -> chainId -> nonce -> deadline


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


@internal
@pure
def _get_ttl(agent: Agent, ttl: uint256) -> uint256:
    if agent == Agent.EMERGENCY:
        # Emergency votes should be brisk
        if ttl == 0:
            ttl = DAY  # default
        assert ttl <= WEEK
    else:
        if ttl == 0:
            ttl = WEEK  # default
        assert DAY <= ttl and ttl <= 3 * WEEK
    return ttl


@external
def broadcast(_chain_id: uint256, _messages: DynArray[Message, MAX_MESSAGES], _ttl: uint256=0):
    """
    @notice Broadcast a sequence of messages.
    @param _chain_id The chain id to have messages executed on.
    @param _messages The sequence of messages to broadcast.
    @param _ttl Time-to-leave for message if it's not executed. 0 will use default values.
    """
    agent: Agent = self.agent[msg.sender]
    assert agent != empty(Agent) and len(_messages) > 0
    ttl: uint256 = self._get_ttl(agent, _ttl)

    digest: bytes32 = keccak256(_abi_encode(_messages))
    nonce: uint256 = self.nonce[agent][_chain_id]

    self.digest[agent][_chain_id][nonce] = digest
    self.nonce[agent][_chain_id] = nonce + 1
    self.deadline[agent][_chain_id][nonce] = block.timestamp + ttl

    log Broadcast(agent, _chain_id, nonce, digest, block.timestamp + ttl)


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
