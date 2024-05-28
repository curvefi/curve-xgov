import click
import requests

from ape import project, Contract
from ape.cli import ConnectedProviderCommand, account_option, network_option

from . import BRIDGE_ABI, POLYGON_ZKEVM_BRIDGE, get_bridge_url


@click.command(cls=ConnectedProviderCommand)
@account_option()
@network_option()
@click.option("--deposit_cnt")
def cli(account, network, deposit_cnt):
    chain_id = project.provider.chain_id

    if chain_id not in (1,):
        bridge = Contract(POLYGON_ZKEVM_BRIDGE, abi=BRIDGE_ABI)
        url = get_bridge_url(project.provider)

        status = requests.get(
            url=f"{url}/bridge",
            params={"net_id": 0, "deposit_cnt": int(deposit_cnt)},
        ).json()["deposit"]
        if not status["ready_for_claim"]:
            raise "Not ready yet"

        proof = requests.get(
            url=f"{url}/merkle-proof",
            params={"net_id": 0, "deposit_cnt": int(deposit_cnt)},
        ).json()

        bridge.claimMessage(
            proof["proof"]["merkle_proof"],
            proof["proof"]["rollup_merkle_proof"],
            status["global_index"],
            proof["proof"]["main_exit_root"],
            proof["proof"]["rollup_exit_root"],
            status["orig_net"],
            status["orig_addr"],
            status["dest_net"],
            status["dest_addr"],
            status["amount"],
            status["metadata"],
            gas_price=project.provider.gas_price,
            sender=account,
        )
