import click
from ape import project
from ape.cli import ConnectedProviderCommand, account_option, network_option


@click.command(cls=ConnectedProviderCommand)
@account_option()
@network_option()
@click.option("--chain_id")
@click.option("--relayer")
def cli(account, chain_id, relayer):
    if int(chain_id) == 10:  # Optimism
        ovm_chain, ovm_messenger = (
            "0x5E4e65926BA27467555EB562121fac00D24E9dD2",
            "0x25ace71c97B33Cc4729CF772ae268934F7ab5fA1",
        )
    elif int(chain_id) == 252:  # fraxtal
        ovm_chain, ovm_messenger = (
            "0x0000000000000000000000000000000000000000",
            "0x126bcc31Bc076B3d515f60FBC81FddE0B0d542Ed",
        )
    elif int(chain_id) == 5000:  # mantle
        ovm_chain, ovm_messenger = (
            "0x291dc3819b863e19b0a9b9809F8025d2EB4aaE93",
            "0x676A795fe6E43C17c668de16730c3F690FEB7120",
        )

    broadcaster = project.OptimismBroadcaster.at("0xE0fE4416214e95F0C67Dc044AAf1E63d6972e0b9")
    broadcaster.set_destination_data(chain_id, (ovm_chain, ovm_messenger, relayer),
                                     sender=account, max_priority_fee="1 gwei", max_fee="20 gwei")

    # Move ownership after set up
    admins = (
        "0x40907540d8a6C65c637785e8f8B742ae6b0b9968",
        "0x4EEb3bA4f221cA16ed4A0cC7254E2E32DF948c5f",
        "0x467947EE34aF926cF1DCac093870f613C96B1E0c",
    )
    # broadcaster.commit_admins(admins, sender=account, max_priority_fee="1 gwei", max_fee="20 gwei")
    # broadcaster.apply_admins(sender=account, max_priority_fee="1 gwei", max_fee="20 gwei")
