# pragma version 0.4.0
"""
@title Broadcaster
@author Curve.Fi
@license Copyright (c) Curve.Fi, 2020-2024 - all rights reserved
@custom:version 0.0.1
@notice Governance message broadcaster
"""

import Agent as agent_lib


event Broadcast:
    chain_id: indexed(uint256)
    agent: indexed(agent_lib.Agent)
    messages: DynArray[agent_lib.Message, agent_lib.MAX_MESSAGES]


event ApplyAdmins:
    admins: AdminSet

event CommitAdmins:
    future_admins: AdminSet


struct AdminSet:
    ownership: address
    parameter: address
    emergency: address


admins: public(AdminSet)
future_admins: public(AdminSet)

agent: public(HashMap[address, agent_lib.Agent])



@deploy
def __init__(_admins: AdminSet):
    assert _admins.ownership != _admins.parameter  # a != b
    assert _admins.ownership != _admins.emergency  # a != c
    assert _admins.parameter != _admins.emergency  # b != c

    self.admins = _admins

    self.agent[_admins.ownership] = agent_lib.Agent.OWNERSHIP
    self.agent[_admins.parameter] = agent_lib.Agent.PARAMETER
    self.agent[_admins.emergency] = agent_lib.Agent.EMERGENCY

    log ApplyAdmins(_admins)


@internal
def _broadcast_check(chain_id: uint256, messages: DynArray[agent_lib.Message, agent_lib.MAX_MESSAGES]) -> agent_lib.Agent:
    """
    @notice Broadcast a sequence of messages.
    @param _chain_id Chain ID of L2
    @param _messages The sequence of messages to broadcast.
    """
    agent: agent_lib.Agent = self.agent[msg.sender]
    assert agent != empty(agent_lib.Agent)
    log Broadcast(chain_id, agent, messages)

    return agent


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
    self.agent[admins.ownership] = empty(agent_lib.Agent)
    self.agent[admins.parameter] = empty(agent_lib.Agent)
    self.agent[admins.emergency] = empty(agent_lib.Agent)

    # set new admins
    future_admins: AdminSet = self.future_admins
    self.agent[future_admins.ownership] = agent_lib.Agent.OWNERSHIP
    self.agent[future_admins.parameter] = agent_lib.Agent.PARAMETER
    self.agent[future_admins.emergency] = agent_lib.Agent.EMERGENCY

    self.admins = future_admins
    log ApplyAdmins(future_admins)
