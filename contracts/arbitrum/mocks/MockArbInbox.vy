# @version 0.3.7


submission_fee: uint256

count: public(uint256)
data: public(Bytes[2**32])


@payable
@external
def unsafeCreateRetryableTicket(
    _to: address,
    _l2_call_value: uint256,
    _submission_cost: uint256,
    _excess_fee_refund_address: address,
    _call_value_refund_address: address,
    _gas_limit: uint256,
    _max_fee_per_gas: uint256,
    _data: Bytes[2**24],
):
    self.count += 1
    self.data = _data


@view
@external
def calculateRetryableSubmissionFee(_data_length: uint256, _base_fee: uint256 = 0) -> uint256:
    return self.submission_fee


@external
def _set_submission_fee(_fee: uint256):
    self.submission_fee = _fee
