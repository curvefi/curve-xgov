import ape
from eth_utils import keccak


def test_constructor(alice, bob, charlie, project, mock_chain, mock_messenger):
    broadcaster = project.OptimismBroadcaster.deploy(
        (alice, bob, charlie), mock_chain, mock_messenger, sender=alice
    )
    assert broadcaster.admins() == (alice, bob, charlie)
    assert broadcaster.ovm_chain() == mock_chain
    assert broadcaster.ovm_messenger() == mock_messenger


def test_set_ovm_chain(alice, broadcaster, ZERO_ADDRESS):
    tx = broadcaster.set_ovm_chain(ZERO_ADDRESS, sender=alice)

    assert broadcaster.ovm_chain() == ZERO_ADDRESS
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak("SetOVMChain(address)".encode())


def test_set_ovm_chain_reverts(bob, broadcaster, ZERO_ADDRESS):
    with ape.reverts():
        broadcaster.set_ovm_chain(ZERO_ADDRESS, sender=bob)


def test_set_ovm_messenger(alice, broadcaster, ZERO_ADDRESS):
    tx = broadcaster.set_ovm_messenger(ZERO_ADDRESS, sender=alice)

    assert broadcaster.ovm_messenger() == ZERO_ADDRESS
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak("SetOVMMessenger(address)".encode())


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
