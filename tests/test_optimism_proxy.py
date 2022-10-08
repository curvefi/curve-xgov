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
