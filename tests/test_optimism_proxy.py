import eth_abi

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def test_constructor(alice, project, cross_domain_messenger, canonical_transaction_chain):
    proxy = project.L1OptimismProxy.deploy(
        (alice, alice, alice), cross_domain_messenger, canonical_transaction_chain, sender=alice
    )

    assert proxy.admins() == tuple([alice] * 3)
    assert proxy.future_admins() == tuple([ZERO_ADDRESS] * 3)
    assert proxy.messenger() == cross_domain_messenger
    assert proxy.messenger() == cross_domain_messenger
    assert proxy.transaction_chain() == canonical_transaction_chain


def test_send_message_success(
    alice, l1_optimism_proxy, cross_domain_messenger, canonical_transaction_chain
):
    tx = l1_optimism_proxy.send_message(alice, b"", sender=alice)

    assert cross_domain_messenger.call_count() == 1
    target = next(filter(lambda frame: frame.op == "STATICCALL", tx.trace)).stack[-2]
    assert eth_abi.decode_single("address", target) == canonical_transaction_chain
