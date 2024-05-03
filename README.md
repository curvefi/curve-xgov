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
| [Agent Blueprint](scripts/deploy_agent.py)              | [0x187FE3505e56f4dA67b06564F03575cC15bE2B4d](https://arbiscan.io/address/0x187FE3505e56f4dA67b06564F03575cC15bE2B4d)  |

### Testnet Deployment Steps

1. Deploy `Agent` blueprint to Arbitrum

   ```bash
   $ ape run deploy_agent --network https://goerli-rollup.arbitrum.io/rpc
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
| [Agent Blueprint](scripts/deploy_agent.py)              | [0xC5fd5D3b06a8ef50b911972CA313E4d327F7c0aC](https://optimistic.etherscan.io/address/0xc5fd5d3b06a8ef50b911972ca313e4d327f7c0ac) |

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

| Name                                                        | Address                                                                                                               |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [L1 Broadcaster](contracts/optimism/OptimismBroadcaster.vy) | [0xcb843280c5037acfa67b8d4adc71484ced7c48c9](https://etherscan.io/address/0xcb843280c5037acfa67b8d4adc71484ced7c48c9) |
| [L2 Relayer](contracts/optimism/OptimismRelayer.vy)         | [0xCb843280C5037ACfA67b8D4aDC71484ceD7C48C9](https://basescan.org/address/0xCb843280C5037ACfA67b8D4aDC71484ceD7C48C9) |
| [L2 Ownership Agent](contracts/Agent.vy)                    | [0x2c163fe0f079d138b9c04f780d735289344C8B80](https://basescan.org/address/0x2c163fe0f079d138b9c04f780d735289344C8B80) |
| [L2 Parameter Agent](contracts/Agent.vy)                    | [0x7Ea4B72f04D8B02994F4EdB171Ce5F56eEdF457F](https://basescan.org/address/0x7Ea4B72f04D8B02994F4EdB171Ce5F56eEdF457F) |
| [L2 Emergency Agent](contracts/Agent.vy)                    | [0x95F0f720CAdDED982E6998b3390E6D3788c2CE5C](https://basescan.org/address/0x95F0f720CAdDED982E6998b3390E6D3788c2CE5C) |
| [L2 Vault](contracts/Vault.vy)                              | [0xA4c0eA0fb8eb652e11C8123E589197E18Ca78AA8](https://basescan.org/address/0xA4c0eA0fb8eb652e11C8123E589197E18Ca78AA8) |
| [Agent Blueprint](scripts/deploy_agent.py)              | [0xF3BC9E5fA891977DCa765ff52E8f22A1F7d49c1f](https://basescan.org/address/0xF3BC9E5fA891977DCa765ff52E8f22A1F7d49c1f) |

## Mantle

### Mainnet Deployment Addresses

| Name                                                        | Address                                                                                                                      |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| [L1 Broadcaster](contracts/optimism/OptimismBroadcaster.vy) | [0xb50b9a0d8a4ed8115fe174f300465ea4686d86df](https://etherscan.io/address/0xb50b9a0d8a4ed8115fe174f300465ea4686d86df)        |
| [L2 Relayer](contracts/optimism/OptimismRelayer.vy)         | [0xB50B9a0D8A4ED8115Fe174F300465Ea4686d86Df](https://explorer.mantle.xyz/address/0xB50B9a0D8A4ED8115Fe174F300465Ea4686d86Df) |
| [L2 Ownership Agent](contracts/Agent.vy)                    | [0xfe87a6cdca1eeb90987c6a196a1c5f5c76f5f2b0](https://explorer.mantle.xyz/address/0xfe87a6cdca1eeb90987c6a196a1c5f5c76f5f2b0) |
| [L2 Parameter Agent](contracts/Agent.vy)                    | [0x024d362f7aa162d8591304016fd60a209efc527e](https://explorer.mantle.xyz/address/0x024d362f7aa162d8591304016fd60a209efc527e) |
| [L2 Emergency Agent](contracts/Agent.vy)                    | [0x4339b53cf7f6eec1a997ceea81165e45c1244429](https://explorer.mantle.xyz/address/0x4339b53cf7f6eec1a997ceea81165e45c1244429) |
| [L2 Vault](contracts/Vault.vy)                              | [0x77A214bd4ee3650e5608339BBbE04b09f5546ECF](https://explorer.mantle.xyz/address/0x77A214bd4ee3650e5608339BBbE04b09f5546ECF) |
| [Agent Blueprint](scripts/deploy_agent.py)              | [0x5EF72230578b3e399E6C6F4F6360edF95e83BBfd](https://explorer.mantle.xyz/address/0x5EF72230578b3e399E6C6F4F6360edF95e83BBfd) |

## Avalanche

### Mainnet Deployment Addresses

| Name                                           | Address                                                                                                               |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [Broadcaster](contracts/xyz/XYZBroadcaster.vy) | [0x5786696bB5bE7fCDb9997E7f89355d9e97FF8d89](https://etherscan.io/address/0x5786696bB5bE7fCDb9997E7f89355d9e97FF8d89) |
| [Relayer](contracts/xyz/XYZRelayer.vy)         | [0x3895064FD74a86542206C4c39eb1bf14BB9aF9a6](https://snowtrace.io/address/0x3895064FD74a86542206C4c39eb1bf14BB9aF9a6) |
| [Ownership Agent](contracts/Agent.vy)          | [0xeD953C2849785A8AEd7bC2ee8cf5fdE776E1Dc07](https://snowtrace.io/address/0xeD953C2849785A8AEd7bC2ee8cf5fdE776E1Dc07) |
| [Parameter Agent](contracts/Agent.vy)          | [0x33F9A2F3B85e7D4Ff4f9286a9a8525060100D855](https://snowtrace.io/address/0x33F9A2F3B85e7D4Ff4f9286a9a8525060100D855) |
| [Emergency Agent](contracts/Agent.vy)          | [0x1309DB123020F0533aFAfaF11D26286d5871bEB0](https://snowtrace.io/address/0x1309DB123020F0533aFAfaF11D26286d5871bEB0) |
| [Vault](contracts/Vault.vy)                    | [0xad422855ac8010f82F08696CA7750EfE061aa6D6](https://snowtrace.io/address/0xad422855ac8010f82F08696CA7750EfE061aa6D6) |
| [Agent Blueprint](scripts/deploy_agent.py) | [0x31d13B6e3e287F506D21bBED9eA4b169971DF3fe](https://snowtrace.io/address/0x31d13B6e3e287F506D21bBED9eA4b169971DF3fe) |

## Fantom

### Mainnet Deployment Addresses

| Name                                           | Address                                                                                                               |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [Broadcaster](contracts/xyz/XYZBroadcaster.vy) | [0x5786696bB5bE7fCDb9997E7f89355d9e97FF8d89](https://etherscan.io/address/0x5786696bB5bE7fCDb9997E7f89355d9e97FF8d89) |
| [Relayer](contracts/xyz/XYZRelayer.vy)         | [0x002599c7D4299A268b332B3240d60308f93C99eC](https://ftmscan.com/address/0x002599c7D4299A268b332B3240d60308f93C99eC) |
| [Ownership Agent](contracts/Agent.vy)          | [0xd62Ade30F740de7ef766008258B4b2F574A084F7](https://ftmscan.com/address/0xd62Ade30F740de7ef766008258B4b2F574A084F7) |
| [Parameter Agent](contracts/Agent.vy)          | [0x837814ba42c6f3B39f0A5060168F7027695DDAb1](https://ftmscan.com/address/0x837814ba42c6f3B39f0A5060168F7027695DDAb1) |
| [Emergency Agent](contracts/Agent.vy)          | [0x42113C6818ACb87ca3CaFDbBc6a6ae396f1548E6](https://ftmscan.com/address/0x42113C6818ACb87ca3CaFDbBc6a6ae396f1548E6) |
| [Vault](contracts/Vault.vy)                    | [0x49C8De2D10C9A56DD9A59ab5Ca1216111276394C](https://ftmscan.com/address/0x49C8De2D10C9A56DD9A59ab5Ca1216111276394C) |
| [Agent Blueprint](scripts/deploy_agent.py) | [0x0732539C8aD556594FDa6A50fA8E976cA6D514B9](https://ftmscan.com/address/0x0732539C8aD556594FDa6A50fA8E976cA6D514B9) |

## Binance Smart Chain

### Mainnet Deployment Addresses

| Name                                           | Address                                                                                                               |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [Broadcaster](contracts/xyz/XYZBroadcaster.vy) | [0x5786696bB5bE7fCDb9997E7f89355d9e97FF8d89](https://etherscan.io/address/0x5786696bB5bE7fCDb9997E7f89355d9e97FF8d89) |
| [Relayer](contracts/xyz/XYZRelayer.vy)         | [0x37b6d6d425438a9f8e40C8B4c06c10560967b678](https://bscscan.com/address/0x37b6d6d425438a9f8e40C8B4c06c10560967b678) |
| [Ownership Agent](contracts/Agent.vy)          | [0xC97E2328c5701572C0DFB199b9f860d6ccD74199](https://bscscan.com/address/0xC97E2328c5701572C0DFB199b9f860d6ccD74199) |
| [Parameter Agent](contracts/Agent.vy)          | [0x618a38a556B66FdDdcB5495Be412Df911D18eA1d](https://bscscan.com/address/0x618a38a556B66FdDdcB5495Be412Df911D18eA1d) |
| [Emergency Agent](contracts/Agent.vy)          | [0xC940CE179f1F1bdC1EA1c02A2d0481bfD84C3280](https://bscscan.com/address/0xC940CE179f1F1bdC1EA1c02A2d0481bfD84C3280) |
| [Vault](contracts/Vault.vy)                    | [0x44C927BacD65da570cB1F0A2F625367049525022](https://bscscan.com/address/0x44C927BacD65da570cB1F0A2F625367049525022) |
| [Agent Blueprint](scripts/deploy_agent.py) | [0x3D09c5D6AE6e45d01C560342E11ef355C2763F01](https://bscscan.com/address/0x3D09c5D6AE6e45d01C560342E11ef355C2763F01) |

## Kava

### Mainnet Deployment Addresses

| Name                                           | Address                                                                                                               |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [Broadcaster](contracts/xyz/XYZBroadcaster.vy) | [0x5786696bB5bE7fCDb9997E7f89355d9e97FF8d89](https://etherscan.io/address/0x5786696bB5bE7fCDb9997E7f89355d9e97FF8d89) |
| [Relayer](contracts/xyz/XYZRelayer.vy)         | [0xA5961898870943c68037F6848d2D866Ed2016bcB](https://kavascan.com/address/0xA5961898870943c68037F6848d2D866Ed2016bcB) |
| [Ownership Agent](contracts/Agent.vy)          | [0xeC6a886148B38C233B07cc6732142dccaBF1051D](https://kavascan.com/address/0xeC6a886148B38C233B07cc6732142dccaBF1051D) |
| [Parameter Agent](contracts/Agent.vy)          | [0x6e53131F68a034873b6bFA15502aF094Ef0c5854](https://kavascan.com/address/0x6e53131F68a034873b6bFA15502aF094Ef0c5854) |
| [Emergency Agent](contracts/Agent.vy)          | [0xA177D2bd2BD723878bD95982c0855291953f74C9](https://kavascan.com/address/0xA177D2bd2BD723878bD95982c0855291953f74C9) |
| [Agent Blueprint](scripts/deploy_agent.py) | [0xC0AE3B85060530384647E9F3D63C9e1F53231f68](https://kavascan.com/address/0xC0AE3B85060530384647E9F3D63C9e1F53231f68) |

## Polygon

### Mainnet Deployment Addresses

| Name                                           | Address                                                                                                               |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [Broadcaster](contracts/xyz/XYZBroadcaster.vy) | [0x91e95f16f7F1b988391A869771Ffb50Df4ceBDF7](https://etherscan.io/address/0x91e95f16f7F1b988391A869771Ffb50Df4ceBDF7) |
| [Relayer](contracts/xyz/XYZRelayer.vy)         | [0x91e95f16f7F1b988391A869771Ffb50Df4ceBDF7](https://polygonscan.com/address/0x91e95f16f7F1b988391A869771Ffb50Df4ceBDF7) |
| [Ownership Agent](contracts/Agent.vy)          | [0x8cB05bFEd65b522a7cF98d590F1711A9Db43af71](https://polygonscan.com/address/0x8cB05bFEd65b522a7cF98d590F1711A9Db43af71) |
| [Parameter Agent](contracts/Agent.vy)          | [0x3CF7c393519ea55D1E1F2c55a6395be63b1A9F9C](https://polygonscan.com/address/0x3CF7c393519ea55D1E1F2c55a6395be63b1A9F9C) |
| [Emergency Agent](contracts/Agent.vy)          | [0x9FD6E204e08867170ddE54a8374083fF592eBD3E](https://polygonscan.com/address/0x9FD6E204e08867170ddE54a8374083fF592eBD3E) |
| [Agent Blueprint](scripts/deploy_agent.py) | [0x1fE46Da288A55aAf32facc6D182fB1933B22c2E9](https://polygonscan.com/address/0x1fE46Da288A55aAf32facc6D182fB1933B22c2E9) |
