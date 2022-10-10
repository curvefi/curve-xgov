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
    initcode = bytes.fromhex(project.Agent.contract_type.deployment_bytecode.bytecode[2:])
    initcode = b"\xfe\x71\x00" + initcode  # eip-5202 preamble version 0
    initcode = (
        b"\x61" + len(initcode).to_bytes(2, "big") + b"\x3d\x81\x60\x0a\x3d\x39\xf3" + initcode
    )

    tx = project.provider.network.ecosystem.create_transaction(
        chain_id=project.provider.chain_id,
        data=initcode,
        maxFeePerGas=0,
        maxPriorityFeePerGas=0,
        nonce=alice.nonce,
    )
    tx.gas_limit = project.provider.estimate_gas_cost(tx)
    tx.signature = alice.sign_transaction(tx)
    receipt = project.provider.send_transaction(tx)

    yield receipt.contract_address
