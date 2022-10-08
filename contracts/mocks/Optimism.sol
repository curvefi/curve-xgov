pragma solidity >=0.8.0;

contract CrossDomainMessenger {
    uint256 public call_count;

    function sendMessage(
        address target,
        bytes calldata message,
        uint32 gasLimit
    ) external {
        call_count += 1;
    }
}

contract CanonicalTransactionChain {
    function enqueueL2GasPrepaid() external view returns (uint256) {
        return 1_920_000;
    }
}
