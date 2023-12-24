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

## Base

### Mainnet Deployment Addresses

| Name                                                        | Address                                                                                                                          |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| [L1 Broadcaster](contracts/optimism/OptimismBroadcaster.vy) | [0xcb843280c5037acfa67b8d4adc71484ced7c48c9](https://etherscan.io/address/0xcb843280c5037acfa67b8d4adc71484ced7c48c9)            |
| [L2 Relayer](contracts/optimism/OptimismRelayer.vy)         | [0xCb843280C5037ACfA67b8D4aDC71484ceD7C48C9](https://basescan.org/address/0xCb843280C5037ACfA67b8D4aDC71484ceD7C48C9) |
| [L2 Ownership Agent](contracts/Agent.vy)                    | [0x2c163fe0f079d138b9c04f780d735289344C8B80](https://basescan.org/address/0x2c163fe0f079d138b9c04f780d735289344C8B80) |
| [L2 Parameter Agent](contracts/Agent.vy)                    | [0x7Ea4B72f04D8B02994F4EdB171Ce5F56eEdF457F](https://basescan.org/address/0x7Ea4B72f04D8B02994F4EdB171Ce5F56eEdF457F) |
| [L2 Emergency Agent](contracts/Agent.vy)                    | [0x95F0f720CAdDED982E6998b3390E6D3788c2CE5C](https://basescan.org/address/0x95F0f720CAdDED982E6998b3390E6D3788c2CE5C) |
| [L2 Vault](contracts/Vault.vy)                              | [0xA4c0eA0fb8eb652e11C8123E589197E18Ca78AA8](https://basescan.org/address/0xA4c0eA0fb8eb652e11C8123E589197E18Ca78AA8) |
| [Agent Blueprint](scripts/deploy_blueprint.py)              | [0xF3BC9E5fA891977DCa765ff52E8f22A1F7d49c1f](https://basescan.org/address/0xF3BC9E5fA891977DCa765ff52E8f22A1F7d49c1f) |

## Mantle

### Mainnet Deployment Addresses

| Name                                                        | Address                                                                                                                          |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| [L1 Broadcaster](contracts/optimism/OptimismBroadcaster.vy) | [0xb50b9a0d8a4ed8115fe174f300465ea4686d86df](https://etherscan.io/address/0xb50b9a0d8a4ed8115fe174f300465ea4686d86df)            |
| [L2 Relayer](contracts/optimism/OptimismRelayer.vy)         | [0xB50B9a0D8A4ED8115Fe174F300465Ea4686d86Df](https://explorer.mantle.xyz/address/0xB50B9a0D8A4ED8115Fe174F300465Ea4686d86Df) |
| [L2 Ownership Agent](contracts/Agent.vy)                    | [0xfe87a6cdca1eeb90987c6a196a1c5f5c76f5f2b0](https://explorer.mantle.xyz/address/0xfe87a6cdca1eeb90987c6a196a1c5f5c76f5f2b0) |
| [L2 Parameter Agent](contracts/Agent.vy)                    | [0x024d362f7aa162d8591304016fd60a209efc527e](https://explorer.mantle.xyz/address/0x024d362f7aa162d8591304016fd60a209efc527e) |
| [L2 Emergency Agent](contracts/Agent.vy)                    | [0x4339b53cf7f6eec1a997ceea81165e45c1244429](https://explorer.mantle.xyz/address/0x4339b53cf7f6eec1a997ceea81165e45c1244429) |
| [L2 Vault](contracts/Vault.vy)                              | [0x77A214bd4ee3650e5608339BBbE04b09f5546ECF](https://explorer.mantle.xyz/address/0x77A214bd4ee3650e5608339BBbE04b09f5546ECF) |
| [Agent Blueprint](scripts/deploy_blueprint.py)              | [0x5EF72230578b3e399E6C6F4F6360edF95e83BBfd](https://explorer.mantle.xyz/address/0x5EF72230578b3e399E6C6F4F6360edF95e83BBfd) |
