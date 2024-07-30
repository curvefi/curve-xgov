import pytest


@pytest.fixture(scope="module")
def mock_bridge(alice, project):
    yield project.MockPolygonzkEVMBridge.deploy(sender=alice)


@pytest.fixture(scope="module")
def broadcaster(alice, bob, charlie, project, mock_bridge):
    yield project.PolygonzkEVMBroadcaster.deploy(
        (alice, bob, charlie), mock_bridge, 3, sender=alice
    )


@pytest.fixture(scope="module")
def relayer(alice, dave, project, broadcaster, agent_blueprint, mock_bridge):
    relayer = project.PolygonzkEVMRelayer.deploy(
        broadcaster, agent_blueprint, mock_bridge, 0, sender=alice
    )
    broadcaster.set_relayer(relayer, sender=dave)  # anyone at set up
    yield relayer


@pytest.fixture(scope="module")
def agents(relayer):
    yield [getattr(relayer, attr + "_AGENT")() for attr in ["OWNERSHIP", "PARAMETER", "EMERGENCY"]]
