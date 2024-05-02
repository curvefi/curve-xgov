import math

import ape
import eth_abi
import pytest

from tests import AgentEnum


def test_constructor(alice, project, agent_blueprint, mock_messenger, ZERO_ADDRESS):
    relayer = project.OptimismRelayer.deploy(agent_blueprint, mock_messenger, sender=alice)

    assert relayer.OWNERSHIP_AGENT() != ZERO_ADDRESS
    assert relayer.PARAMETER_AGENT() != ZERO_ADDRESS
    assert relayer.EMERGENCY_AGENT() != ZERO_ADDRESS
    assert relayer.MESSENGER() == mock_messenger


@pytest.mark.parametrize("agent", AgentEnum)
def test_relay_success(alice, relayer, mock_messenger, agent, agents):
    agent_addr = agents[int(math.log2(agent))]
    tx = relayer.relay(agent, [(alice.address, b"")], sender=mock_messenger)

    targets = [f.contract_address for f in tx.trace if f.op == "CALL"]
    assert {agent_addr, alice.address} == set(targets)


def test_relay_invalid_caller(alice, relayer):
    with ape.reverts():
        relayer.relay(AgentEnum.OWNERSHIP, [(alice.address, b"")], sender=alice)


def test_relay_invalid_cross_domain_sender(alice, relayer, mock_messenger):
    mock_messenger._set_sender(alice.address, sender=alice)
    with ape.reverts():
        relayer.relay(AgentEnum.OWNERSHIP, [(alice.address, b"")], sender=mock_messenger)


def test_relay_invalid_agent(alice, relayer, mock_messenger):
    with ape.reverts():
        relayer.relay(42, [(alice.address, b"")], sender=mock_messenger)
