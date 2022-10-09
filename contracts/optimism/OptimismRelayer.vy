# @version 0.3.7
"""
@title Optimism Relayer
@author CurveFi
"""


interface IAgent:
    def execute(_messages: DynArray[Message, MAX_MESSAGES]): nonpayable

interface IMessenger:
    def xDomainMessageSender() -> address: view


enum Agent:
    OWNERSHIP
    PARAMETER
    EMERGENCY


struct Message:
    target: address
    data: Bytes[MAX_BYTES]


MAX_BYTES: constant(uint256) = 1000
MAX_MESSAGES: constant(uint256) = 8

CODE_OFFSET: constant(uint256) = 3


MESSENGER: public(immutable(address))

OWNERSHIP_AGENT: public(immutable(address))
PARAMETER_AGENT: public(immutable(address))
EMERGENCY_AGENT: public(immutable(address))


agent: HashMap[Agent, address]


@external
def __init__(_agent_blueprint: address, _messenger: address):
    MESSENGER = _messenger

    OWNERSHIP_AGENT = create_from_blueprint(_agent_blueprint, code_offset=CODE_OFFSET)
    PARAMETER_AGENT = create_from_blueprint(_agent_blueprint, code_offset=CODE_OFFSET)
    EMERGENCY_AGENT = create_from_blueprint(_agent_blueprint, code_offset=CODE_OFFSET)

    self.agent[Agent.OWNERSHIP] = OWNERSHIP_AGENT
    self.agent[Agent.PARAMETER] = PARAMETER_AGENT
    self.agent[Agent.EMERGENCY] = EMERGENCY_AGENT


@external
def relay(_agent: Agent, _messages: DynArray[Message, MAX_MESSAGES]):
    """
    @notice Receive messages for an agent and relay them.
    @param _agent The agent to relay messages to.
    @param _messages The sequence of messages to relay.
    """
    assert msg.sender == MESSENGER
    assert IMessenger(MESSENGER).xDomainMessageSender() == self

    IAgent(self.agent[_agent]).execute(_messages)
