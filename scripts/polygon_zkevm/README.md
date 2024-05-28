## Deploy
1. Deploy `Agent` blueprint

   ```bash
   ape run deploy_agent --network <destination network>
   ```

2. Deploy `Relayer` and `Vault`

   ```bash
   ape run polygon_zkevm deploy --blueprint <AGENT_BLUEPRINT_ADDRESS> --network <destination network>
   ```

3. Deploy `Broadcaster`

   ```bash
   ape run polygon_zkevm deploy --network <origin network> --destination_chain_id <destination network chain ID>
   ```

## Claim message on destination chain
Save `depositCount` from PolygonZkEVMBridge.BridgeEvent to claim message on destination chain:
```bash
ape run polygon_zkevm claim_message --deposit_cnt <depositCount> --network <network>
```

Example:
```bash
ape run polygon_zkevm claim_message --deposit_cnt 189238 --network https://rpc.xlayer.tech 
```
