"""Entry point: simulate a game.

Run from anywhere:
    python Sybe/main.py                             # simulate a game
    python Sybe/main.py --save_frames               # save frames
    python Sybe/main.py --viewer                    # show pygame viewer
"""
import argparse

from overcooked_irl.agent_factory import create_agent_pair
import config
from overcooked_irl.export import save_frames, save_gif
from overcooked_irl.simulation import random_agent_pair, run_game
from overcooked_irl.viewer import run_viewer
from overcooked_irl.paths import next_episode_dir, next_run_dir
from overcooked_ai_py.visualization.state_visualizer import StateVisualizer # TODO Remove StateVisualizer logic from main?

def parse_args(): 
    p = argparse.ArgumentParser(description="Overcooked simulation + visualization")
    p.add_argument("--layout", default=config.LAYOUT_NAME)
    p.add_argument("--horizon", type=int, default=config.HORIZON)
    p.add_argument(
        "--experiment",
        choices=config.EXPERIMENTS,
        default="random",
        help="Experiment configuration",
    )
    p.add_argument("--save_frames", action="store_true", help="saves images of every timestep")
    p.add_argument("--save_gif", action="store_true", help="save images AND a gif")
    p.add_argument("--viewer", action="store_true", help="show the pygame viewer")
    return p.parse_args()


def main():
    args = parse_args()
    
    run_dir = config.BASE_DIR / "experiments" / args.experiment / "run_0001" 
    # run_dir = next_run_dir(args.experiment)

    agent_pair = create_agent_pair(args.experiment, args.experiment)
    
    episode = run_game(agent_pair, args.layout, args.horizon)
    episode_dir = run_dir / "episode_000001"
    # episode_dir = next_episode_dir(run_dir)

    if args.save_gif:
        frames_dir = episode_dir / "frames"
        save_gif(episode.trajectories, frames_dir, fps=config.GIF_FPS)
    elif args.save_frames:
        save_frames(episode.trajectories, frames_dir)
    
    if args.viewer:
        run_viewer(episode)
        
    

if __name__ == "__main__":
    main()