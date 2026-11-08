import config

def next_run_dir(experiment):
    """Create and return experiments/<experiment>/run_XXXX"""
    if experiment not in config.EXPERIMENTS:
        raise ValueError(f"Unknown experiment: {experiment}. Must be one of {config.EXPERIMENTS}")
    exp_dir = config.BASE_DIR / "experiments" / experiment
    numbers = [int(p.name[4:]) for p in exp_dir.glob("run_*") if p.name[4:].isdigit()]
    run_dir = exp_dir / f"run_{max(numbers, default=0) + 1:04d}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

def next_episode_dir(run_dir):
    """Create and return experiments/<experiment>/run_XXXX/episode_XXXXXX"""
    numbers = [int(p.name[8:]) for p in run_dir.glob("episode_*") if p.name[8:].isdigit()]
    episode_dir = run_dir / f"episode_{max(numbers, default=0) + 1:06d}"
    episode_dir.mkdir(parents=True, exist_ok=True)
    return episode_dir