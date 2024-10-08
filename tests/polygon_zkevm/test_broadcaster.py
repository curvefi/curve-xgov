import itertools

import ape
import eth_abi
import pytest
from eth_utils import keccak


def test_constructor(alice, bob, charlie, broadcaster, mock_bridge, chain_id, relayer):
    assert broadcaster.admins() == (alice, bob, charlie)
    assert broadcaster.POLYGON_ZKEVM_BRIDGE() == mock_bridge
    assert broadcaster.destination_data(chain_id) == (1, relayer)


@pytest.mark.parametrize("idx,force_update", itertools.product(range(3), [False, True]))
def test_broadcast_success(
    alice, bob, charlie, broadcaster, chain_id, mock_bridge, idx, force_update
):
    msg_sender = [alice, bob, charlie][idx]

    broadcaster.broadcast(chain_id, [(alice.address, b"")], force_update, sender=msg_sender)

    decoded = eth_abi.decode(["uint256", "(address,bytes)[]"], mock_bridge.metadata()[4:])

    assert mock_bridge.count() == 1
    assert len(mock_bridge.metadata()) < 500
    assert mock_bridge.metadata()[:4] == keccak(text="relay(uint256,(address,bytes)[])")[:4]
    assert decoded[0] == 2**idx
    assert decoded[1] == ((alice.address.lower(), b""),)

    assert mock_bridge.force_updated() == force_update


def test_broadcast_reverts(alice, dave, broadcaster, chain_id, ZERO_ADDRESS):
    with ape.reverts():
        broadcaster.broadcast(chain_id, [(dave.address, b"")], False, sender=dave)
    with ape.reverts():
        broadcaster.broadcast(chain_id + 1, [(dave.address, b"")], False, sender=alice)


def test_set_destination_data(alice, bob, broadcaster, chain_id, ZERO_ADDRESS):
    tx = broadcaster.set_destination_data(chain_id + 1, (2, bob), sender=alice)

    assert broadcaster.destination_data(chain_id + 1) == (2, bob)
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak(text="SetDestinationData(uint256,(uint32,address))")
    assert int(tx.logs[0]["topics"][1].hex(), base=16) == chain_id + 1


def test_set_destination_data_reverts(bob, broadcaster, chain_id, ZERO_ADDRESS):
    with ape.reverts():
        broadcaster.set_destination_data(chain_id + 1, (2, bob), sender=bob)


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
