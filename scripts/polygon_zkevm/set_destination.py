import click
from ape import project
from ape.cli import ConnectedProviderCommand, account_option, network_option

from . import get_destination_network


@click.command(cls=ConnectedProviderCommand)
@account_option()
@network_option()
@click.option("--chain_id")
@click.option("--relayer")
def cli(account, chain_id, relayer):
    network = get_destination_network(chain_id)

    broadcaster = project.PolygonzkEVMBroadcaster.at("0xB5e7fE8eA8ECbd33504485756fCabB5f5D29C051")
    broadcaster.set_destination_data(chain_id, (network, relayer),
                                     sender=account, max_priority_fee="1 gwei", max_fee="20 gwei")

    # Move ownership after set up
    admins = (
        "0x40907540d8a6C65c637785e8f8B742ae6b0b9968",
        "0x4EEb3bA4f221cA16ed4A0cC7254E2E32DF948c5f",
        "0x467947EE34aF926cF1DCac093870f613C96B1E0c",
    )
    # broadcaster.commit_admins(admins, sender=account, max_priority_fee="1 gwei", max_fee="20 gwei")
    # broadcaster.apply_admins(sender=account, max_priority_fee="1 gwei", max_fee="20 gwei")
