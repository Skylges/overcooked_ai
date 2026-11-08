from overcooked_ai_py.agents.agent import AgentPair, RandomAgent

def create_agent(agent_type):
    if agent_type == "random":
        return RandomAgent()

    elif agent_type == "ddqn":
        raise NotImplementedError

    elif agent_type == "curiosity":
        raise NotImplementedError

    else:
        raise ValueError(f"Unknown agent type: {agent_type}")


def create_agent_pair(agent1_type, agent2_type):
    agent1 = create_agent(agent1_type)
    agent2 = create_agent(agent2_type)

    return AgentPair(agent1, agent2)