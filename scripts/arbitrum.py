import click
from ape import project
from ape.cli import NetworkBoundCommand, account_option, network_option


@click.command(cls=NetworkBoundCommand)
@account_option()
@network_option()
@click.argument("agent_blueprint")
@click.argument("arb_refund")
def cli(account, network, agent_blueprint, arb_refund):
    chain_id = project.provider.chain_id

    # L1
    if chain_id in (1, 5):

        if chain_id == 1:
            admins = (
                "0x40907540d8a6C65c637785e8f8B742ae6b0b9968",
                "0x4EEb3bA4f221cA16ed4A0cC7254E2E32DF948c5f",
                "0x467947EE34aF926cF1DCac093870f613C96B1E0c",
            )
            arb_inbox = "0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f"
        else:
            admins = (
                account.address,
                "0x0000000000000000000000000000000000000000",
                "0xFFfFfFffFFfffFFfFFfFFFFFffFFFffffFfFFFfF",
            )
            arb_inbox = "0x6BEbC4925716945D46F0Ec336D5C2564F419682C"

        project.ArbitrumBroadcaster.deploy(admins, arb_inbox, arb_refund, sender=account)

        return

    # L2
    project.ArbitrumRelayer.deploy(
        agent_blueprint,
        "0x0000000000000000000000000000000000000064",
        gas_limit=800_000,
        gas_price=project.provider.gas_price,
        sender=account,
    )
