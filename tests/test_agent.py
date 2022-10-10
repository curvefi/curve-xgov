import ape
import pytest


@pytest.fixture
def agent(alice, project):
    yield project.Agent.deploy(sender=alice)


def test_constructor(alice, agent):
    assert agent.RELAYER() == alice


@pytest.mark.parametrize("size", range(9))
def test_execute_success(alice, agent, size):
    tx = agent.execute([(alice.address, b"")] * size, sender=alice)

    assert len([f for f in tx.trace if f.op == "CALL"]) == size


def test_execute_reverts_for_invalid_caller(bob, agent):
    with ape.reverts():
        agent.execute([(bob, b"")], sender=bob)
