import itertools

import ape
import eth_abi
import pytest
from eth_utils import keccak


def test_constructor(
    alice, bob, charlie, broadcaster, chain_id, relayer, mock_chain, mock_messenger
):
    assert broadcaster.admins() == (alice, bob, charlie)
    assert broadcaster.destination_data(chain_id) == (mock_chain, mock_messenger, relayer)


@pytest.mark.parametrize("idx,gas_limit", itertools.product(range(3), [0, 1]))
def test_broadcast_success(
    alice, bob, charlie, broadcaster, chain_id, mock_chain, mock_messenger, idx, gas_limit
):
    msg_sender = [alice, bob, charlie][idx]

    tx = broadcaster.broadcast(chain_id, [(alice.address, b"")], gas_limit, sender=msg_sender)

    tx_trace = list(tx.trace)
    staticcall_targets = {f.contract_address for f in tx_trace if f.op == "STATICCALL"}
    decoded = eth_abi.decode(["uint256", "(address,bytes)[]"], mock_messenger.data()[4:])

    assert mock_messenger.count() == 1
    assert len(mock_messenger.data()) < 500
    assert mock_messenger.data()[:4] == keccak(text="relay(uint256,(address,bytes)[])")[:4]
    assert decoded[0] == 2**idx
    assert decoded[1] == ((alice.address.lower(), b""),)

    if gas_limit == 0:
        assert mock_chain.address in staticcall_targets
    else:
        assert mock_chain.address not in staticcall_targets


def test_broadcast_reverts(alice, dave, broadcaster, chain_id, ZERO_ADDRESS):
    with ape.reverts():
        broadcaster.broadcast(chain_id, [(dave.address, b"")], 0, sender=dave)
    with ape.reverts():
        broadcaster.broadcast(chain_id + 1, [(dave.address, b"")], 0, sender=alice)


def test_set_destination_data(alice, bob, broadcaster, chain_id, ZERO_ADDRESS):
    tx = broadcaster.set_destination_data(chain_id + 1, (bob, bob, bob), sender=alice)

    assert broadcaster.destination_data(chain_id + 1) == (bob, bob, bob)
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak(
        text="SetDestinationData(uint256,(address,address,address))"
    )
    assert int(tx.logs[0]["topics"][1].hex(), base=16) == chain_id + 1


def test_set_destination_data_reverts(bob, broadcaster, chain_id, ZERO_ADDRESS):
    with ape.reverts():
        broadcaster.set_destination_data(chain_id + 1, (bob, bob, bob), sender=bob)


def test_commit_admins(alice, bob, charlie, broadcaster):
    tx = broadcaster.commit_admins((alice, bob, charlie), sender=alice)

    assert broadcaster.future_admins() == (alice, bob, charlie)
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak("CommitAdmins((address,address,address))".encode())


def test_commit_admins_reverts(alice, bob, charlie, broadcaster):
    with ape.reverts():
        broadcaster.commit_admins((bob, charlie, alice), sender=bob)

    with ape.reverts():
        broadcaster.commit_admins((alice, alice, alice), sender=alice)


def test_apply_admins(alice, bob, charlie, broadcaster):
    broadcaster.commit_admins((charlie, bob, alice), sender=alice)
    tx = broadcaster.apply_admins(sender=alice)

    assert broadcaster.admins() == (charlie, bob, alice)
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak("ApplyAdmins((address,address,address))".encode())


def test_apply_admins_reverts(alice, bob, charlie, broadcaster):
    broadcaster.commit_admins((charlie, bob, alice), sender=alice)

    with ape.reverts():
        broadcaster.apply_admins(sender=bob)
