# Curve Cross-Chain Governance

Extends the capabilities of the Curve DAO allowing it to interact with contracts on different networks.

## Arbitrum

### Mainnet Deployment Addresses

| Name                                                        | Address                                                                                                               |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [L1 Broadcaster](contracts/arbitrum/ArbitrumBroadcaster.vy) | [0xb7b0FF38E0A01D798B5cd395BbA6Ddb56A323830](https://etherscan.io/address/0xb7b0FF38E0A01D798B5cd395BbA6Ddb56A323830) |
| [L2 Relayer](contracts/arbitrum/ArbitrumRelayer.vy)         | [0xb7b0FF38E0A01D798B5cd395BbA6Ddb56A323830](https://arbiscan.io/address/0xb7b0FF38E0A01D798B5cd395BbA6Ddb56A323830)  |
| [L2 Ownership Agent](contracts/Agent.vy)                    | [0x452030a5D962d37D97A9D65487663cD5fd9C2B32](https://arbiscan.io/address/0x452030a5D962d37D97A9D65487663cD5fd9C2B32)  |
| [L2 Parameter Agent](contracts/Agent.vy)                    | [0x5ccbB27FB594c5cF6aC0670bbcb360c0072F6839](https://arbiscan.io/address/0x5ccbB27FB594c5cF6aC0670bbcb360c0072F6839)  |
| [L2 Emergency Agent](contracts/Agent.vy)                    | [0x2CB6E1Adf22Af1A38d7C3370441743a123991EC3](https://arbiscan.io/address/0x2CB6E1Adf22Af1A38d7C3370441743a123991EC3)  |
| [L2 Vault](contracts/Vault.vy)                              | [0x25877b9413Cc7832A6d142891b50bd53935feF82](https://arbiscan.io/address/0x25877b9413Cc7832A6d142891b50bd53935feF82)  |
| [Agent Blueprint](scripts/deploy_blueprint.py)              | [0x187FE3505e56f4dA67b06564F03575cC15bE2B4d](https://arbiscan.io/address/0x187FE3505e56f4dA67b06564F03575cC15bE2B4d)  |

### Testnet Deployment Steps

1. Deploy `Agent` blueprint to Arbitrum

   ```bash
   $ ape run deploy_blueprint Agent --network https://goerli-rollup.arbitrum.io/rpc
   ```

2. Deploy `ArbitrumRelayer` and `Vault` to Arbitrum

   ```bash
   $ ape run arbitrum --blueprint <AGENT_BLUEPRINT_ADDRESS> --network https://goerli-rollup.arbitrum.io/rpc
   ```

3. Deploy `ArbitrumBroadcaster` to Goerli

   ```bash
   $ ape run arbitrum --arb-refund <ARB_VAULT_ADDRESS> --network :goerli:infura
   ```

Note: The `ArbitrumRelayer` and the `ArbitrumBroadcaster` need to be deployed at the same address. To do so you need to use the same nonce. It's
preferable to generate a fresh account and use it for steps 2 and 3.

## Optimism

### Mainnet Deployment Addresses

| Name                                                        | Address                                                                                                                          |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| [L1 Broadcaster](contracts/optimism/OptimismBroadcaster.vy) | [0x8e1e5001C7B8920196c7E3EdF2BCf47B2B6153ff](https://etherscan.io/address/0x8e1e5001c7b8920196c7e3edf2bcf47b2b6153ff)            |
| [L2 Relayer](contracts/optimism/OptimismRelayer.vy)         | [0x8e1e5001C7B8920196c7E3EdF2BCf47B2B6153ff](https://optimistic.etherscan.io/address/0x8e1e5001c7b8920196c7e3edf2bcf47b2b6153ff) |
| [L2 Ownership Agent](contracts/Agent.vy)                    | [0x28c4A1Fa47EEE9226F8dE7D6AF0a41C62Ca98267](https://optimistic.etherscan.io/address/0x28c4A1Fa47EEE9226F8dE7D6AF0a41C62Ca98267) |
| [L2 Parameter Agent](contracts/Agent.vy)                    | [0xE7F2B72E94d1c2497150c24EA8D65aFFf1027b9b](https://optimistic.etherscan.io/address/0xE7F2B72E94d1c2497150c24EA8D65aFFf1027b9b) |
| [L2 Emergency Agent](contracts/Agent.vy)                    | [0x9fF1ddE4BE9BbD891836863d227248047B3D881b](https://optimistic.etherscan.io/address/0x9fF1ddE4BE9BbD891836863d227248047B3D881b) |
| [L2 Vault](contracts/Vault.vy)                              | [0xD166EEdf272B860E991d331B71041799379185D5](https://optimistic.etherscan.io/address/0xD166EEdf272B860E991d331B71041799379185D5) |
| [Agent Blueprint](scripts/deploy_blueprint.py)              | [0xC5fd5D3b06a8ef50b911972CA313E4d327F7c0aC](https://optimistic.etherscan.io/address/0xc5fd5d3b06a8ef50b911972ca313e4d327f7c0ac) |

### Testnet Deployment Steps

1. Deploy `Agent` blueprint to Optimism

   ```bash
   $ ape run deploy_blueprint Agent --network https://goerli.optimism.io/
   ```

2. Deploy `OptimismRelayer` and `Vault` to Optimism

   ```bash
   $ ape run optimism --blueprint <AGENT_BLUEPRINT_ADDRESS> --network https://goerli.optimism.io/
   ```

3. Deploy `OptimismBroadcaster` to Goerli

   ```bash
   $ ape run optimism --network :goerli:infura
   ```

Note: The `OptimismRelayer` and the `OptimismBroadcaster` need to be deployed at the same address. To do so you need to use the same nonce. It's
preferable to generate a fresh account and use it for steps 2 and 3.
