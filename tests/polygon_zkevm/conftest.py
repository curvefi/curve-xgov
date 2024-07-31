import pytest


@pytest.fixture(scope="module")
def chain_id():
    return 1101


@pytest.fixture(scope="module")
def mock_bridge(alice, project):
    yield project.MockPolygonzkEVMBridge.deploy(sender=alice)


@pytest.fixture(scope="module")
def broadcaster(alice, bob, charlie, project, mock_bridge):
    yield project.PolygonzkEVMBroadcaster.deploy((alice, bob, charlie), mock_bridge, sender=alice)


@pytest.fixture(scope="module")
def relayer(alice, project, broadcaster, agent_blueprint, mock_bridge, chain_id):
    relayer = project.PolygonzkEVMRelayer.deploy(
        broadcaster, agent_blueprint, mock_bridge, 0, sender=alice
    )
    broadcaster.set_destination_data(chain_id, (1, relayer), sender=alice)
    yield relayer


@pytest.fixture(scope="module")
def agents(relayer):
    yield [getattr(relayer, attr + "_AGENT")() for attr in ["OWNERSHIP", "PARAMETER", "EMERGENCY"]]
