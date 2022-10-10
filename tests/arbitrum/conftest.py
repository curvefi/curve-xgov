import pytest


@pytest.fixture(scope="module")
def mock_arbsys(alice, project):
    yield project.MockArbSys.deploy(sender=alice)


@pytest.fixture(scope="module")
def relayer(alice, project, agent_blueprint, mock_arbsys):
    relayer = project.ArbitrumRelayer.deploy(agent_blueprint, mock_arbsys, sender=alice)
    mock_arbsys._set_l1_caller(relayer, sender=alice)
    yield relayer


@pytest.fixture(scope="module")
def agents(relayer):
    yield [getattr(relayer, attr + "_AGENT")() for attr in ["OWNERSHIP", "PARAMETER", "EMERGENCY"]]


@pytest.fixture(scope="module")
def mock_arb_inbox(alice, project):
    yield project.MockArbSys.deploy(sender=alice)


@pytest.fixture(scope="module")
def broadcaster(alice, bob, charlie, project, mock_arb_inbox):
    yield project.ArbitrumBroadcaster.deploy(
        (alice, bob, charlie), mock_arb_inbox, alice, sender=alice, value=10**18
    )
