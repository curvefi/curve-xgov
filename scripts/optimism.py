import click
from ape import project
from ape.cli import NetworkBoundCommand, account_option, network_option


@click.command(cls=NetworkBoundCommand)
@account_option()
@network_option()
@click.option("--blueprint")
def cli(account, network, blueprint):
    chain_id = project.provider.chain_id

    if chain_id not in (1, 5):
        relayer = project.OptimismRelayer.deploy(
            blueprint,
            "0x4200000000000000000000000000000000000007",
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
        ovm_chain, ovm_messenger = (
            "0x5E4e65926BA27467555EB562121fac00D24E9dD2",
            "0x25ace71c97B33Cc4729CF772ae268934F7ab5fA1",
        )
    elif chain_id == 5:
        admins = (
            account.address,
            "0x0000000000000000000000000000000000000000",
            "0xFFfFfFffFFfffFFfFFfFFFFFffFFFffffFfFFFfF",
        )
        ovm_chain, ovm_messenger = (
            "0x607F755149cFEB3a14E1Dc3A4E2450Cde7dfb04D",
            "0x5086d1eEF304eb5284A0f6720f79403b4e9bE294",
        )

    return project.OptimismBroadcaster.deploy(admins, ovm_chain, ovm_messenger, sender=account)
