import click
from ape import project
from ape.cli import ConnectedProviderCommand, account_option, network_option

from . import POLYGON_ZKEVM_BRIDGE


@click.command(cls=ConnectedProviderCommand)
@account_option()
@network_option()
@click.option("--blueprint")
def cli(account, blueprint):
    relayer = project.PolygonzkEVMRelayer.deploy(
        "0xB5e7fE8eA8ECbd33504485756fCabB5f5D29C051",  # Broadcaster
        blueprint,
        POLYGON_ZKEVM_BRIDGE,
        0,  # origin_network = Ethereum
        gas_limit=800_000,
        gas_price=project.provider.gas_price,
        sender=account,
    )
    return relayer, project.Vault.deploy(
        relayer.OWNERSHIP_AGENT(), gas_price=project.provider.gas_price, sender=account
    )

