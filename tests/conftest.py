import pytest


@pytest.fixture(scope="session")
def alice(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def bob(accounts):
    yield accounts[1]


@pytest.fixture(scope="session")
def charlie(accounts):
    yield accounts[2]


@pytest.fixture(scope="session")
def dave(accounts):
    yield accounts[3]


@pytest.fixture(scope="session")
def NATIVE_ADDRESS():
    yield "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"


@pytest.fixture(scope="session")
def ZERO_ADDRESS():
    yield "0x0000000000000000000000000000000000000000"


@pytest.fixture(scope="module")
def agent_blueprint(alice, project):
    yield project.Agent.declare(sender=alice).contract_address
