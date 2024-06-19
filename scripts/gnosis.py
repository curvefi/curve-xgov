import click
from ape import project
from ape.cli import ConnectedProviderCommand, account_option, network_option


@click.command(cls=ConnectedProviderCommand)
@account_option()
@network_option()
@click.option("--blueprint")
def cli(account, network, blueprint):
    chain_id = project.provider.chain_id

    if chain_id not in (1,):
        relayer = project.GnosisRelayer.deploy(
            blueprint,
            "0x75Df5AF045d91108662D8080fD1FEFAd6aA0bb59",
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
        bridge = "0x4C36d2919e407f0Cc2Ee3c993ccF8ac26d9CE64e"

    return project.GnosisBroadcaster.deploy(admins, bridge, sender=account)
