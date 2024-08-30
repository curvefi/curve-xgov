import math

import ape
import pytest

from tests import AgentEnum


def test_constructor(alice, relayer, agent_blueprint, mock_bridge, ZERO_ADDRESS):
    assert relayer.OWNERSHIP_AGENT() != ZERO_ADDRESS
    assert relayer.PARAMETER_AGENT() != ZERO_ADDRESS
    assert relayer.EMERGENCY_AGENT() != ZERO_ADDRESS
    assert relayer.MESSENGER() == mock_bridge


@pytest.mark.parametrize("agent", AgentEnum)
def test_relay_success(alice, relayer, mock_bridge, agent, agents):
    agent_addr = agents[int(math.log2(agent))]
    tx = relayer.relay(agent, [(alice.address, b"")], sender=mock_bridge)

    targets = [f.contract_address for f in tx.trace if f.op == "CALL"]
    assert {agent_addr, alice.address} == set(targets)


def test_relay_invalid_caller(alice, relayer):
    with ape.reverts():
        relayer.relay(AgentEnum.OWNERSHIP, [(alice.address, b"")], sender=alice)


def test_relay_invalid_agent(alice, relayer, mock_bridge):
    with ape.reverts():
        relayer.relay(42, [(alice.address, b"")], sender=mock_bridge)
