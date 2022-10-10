import pytest


@pytest.fixture(scope="module")
def mock_messenger(alice, project):
    yield project.MockCrossDomainMessenger.deploy(sender=alice)


@pytest.fixture(scope="module")
def relayer(alice, project, agent_blueprint, mock_messenger):
    relayer = project.OptimismRelayer.deploy(agent_blueprint, mock_messenger, sender=alice)
    mock_messenger._set_sender(relayer, sender=alice)
    yield relayer


@pytest.fixture(scope="module")
def agents(relayer):
    yield [getattr(relayer, attr + "_AGENT")() for attr in ["OWNERSHIP", "PARAMETER", "EMERGENCY"]]


@pytest.fixture(scope="module")
def mock_chain(alice, project):
    yield project.MockCanonicalTransactionChain.deploy(sender=alice)


@pytest.fixture(scope="module")
def broadcaster(alice, bob, charlie, project, mock_chain, mock_messenger):
    yield project.OptimismBroadcaster.deploy(
        (alice, bob, charlie), mock_chain, mock_messenger, sender=alice
    )
