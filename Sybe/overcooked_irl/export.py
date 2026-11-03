"""Turning states/trajectories into image files (PNG frames, GIF)."""
from pathlib import Path

import imageio
from overcooked_ai_py.mdp.overcooked_env import OvercookedEnv
from overcooked_ai_py.mdp.overcooked_mdp import OvercookedGridworld
from overcooked_ai_py.visualization.state_visualizer import StateVisualizer

def stitch_gif(frames_dir, gif_name="0trajectory.gif", fps=10):
    """Combine the numbered PNGs in frames_dir into a GIF."""
    frames_dir = Path(frames_dir)
    frame_files = sorted(
        frames_dir.glob("*.png"),
        key=lambda p: int("".join(c for c in p.stem if c.isdigit())),
    )
    images = [imageio.imread(f) for f in frame_files]
    gif_path = frames_dir / gif_name
    imageio.mimsave(gif_path, images, duration=1 / fps, loop=0)
    print(f"GIF saved to: {gif_path}")
    return gif_path


def save_gif(trajectory, out_dir, fps=10):
    """Frames + stitching in one call."""
    StateVisualizer().display_rendered_trajectory(
        trajectories=trajectory,
        img_directory_path=str(out_dir),
        ipython_display=False,
    )
    return stitch_gif(out_dir, fps=fps)