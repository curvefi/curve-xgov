## Requirements
- [Broadcaster](https://github.com/curvefi/curve-xgov/blob/feat/taiko/contracts/Broadcaster.vy) on Ethereum that forwards messages from DAO to bridge.
- [Relayer](https://github.com/curvefi/curve-xgov/blob/feat/taiko/contracts/Relayer.vy) on your network that checks the sender and relays messages to agents(mirrors of Curve DAO entities).
It should be safe from blocking the contracts and any external access to execution.

## Examples
There is a version in vyper 0.4.0 with module imports, but there are issues with running tests: https://github.com/curvefi/curve-xgov/tree/feat/taiko/contracts/taiko

Vyper 0.3.10 version example: https://github.com/curvefi/curve-xgov/tree/master/contracts
