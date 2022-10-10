from typing import Union

import click
from ape import project
from ape.cli import NetworkBoundCommand, account_option, network_option


def get_blueprint_initcode(initcode: Union[str, bytes]):
    if isinstance(initcode, str):
        initcode = bytes.fromhex(initcode.removeprefix("0x"))
    initcode = b"\xfe\x71\x00" + initcode  # eip-5202 preamble version 0
    initcode = (
        b"\x61" + len(initcode).to_bytes(2, "big") + b"\x3d\x81\x60\x0a\x3d\x39\xf3" + initcode
    )
    return initcode


@click.command(cls=NetworkBoundCommand)
@account_option()
@network_option()
@click.argument("name")
def cli(account, network, name):
    contract = getattr(project, name)
    initcode = get_blueprint_initcode(contract.contract_type.deployment_bytecode.bytecode)
    tx = project.provider.network.ecosystem.create_transaction(
        chain_id=project.provider.chain_id,
        data=initcode,
        gas_price=project.provider.gas_price,
        nonce=account.nonce,
    )
    tx.gas_limit = project.provider.estimate_gas_cost(tx)
    tx.signature = account.sign_transaction(tx)

    receipt = project.provider.send_transaction(tx)
    click.echo(f"{name.title()} blueprint deployed at: {receipt.contract_address}")
