"""Entry point: simulate a game.

Run from anywhere:
    python Sybe/main.py                             # simulate a game
    python Sybe/main.py --save_frames               # save frames
    python Sybe/main.py --viewer                    # show pygame viewer
"""
import argparse

import config
from overcooked_irl.export import save_gif
from overcooked_irl.simulation import random_agent_pair, run_game
from overcooked_irl.viewer import run_viewer
from overcooked_ai_py.visualization.state_visualizer import StateVisualizer

def parse_args(): 
    p = argparse.ArgumentParser(description="Overcooked simulation + visualization")
    p.add_argument("--layout", default=config.LAYOUT_NAME)
    p.add_argument("--horizon", type=int, default=config.HORIZON)
    p.add_argument("--save_frames", action="store_true", help="saves images of every timestep")
    p.add_argument("--save_gif", action="store_true", help="save images and a gif")
    p.add_argument("--viewer", action="store_true", help="show the pygame viewer")
    return p.parse_args()


def main():
    args = parse_args()

    episode = run_game(random_agent_pair(), args.layout, args.horizon)
    frames_dir = config.OUTPUT_DIR / "frames"

    if args.save_frames:
        StateVisualizer().display_rendered_trajectory(
            episode.trajectories,
            img_directory_path=str(frames_dir),
            ipython_display=False,
        )
    if args.save_gif:
        save_gif(episode.trajectories, frames_dir, fps=config.GIF_FPS)
    if args.viewer:
        run_viewer(episode)

        
    # TODO Do I want separate funcions or 
    """ agent_evaluator = AgentEvaluator.from_layout_name(
            mdp_params={"layout_name": layout_name},
            env_params={"horizon": horizon}
        )"""


if __name__ == "__main__":
    main()