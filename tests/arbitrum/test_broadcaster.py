import ape
import eth_abi
import pytest
from eth_utils import keccak


def test_constructor(alice, bob, charlie, broadcaster, chain_id, relayer, mock_arb_inbox):
    assert broadcaster.admins() == (alice, bob, charlie)
    assert broadcaster.destination_data(chain_id) == (mock_arb_inbox, alice, relayer)


@pytest.mark.parametrize("idx", range(3))
def test_broadcast_success(alice, bob, charlie, broadcaster, chain_id, mock_arb_inbox, idx):
    msg_sender = [alice, bob, charlie][idx]
    broadcaster.broadcast(chain_id, [(alice.address, b"")], 100_000, 10**9, sender=msg_sender)
    decoded = eth_abi.decode(["uint256", "(address,bytes)[]"], mock_arb_inbox.data()[4:])

    assert mock_arb_inbox.count() == 1
    assert len(mock_arb_inbox.data()) < 500
    assert mock_arb_inbox.data()[:4] == keccak(text="relay(uint256,(address,bytes)[])")[:4]
    assert decoded[0] == 2**idx
    assert decoded[1] == ((alice.address.lower(), b""),)

    assert mock_arb_inbox.balance == 100_000 * 10**9


def test_broadcast_reverts(alice, dave, broadcaster, chain_id, ZERO_ADDRESS):
    # invalid caller
    with ape.reverts():
        broadcaster.broadcast(chain_id, [(dave.address, b"")], 100_000, 10**9, sender=dave)

    # not enough funds
    with ape.reverts():
        broadcaster.broadcast(chain_id, [(dave.address, b"")], 100_000, 10**18, sender=alice)

    # relayer == empty(address)
    with ape.reverts():
        broadcaster.broadcast(chain_id + 2, [(dave.address, b"")], 100_000, 10**9, sender=alice)


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


def test_default_method_receives_ether(alice, broadcaster):
    pre_balance = broadcaster.balance
    alice.transfer(broadcaster, 10**18)

    assert broadcaster.balance == pre_balance + 10**18


def test_default_method_reverts_with_data(alice, broadcaster):
    with ape.reverts():
        alice.transfer(broadcaster, 10**18, data=b"Hello")
