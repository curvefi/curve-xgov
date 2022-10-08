import pytest

# account fixtures


@pytest.fixture(scope="session")
def alice(accounts):
    yield accounts[0]


# optimism fixtures


@pytest.fixture
def cross_domain_messenger(alice, project):
    yield project.CrossDomainMessenger.deploy(sender=alice)


@pytest.fixture
def canonical_transaction_chain(alice, project):
    yield project.CanonicalTransactionChain.deploy(sender=alice)


@pytest.fixture
def l1_optimism_proxy(alice, project, cross_domain_messenger, canonical_transaction_chain):
    yield project.L1OptimismProxy.deploy(
        (alice, alice, alice), cross_domain_messenger, canonical_transaction_chain, sender=alice
    )
