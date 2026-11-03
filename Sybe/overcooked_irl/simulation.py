"""Running games and packaging the results. No rendering or UI in here."""
from dataclasses import dataclass

from overcooked_ai_py.agents.agent import AgentPair, RandomAgent
from overcooked_ai_py.agents.benchmarking import AgentEvaluator


@dataclass
class Episode:
    """Data from one finished game"""
    trajectories: dict   # raw output of evaluate_agent_pair (needed by StateVisualizer)
    states: list         # OvercookedState per timestep
    rewards: list        # sparse reward per timestep
    grid: list           # terrain matrix
    total_return: int
    horizon: int

    @classmethod
    def from_trajectories(cls, trajectories, evaluator, game_idx=0):
        return cls(
            trajectories=trajectories,
            states=trajectories["ep_states"][game_idx],
            rewards=trajectories["ep_rewards"][game_idx],
            grid=evaluator.env.mdp.terrain_mtx,
            total_return=int(trajectories["ep_returns"][game_idx]),
            horizon=evaluator.env.horizon,
        )


def make_evaluator(layout_name, horizon):
    return AgentEvaluator.from_layout_name(
        mdp_params={"layout_name": layout_name},
        env_params={"horizon": horizon},
    )


def random_agent_pair():
    return AgentPair(RandomAgent(), RandomAgent())


def run_game(agent_pair, layout_name, horizon):
    """Play one game with any AgentPair"""
    print(f"Simulating '{layout_name}' for {horizon} steps...")
    evaluator = make_evaluator(layout_name, horizon)
    trajectories = evaluator.evaluate_agent_pair(agent_pair, num_games=1)
    return Episode.from_trajectories(trajectories, evaluator)