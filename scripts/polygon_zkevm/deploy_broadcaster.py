import click
from ape import project
from ape.cli import ConnectedProviderCommand, account_option, network_option

from . import POLYGON_ZKEVM_BRIDGE


@click.command(cls=ConnectedProviderCommand)
@account_option()
@network_option()
def cli(account):
    chain_id = project.provider.chain_id

    if chain_id == 1:
        admins = (
            account.address,  # "0x40907540d8a6C65c637785e8f8B742ae6b0b9968",
            "0x4EEb3bA4f221cA16ed4A0cC7254E2E32DF948c5f",
            "0x467947EE34aF926cF1DCac093870f613C96B1E0c",
        )

    return project.PolygonzkEVMBroadcaster.deploy(
        admins,
        POLYGON_ZKEVM_BRIDGE,
        sender=account,
        max_priority_fee="1 gwei",
        max_fee="20 gwei",
    )
