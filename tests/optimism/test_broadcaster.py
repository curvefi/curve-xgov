import itertools

import ape
import eth_abi
import pytest
from eth_utils import keccak


def test_constructor(alice, bob, charlie, project, mock_chain, mock_messenger):
    broadcaster = project.OptimismBroadcaster.deploy(
        (alice, bob, charlie), mock_chain, mock_messenger, sender=alice
    )
    assert broadcaster.admins() == (alice, bob, charlie)
    assert broadcaster.ovm_chain() == mock_chain
    assert broadcaster.ovm_messenger() == mock_messenger


@pytest.mark.parametrize("idx,gas_limit", itertools.product(range(3), [0, 1]))
def test_broadcast_success(
    alice, bob, charlie, broadcaster, mock_chain, mock_messenger, idx, gas_limit
):
    msg_sender = [alice, bob, charlie][idx]

    tx = broadcaster.broadcast([(alice.address, b"")], gas_limit, sender=msg_sender)

    tx_trace = list(tx.trace)
    staticcall_targets = {
        eth_abi.decode_single("address", f.stack[-2]) for f in tx_trace if f.op == "STATICCALL"
    }
    decoded = eth_abi.decode_single("(uint256,(address,bytes)[])", mock_messenger.data()[4:])

    assert mock_messenger.count() == 1
    assert len(mock_messenger.data()) < 500
    assert mock_messenger.data()[:4] == keccak(text="relay(uint256,(address,bytes)[])")[:4]
    assert decoded[0] == 2**idx
    assert decoded[1] == ((alice.address.lower(), b""),)

    if gas_limit == 0:
        assert mock_chain.address.lower() in staticcall_targets
    else:
        assert mock_chain.address.lower() not in staticcall_targets


def test_broadcast_reverts(dave, broadcaster):
    with ape.reverts():
        broadcaster.broadcast([(dave.address, b"")], 0, sender=dave)


def test_set_ovm_chain(alice, broadcaster, ZERO_ADDRESS):
    tx = broadcaster.set_ovm_chain(ZERO_ADDRESS, sender=alice)

    assert broadcaster.ovm_chain() == ZERO_ADDRESS
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak(text="SetOVMChain(address)")


def test_set_ovm_chain_reverts(bob, broadcaster, ZERO_ADDRESS):
    with ape.reverts():
        broadcaster.set_ovm_chain(ZERO_ADDRESS, sender=bob)


def test_set_ovm_messenger(alice, broadcaster, ZERO_ADDRESS):
    tx = broadcaster.set_ovm_messenger(ZERO_ADDRESS, sender=alice)

    assert broadcaster.ovm_messenger() == ZERO_ADDRESS
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak(text="SetOVMMessenger(address)")


def test_set_ovm_messenger_reverts(bob, broadcaster, ZERO_ADDRESS):
    with ape.reverts():
        broadcaster.set_ovm_messenger(ZERO_ADDRESS, sender=bob)


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
