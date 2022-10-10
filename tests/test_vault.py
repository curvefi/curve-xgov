import ape
import pytest
from eth_utils import keccak


@pytest.fixture
def vault(alice, project):
    yield project.Vault.deploy(alice.address, sender=alice)


def test_vault_constructor(alice, project):
    vault = project.Vault.deploy(alice.address, sender=alice)

    assert vault.owner() == alice


def test_transfer_sends_native_asset(alice, vault, NATIVE_ADDRESS):
    balance = alice.balance
    alice.transfer(vault, 10**18)

    vault.transfer(NATIVE_ADDRESS, alice, 10**18, sender=alice)
    assert alice.balance == balance and vault.balance == 0


def test_transfer_reverts_for_invalid_caller(bob, vault, NATIVE_ADDRESS):
    with ape.reverts():
        vault.transfer(NATIVE_ADDRESS, bob, 10**18, sender=bob)


def test_vault_commit_future_owner(alice, bob, vault):
    tx = vault.commit_future_owner(bob, sender=alice)

    assert vault.future_owner() == bob
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak(text="CommitOwnership(address)")


def test_vault_commit_future_owner_reverts(bob, vault):
    with ape.reverts():
        vault.commit_future_owner(bob, sender=bob)


def test_vault_apply_future_owner(alice, bob, vault):
    vault.commit_future_owner(bob, sender=alice)
    tx = vault.apply_future_owner(sender=alice)

    assert vault.owner() == bob
    assert len(tx.logs) == 1
    assert tx.logs[0]["topics"][0] == keccak(text="ApplyOwnership(address)")


def test_vault_apply_future_owner_reverts(alice, bob, vault):
    vault.commit_future_owner(bob, sender=alice)
    with ape.reverts():
        vault.apply_future_owner(sender=bob)


def test_default_method_receives_ether(alice, vault):
    alice.transfer(vault, 10**18)

    assert vault.balance == 10**18


def test_default_method_reverts_with_data(alice, vault):
    with ape.reverts():
        alice.transfer(vault, 10**18, data=b"Hello")
