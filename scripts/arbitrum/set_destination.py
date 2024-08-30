import click
from ape import project
from ape.cli import ConnectedProviderCommand, account_option, network_option


@click.command(cls=ConnectedProviderCommand)
@account_option()
@network_option()
@click.option("--chain_id")
@click.option("--relayer")
@click.option("--vault")
def cli(account, chain_id, relayer, vault):
    if int(chain_id) == 42161:  # Arbitrum One
        arb_inbox = "0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f"
    arb_refund = vault

    broadcaster = project.ArbitrumBroadcaster.at("0x94630a56519c00Be339BBd8BD26f342Bf4bd7eE0")
    broadcaster.set_destination_data(chain_id, (arb_inbox, arb_refund, relayer),
                                     sender=account, max_priority_fee="1 gwei", max_fee="20 gwei")

    # Move ownership after set up
    admins = (
        "0x40907540d8a6C65c637785e8f8B742ae6b0b9968",
        "0x4EEb3bA4f221cA16ed4A0cC7254E2E32DF948c5f",
        "0x467947EE34aF926cF1DCac093870f613C96B1E0c",
    )
    # broadcaster.commit_admins(admins, sender=account, max_priority_fee="1 gwei", max_fee="20 gwei")
    # broadcaster.apply_admins(sender=account, max_priority_fee="1 gwei", max_fee="20 gwei")
