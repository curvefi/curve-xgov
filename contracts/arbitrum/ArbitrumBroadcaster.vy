# @version 0.3.7
"""
@title Arbitrum Broadcaster
@author CurveFi
"""


event ApplyAdmins:
    admins: AdminSet

event CommitAdmins:
    future_admins: AdminSet

event SetArbInbox:
    arb_inbox: address


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

arb_inbox: public(address)


@external
def __init__(_admins: AdminSet, _arb_inbox: address):
    assert _admins.ownership != _admins.parameter  # a != b
    assert _admins.ownership != _admins.emergency  # a != c
    assert _admins.parameter != _admins.emergency  # b != c

    self.admins = _admins

    self.agent[_admins.ownership] = Agent.OWNERSHIP
    self.agent[_admins.parameter] = Agent.PARAMETER
    self.agent[_admins.emergency] = Agent.EMERGENCY

    self.arb_inbox = _arb_inbox

    log ApplyAdmins(_admins)
    log SetArbInbox(_arb_inbox)


@external
def broadcast(_messages: DynArray[Message, MAX_MESSAGES]):
    """
    @notice Broadcast a sequence of messeages.
    @param _messages The sequence of messages to broadcast.
    """
    agent: Agent = self.agent[msg.sender]
    assert agent != empty(Agent)


@external
def set_arb_inbox(_arb_inbox: address):
    assert msg.sender == self.admins.ownership

    self.arb_inbox = _arb_inbox
    log SetArbInbox(_arb_inbox)


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
