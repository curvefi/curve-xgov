from ape.api import ProviderAPI

POLYGON_ZKEVM_BRIDGE = "0x2a3DD3EB832aF982ec71669E178424b10Dca2EDe"
BRIDGE_ABI = [
    {"constant": False, "inputs": [
        {"indexed": False, "internalType": "bytes32[32]", "name": "smtProofLocalExitRoot", "type": "bytes32[32]"},
        {"indexed": False, "internalType": "bytes32[32]", "name": "smtProofRollupExitRoot", "type": "bytes32[32]"},
        {"indexed": False, "internalType": "uint256", "name": "globalIndex", "type": "uint256"},
        {"indexed": False, "internalType": "bytes32", "name": "mainnetExitRoot", "type": "bytes32"},
        {"indexed": False, "internalType": "bytes32", "name": "rollupExitRoot", "type": "bytes32"},
        {"indexed": False, "internalType": "uint32", "name": "originNetwork", "type": "uint32"},
        {"indexed": False, "internalType": "address", "name": "originAddress", "type": "address"},
        {"indexed": False, "internalType": "uint32", "name": "destinationNetwork", "type": "uint32"},
        {"indexed": False, "internalType": "address", "name": "destinationAddress", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
        {"indexed": False, "internalType": "bytes", "name": "metadata", "type": "bytes"}], "name": "claimMessage",
     "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
]


def get_destination_network(destination_chain_id: int | str):
    if int(destination_chain_id) == 196:  # xlayer
        return 3
    raise "Unknown destination chain id"


def get_bridge_url(provider: ProviderAPI):
    rpc = provider.http_uri  # try
    if provider.chain_id == 196:  # xlayer
        rpc = "https://rpc.xlayer.tech"
    return rpc + "/priapi/v1/ob/bridge"
