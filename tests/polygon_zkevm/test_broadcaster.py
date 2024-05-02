import itertools

import ape
import eth_abi
import pytest
from eth_utils import keccak


def test_constructor(alice, bob, charlie, broadcaster, mock_bridge):
    assert broadcaster.admins() == (alice, bob, charlie)
    assert broadcaster.polygon_zkevm_bridge() == mock_bridge
    assert broadcaster.destination_network() == 3


@pytest.mark.parametrize("idx,force_update", itertools.product(range(3), [False, True]))
def test_broadcast_success(
    alice, bob, charlie, broadcaster, mock_bridge, idx, force_update
):
    msg_sender = [alice, bob, charlie][idx]

    tx = broadcaster.broadcast([(alice.address, b"")], force_update, sender=msg_sender)

    decoded = eth_abi.decode_single("(uint256,(address,bytes)[])", mock_bridge.metadata()[4:])

    assert mock_bridge.count() == 1
    assert len(mock_bridge.metadata()) < 500
    assert mock_bridge.metadata()[:4] == keccak(text="relay(uint256,(address,bytes)[])")[:4]
    assert decoded[0] == 2**idx
    assert decoded[1] == ((alice.address.lower(), b""),)

    assert mock_bridge.force_updated() == force_update


def test_broadcast_reverts(dave, broadcaster):
    with ape.reverts():
        broadcaster.broadcast([(dave.address, b"")], False, sender=dave)


def test_set_new_bridge(alice, bob, broadcaster, ZERO_ADDRESS):
    tx = broadcaster.set_new_bridge(ZERO_ADDRESS, sender=alice)

    assert broadcaster.polygon_zkevm_bridge() == ZERO_ADDRESS
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak(text="SetNewBridge(address)")

    with ape.reverts():
        broadcaster.set_new_bridge(ZERO_ADDRESS, sender=bob)


def test_set_destination_network(alice, bob, broadcaster, ZERO_ADDRESS):
    tx = broadcaster.set_destination_network(2, sender=alice)

    assert broadcaster.destination_network() == 2
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak(text="SetNewDestinationNetwork(uint32)")

    with ape.reverts():
        broadcaster.set_destination_network(2, sender=bob)


def test_commit_admins(alice, bob, charlie, broadcaster):
    tx = broadcaster.commit_admins((alice, bob, charlie), sender=alice)

    assert broadcaster.future_admins() == (alice, bob, charlie)
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak("CommitAdmins((address,address,address))".encode())

    with ape.reverts():
        broadcaster.commit_admins((bob, charlie, alice), sender=bob)

    with ape.reverts():
        broadcaster.commit_admins((alice, alice, alice), sender=alice)


def test_apply_admins(alice, bob, charlie, broadcaster):
    broadcaster.commit_admins((charlie, bob, alice), sender=alice)

    with ape.reverts():
        broadcaster.apply_admins(sender=bob)

    tx = broadcaster.apply_admins(sender=alice)

    assert broadcaster.admins() == (charlie, bob, alice)
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak("ApplyAdmins((address,address,address))".encode())
