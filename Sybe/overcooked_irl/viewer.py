"""Interactive pygame trajectory viewer."""
import pygame
from overcooked_ai_py.visualization.state_visualizer import StateVisualizer

import config as config


def run_viewer(trajectory, fps=config.VIEWER_FPS):
    pygame.init()
    pygame.key.set_repeat(500, 30)  # hold a key: 0.5s delay, then ~33 steps/s

    viz = StateVisualizer()
    font = pygame.font.SysFont(None, 24)
    n_steps = len(trajectory.states)

    def render(t):
        return viz.render_state(trajectory.states[t], trajectory.grid)

    def draw_hud(screen, t):
        current_score = int(sum(trajectory.rewards[:t])) if t > 0 else 0
        time_left = max(0, trajectory.horizon - t)
        screen.blit(font.render(f"TIME LEFT: {time_left}", True, (255, 255, 255)), (20, 10))
        screen.blit(
            font.render(f"SCORE: {current_score} / {trajectory.total_return}", True, (255, 255, 255)),
            (20, 35),
        )

    width, height = render(0).get_size()
    screen = pygame.display.set_mode((width, height + config.HUD_HEIGHT))
    clock = pygame.time.Clock()

    t, playing, running = 0, False, True
    game_surface, rendered_t = render(0), 0

    print("\n--- CONTROLS ---")
    print("Right/Left : step forward/backward (hold to repeat)")
    print("Space      : play / pause")
    print("Esc        : quit\n")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RIGHT:
                    t, playing = min(t + 1, n_steps - 1), False
                elif event.key == pygame.K_LEFT:
                    t, playing = max(t - 1, 0), False
                elif event.key == pygame.K_SPACE:
                    playing = not playing

        if playing:
            if t < n_steps - 1:
                t += 1
            else:
                playing = False

        if t != rendered_t:  # only re-render when the frame changes
            game_surface, rendered_t = render(t), t

        screen.fill(config.BG_COLOR)
        draw_hud(screen, t)
        screen.blit(game_surface, (0, config.HUD_HEIGHT))
        pygame.display.set_caption(
            f"Replay - Step {t}/{n_steps - 1} {'[PLAYING]' if playing else '[PAUSED]'}"
        )
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()