import math

import ape
import pytest

from tests import AgentEnum


def test_constructor(alice, broadcaster, relayer, agent_blueprint, mock_arbsys, ZERO_ADDRESS):
    assert relayer.OWNERSHIP_AGENT() != ZERO_ADDRESS
    assert relayer.PARAMETER_AGENT() != ZERO_ADDRESS
    assert relayer.EMERGENCY_AGENT() != ZERO_ADDRESS
    assert relayer.ARBSYS() == mock_arbsys
    assert relayer.BROADCASTER() == broadcaster


@pytest.mark.parametrize("agent", AgentEnum)
def test_relay_success(alice, relayer, agent, agents):
    agent_addr = agents[int(math.log2(agent))]
    tx = relayer.relay(agent, [(alice.address, b"")], sender=alice)

    targets = [f.contract_address for f in tx.trace if f.op == "CALL"]
    assert {agent_addr, alice.address} == set(targets)


def test_relay_invalid_caller(alice, relayer, mock_arbsys, ZERO_ADDRESS):
    mock_arbsys._set_l1_caller(ZERO_ADDRESS, sender=alice)
    with ape.reverts():
        relayer.relay(AgentEnum.OWNERSHIP, [(alice.address, b"")], sender=alice)


def test_relay_invalid_cross_domain_sender(alice, relayer, mock_arbsys):
    mock_arbsys._set_l1_caller(alice.address, sender=alice)
    with ape.reverts():
        relayer.relay(AgentEnum.OWNERSHIP, [(alice.address, b"")], sender=alice)


def test_relay_invalid_agent(alice, relayer):
    with ape.reverts():
        relayer.relay(42, [(alice.address, b"")], sender=alice)
