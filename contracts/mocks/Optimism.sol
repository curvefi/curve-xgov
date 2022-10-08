pragma solidity >=0.8.0;

contract CrossDomainMessenger {
    function sendMessage(
        address target,
        bytes calldata message,
        uint32 gasLimit
    ) external {}
}

contract CanonicalTransactionChain {
    function enqueueL2GasPrepaid() external view returns (uint256) {
        return 1_920_000;
    }
}
