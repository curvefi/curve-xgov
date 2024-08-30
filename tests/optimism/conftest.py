import pytest


@pytest.fixture(scope="module")
def chain_id():
    return 10


@pytest.fixture(scope="module")
def mock_messenger(alice, project):
    yield project.MockCrossDomainMessenger.deploy(sender=alice)


@pytest.fixture(scope="module")
def broadcaster(alice, bob, charlie, project, mock_chain, mock_messenger):
    contract = project.OptimismBroadcaster.deploy((alice, bob, charlie), sender=alice)
    mock_messenger._set_sender(contract, sender=alice)
    return contract


@pytest.fixture(scope="module")
def relayer(
    alice, dave, project, broadcaster, agent_blueprint, mock_messenger, chain_id, mock_chain
):
    relayer = project.OptimismRelayer.deploy(
        broadcaster, agent_blueprint, mock_messenger, sender=alice
    )
    broadcaster.set_destination_data(chain_id, (mock_chain, mock_messenger, relayer), sender=alice)
    yield relayer


@pytest.fixture(scope="module")
def agents(relayer):
    yield [getattr(relayer, attr + "_AGENT")() for attr in ["OWNERSHIP", "PARAMETER", "EMERGENCY"]]


@pytest.fixture(scope="module")
def mock_chain(alice, project):
    yield project.MockCanonicalTransactionChain.deploy(sender=alice)
