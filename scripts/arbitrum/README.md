## Initial Deploy
Set up first contracts and move ownership to DAO.

0. If no broadcaster deployed:
```bash
ape run arbitrum deploy_broadcaster --network <ethereum>
```

3. Set `Relayer` in `Broadcaster` 
```bash
ape run arbitrum set_destination --chain_id <destination chain ID> --relayer <relayer from destination deployment> --vault <vault from destination deployment> --network <ethereum>
```

4. Uncomment correct admins and set
```bash
ape run arbitrum set_destination --network <ethereum>
```

## Deploy

1. Deploy `Agent` blueprint
```bash
ape run deploy_agent --network <destination network>
```

2. Deploy `Relayer` and `Vault`
```bash
ape run arbitrum deploy_destination --blueprint <AGENT_BLUEPRINT_ADDRESS> --network <destination network>
```

3. Create a vote to set destination data as in [set_destination](set_destination.py)
