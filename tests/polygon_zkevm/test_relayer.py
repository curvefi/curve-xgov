import math

import ape
import eth_abi
import pytest
from eth_utils import keccak

from tests import AgentEnum


def test_constructor(alice, broadcaster, relayer, mock_bridge, ZERO_ADDRESS):
    assert relayer.OWNERSHIP_AGENT() != ZERO_ADDRESS
    assert relayer.PARAMETER_AGENT() != ZERO_ADDRESS
    assert relayer.EMERGENCY_AGENT() != ZERO_ADDRESS
    assert relayer.MESSENGER() == mock_bridge
    assert relayer.BROADCASTER() == broadcaster


@pytest.mark.parametrize("agent", AgentEnum)
def test_relay_success(alice, bob, relayer, mock_bridge, agent, agents, broadcaster):
    agent_addr = agents[int(math.log2(agent))]
    data = keccak(text="relay(uint256,(address,bytes)[])")[:4] + eth_abi.encode(
        ["uint256", "(address,bytes)[]"], [agent, [(alice.address, b"")]]
    )

    mock_bridge.bridgeMessage(1, relayer.address, False, data, sender=broadcaster)
    mock_bridge._set_destination_address(relayer, sender=alice)
    mock_bridge._set_origin_address(broadcaster, sender=alice)
    tx = mock_bridge.claimMessage(sender=alice)

    targets = [f.contract_address for f in tx.trace if f.op == "CALL"]
    assert {relayer.address, agent_addr, alice.address} == set(targets)

    # invalid caller
    with ape.reverts():
        relayer.relay(agent, [(alice.address, b"")], sender=alice)

    # invalid caller
    with ape.reverts():
        relayer.onMessageReceived(broadcaster.address, 0, data, sender=alice)

    # invalid sender
    mock_bridge.bridgeMessage(1, relayer.address, False, data, sender=bob)
    mock_bridge._set_destination_address(relayer, sender=alice)
    mock_bridge._set_origin_address(alice, sender=alice)
    with ape.reverts():
        mock_bridge.claimMessage(sender=alice)

    # invalid origin network
    mock_bridge._set_origin_network(2, sender=alice)
    mock_bridge.bridgeMessage(1, relayer.address, False, data, sender=broadcaster)
    mock_bridge._set_destination_address(relayer, sender=alice)
    mock_bridge._set_origin_address(relayer, sender=alice)
    with ape.reverts():
        mock_bridge.claimMessage(sender=alice)
