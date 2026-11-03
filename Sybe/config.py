"""Central place for constants and paths."""
from pathlib import Path

LAYOUT_NAME = "cramped_room"
HORIZON = 400

VIEWER_FPS = 30
GIF_FPS = 10
HUD_HEIGHT = 60
BG_COLOR = (153, 102, 0)

# Paths are relative to this file, so scripts work from any working directory
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "experiments" / "random" / "run_000001" / "renders" / "episode_000003"