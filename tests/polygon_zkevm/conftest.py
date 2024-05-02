import pytest


@pytest.fixture(scope="module")
def mock_bridge(alice, project):
    yield project.MockPolygonzkEVMBridge.deploy(sender=alice)


@pytest.fixture(scope="module")
def relayer(alice, project, agent_blueprint, mock_bridge):
    relayer = project.PolygonzkEVMRelayer.deploy(agent_blueprint, mock_bridge, 0, sender=alice)
    yield relayer


@pytest.fixture(scope="module")
def agents(relayer):
    yield [getattr(relayer, attr + "_AGENT")() for attr in ["OWNERSHIP", "PARAMETER", "EMERGENCY"]]


@pytest.fixture(scope="module")
def broadcaster(alice, bob, charlie, project, mock_bridge):
    yield project.PolygonzkEVMBroadcaster.deploy(
        (alice, bob, charlie), mock_bridge, 3, sender=alice
    )
