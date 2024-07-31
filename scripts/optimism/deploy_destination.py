import click
from ape import project
from ape.cli import ConnectedProviderCommand, account_option, network_option


@click.command(cls=ConnectedProviderCommand)
@account_option()
@network_option()
@click.option("--blueprint")
def cli(account, blueprint):
    relayer = project.OptimismRelayer.deploy(
        "0xE0fE4416214e95F0C67Dc044AAf1E63d6972e0b9",  # Broadcaster
        blueprint,
        "0x4200000000000000000000000000000000000007",
        gas_limit=800_000,
        gas_price=project.provider.gas_price,
        sender=account,
    )
    return relayer, project.Vault.deploy(
        relayer.OWNERSHIP_AGENT(), gas_price=project.provider.gas_price, sender=account
    )
