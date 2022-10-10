import ape
import eth_abi
import pytest
from eth_utils import keccak


def test_constructor(alice, bob, charlie, project, mock_arb_inbox):
    broadcaster = project.ArbitrumBroadcaster.deploy(
        (alice, bob, charlie), mock_arb_inbox, alice, sender=alice, value=10**18
    )
    assert broadcaster.admins() == (alice, bob, charlie)
    assert broadcaster.arb_inbox() == mock_arb_inbox
    assert broadcaster.arb_refund() == alice


@pytest.mark.parametrize("idx", range(3))
def test_broadcast_success(alice, bob, charlie, broadcaster, mock_arb_inbox, idx):
    msg_sender = [alice, bob, charlie][idx]
    broadcaster.broadcast([(alice.address, b"")], 100_000, 10**9, sender=msg_sender)
    decoded = eth_abi.decode_single("(uint256,(address,bytes)[])", mock_arb_inbox.data()[4:])

    assert mock_arb_inbox.count() == 1
    assert len(mock_arb_inbox.data()) < 500
    assert mock_arb_inbox.data()[:4] == keccak(text="relay(uint256,(address,bytes)[])")[:4]
    assert decoded[0] == 2**idx
    assert decoded[1] == ((alice.address.lower(), b""),)

    assert mock_arb_inbox.balance == 100_000 * 10**9


def test_broadcast_reverts(dave, broadcaster):
    # invalid caller
    with ape.reverts():
        broadcaster.broadcast([(dave.address, b"")], 100_000, 10**9, sender=dave)

    # not enough funds
    with ape.reverts():
        broadcaster.broadcast([(dave.address, b"")], 100_000, 10**18, sender=dave)


def test_set_arb_inbox(alice, broadcaster):
    tx = broadcaster.set_arb_inbox(alice, sender=alice)

    assert broadcaster.arb_inbox() == alice
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak(text="SetArbInbox(address)")


def test_set_arb_inbox_reverts(bob, broadcaster):
    with ape.reverts():
        broadcaster.set_arb_inbox(bob, sender=bob)


def test_set_arb_refund(alice, bob, broadcaster):
    tx = broadcaster.set_arb_refund(bob, sender=alice)

    assert broadcaster.arb_refund() == bob
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak(text="SetArbRefund(address)")


def test_set_arb_refund_reverts(bob, broadcaster):
    with ape.reverts():
        broadcaster.set_arb_refund(bob, sender=bob)


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
