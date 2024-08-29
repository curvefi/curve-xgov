import itertools

import ape
import eth_abi
import pytest
from eth_utils import keccak


def test_constructor(alice, bob, charlie, broadcaster, mock_bridge):
    assert broadcaster.admins() == (alice, bob, charlie)
    assert broadcaster.bridge() == mock_bridge


@pytest.mark.parametrize("idx,gas", itertools.product(range(3), [0, 1_000]))
def test_broadcast_success(alice, bob, charlie, broadcaster, mock_bridge, idx, gas):
    msg_sender = [alice, bob, charlie][idx]

    if gas > 0:
        broadcaster.broadcast([(alice.address, b"")], gas, sender=msg_sender)
    else:
        broadcaster.broadcast([(alice.address, b"")], sender=msg_sender)

    decoded = eth_abi.decode(["uint256", "(address,bytes)[]"], mock_bridge.data()[4:])

    assert len(mock_bridge.data()) < 500
    assert mock_bridge.data()[:4] == keccak(text="relay(uint256,(address,bytes)[])")[:4]
    assert decoded[0] == 2**idx
    assert decoded[1] == ((alice.address.lower(), b""),)

    assert mock_bridge.gas() == gas if gas > 0 else mock_bridge.maxGasPerTx()


def test_broadcast_reverts(dave, broadcaster):
    with ape.reverts():
        broadcaster.broadcast([(dave.address, b"")], sender=dave)


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
