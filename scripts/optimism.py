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
def cli(account, network):
    chain_id = project.provider.chain_id

    # L1
    if chain_id in (1, 5):

        if chain_id == 1:
            admins = (
                "0x40907540d8a6C65c637785e8f8B742ae6b0b9968",
                "0x4EEb3bA4f221cA16ed4A0cC7254E2E32DF948c5f",
                "0x467947EE34aF926cF1DCac093870f613C96B1E0c",
            )
            ovm_chain, ovm_messenger = (
                "0x5E4e65926BA27467555EB562121fac00D24E9dD2",
                "0x25ace71c97B33Cc4729CF772ae268934F7ab5fA1",
            )
        else:
            admins = (
                account.address,
                "0x0000000000000000000000000000000000000000",
                "0xFFfFfFffFFfffFFfFFfFFFFFffFFFffffFfFFFfF",
            )
            ovm_chain, ovm_messenger = (
                "0x607F755149cFEB3a14E1Dc3A4E2450Cde7dfb04D",
                "0x5086d1eEF304eb5284A0f6720f79403b4e9bE294",
            )

        account.transfer(account, value="0 gwei")
        project.OptimismBroadcaster.deploy(admins, ovm_chain, ovm_messenger, sender=account)

        return

    # L2
    initcode = get_blueprint_initcode(project.Agent.contract_type.deployment_bytecode.bytecode)
    tx = project.provider.network.ecosystem.create_transaction(
        chain_id=project.provider.chain_id,
        data=initcode,
        gas_price=project.provider.gas_price,
        nonce=account.nonce,
    )
    tx.gas_limit = project.provider.estimate_gas_cost(tx)
    tx.signature = account.sign_transaction(tx)

    receipt = project.provider.send_transaction(tx)
    click.echo(f"Agent blueprint deployed at: {receipt.contract_address}")

    project.OptimismRelayer.deploy(
        receipt.contract_address,
        "0x4200000000000000000000000000000000000007",
        gas_price=project.provider.gas_price,
        sender=account,
    )
