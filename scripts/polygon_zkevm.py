import click
from ape import project
from ape.cli import NetworkBoundCommand, account_option, network_option


POLYGON_ZKEVM_BRIDGE = "0x2a3DD3EB832aF982ec71669E178424b10Dca2EDe"


@click.command(cls=NetworkBoundCommand)
@account_option()
@network_option()
@click.option("--blueprint")
@click.option("--destination_chain_id")
def cli(account, network, blueprint, destination_chain_id):
    chain_id = project.provider.chain_id

    if chain_id not in (1,):
        relayer = project.PolygonzkEVMRelayer.deploy(
            blueprint,
            POLYGON_ZKEVM_BRIDGE,
            0,  # origin_network = Ethereum
            gas_limit=800_000,
            gas_price=project.provider.gas_price,
            sender=account,
        )
        return project.Vault.deploy(
            relayer.OWNERSHIP_AGENT(), gas_price=project.provider.gas_price, sender=account
        )

    # L1
    if chain_id == 1:
        admins = (
            "0x40907540d8a6C65c637785e8f8B742ae6b0b9968",
            "0x4EEb3bA4f221cA16ed4A0cC7254E2E32DF948c5f",
            "0x467947EE34aF926cF1DCac093870f613C96B1E0c",
        )

    if destination_chain_id == 196:  # xlayer
        destination_network = 3
    return project.PolygonzkEVMBroadcaster.deploy(admins, POLYGON_ZKEVM_BRIDGE, destination_network, sender=account)
