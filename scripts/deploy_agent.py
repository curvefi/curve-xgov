import click
from ape import project
from ape.cli import ConnectedProviderCommand, account_option, network_option


@click.command(cls=ConnectedProviderCommand)
@account_option()
@network_option()
def cli(account, network):
    receipt = project.Agent.declare(
        sender=account,
        gas_price=project.provider.gas_price,
    )
    click.echo(f"Agent blueprint deployed at: {receipt.contract_address}")
