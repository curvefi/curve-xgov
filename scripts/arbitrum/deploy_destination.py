import click
from ape import project
from ape.cli import ConnectedProviderCommand, account_option, network_option


@click.command(cls=ConnectedProviderCommand)
@account_option()
@network_option()
@click.option("--blueprint")
def cli(account, blueprint):
    relayer = project.ArbitrumRelayer.deploy(
        "0x94630a56519c00Be339BBd8BD26f342Bf4bd7eE0",  # Broadcaster
        blueprint,
        "0x0000000000000000000000000000000000000064",
        gas_limit=4_000_000,
        gas_price=project.provider.gas_price,
        sender=account,
    )
    return relayer, project.Vault.deploy(
        relayer.OWNERSHIP_AGENT(), gas_price=project.provider.gas_price, sender=account
    )
