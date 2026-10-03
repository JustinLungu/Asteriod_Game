from asteriod_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WATCH_QUIT_EXIT_CODE
from asteriod_game.logger import log_state, log_event
from asteriod_game.game.actions import Actions
from asteriod_game.leaderboard import Leaderboard
from asteriod_game.ui.menu import Menu
from asteriod_game.ui.controls_screen import ControlsScreen
from asteriod_game.rl.env import GameEnv
from asteriod_game.rl.model_list import list_runs, list_stages
from asteriod_game.ui.model_picker import ModelPicker
import os
import subprocess
import sys
import pygame


def actions_from_keyboard():
    keys = pygame.key.get_pressed()
    return Actions(
        rotate_left=keys[pygame.K_a],
        rotate_right=keys[pygame.K_d],
        thrust_forward=keys[pygame.K_w],
        thrust_backward=keys[pygame.K_s],
        shoot=keys[pygame.K_SPACE],
    )


def end_game(reason, score, leaderboard):
    log_event(reason, score=score.points)
    print("Game over!")
    print("Final score: " + str(score.points))

    if leaderboard.is_high_score(score.points):
        print("New high score!")
    leaderboard.submit(score.points)
    print("Leaderboard: " + str(leaderboard.scores))


def watch_in_separate_process(model_path):
    pygame.display.quit()
    try:
        completed = subprocess.run([sys.executable, "-m", "asteriod_game.rl.watch", "--model", model_path])
    finally:
        pygame.display.init()
    return completed.returncode


def watch_ai(screen, clock):
    while True:
        run_dir = ModelPicker(screen, "Choose a trained run", list_runs()).run(clock)
        if run_dir == "quit":
            return "quit", screen
        if run_dir is None:
            return "menu", screen

        while True:
            model_path = ModelPicker(screen, "Choose a stage of this run", list_stages(run_dir)).run(clock)
            if model_path == "quit":
                return "quit", screen
            if model_path is None:
                break

            exit_code = watch_in_separate_process(model_path)
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            if exit_code == WATCH_QUIT_EXIT_CODE:
                return "quit", screen


def main():
    print("Starting Asteroids with pygame version: " + pygame.version.ver)
    print("Screen width: " + str(SCREEN_WIDTH))
    print("Screen height: " + str(SCREEN_HEIGHT))

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    leaderboard = Leaderboard()
    menu = Menu(screen, leaderboard)
    controls_screen = ControlsScreen(screen)

    env = GameEnv()

    while True:
        action = menu.run(clock)
        if action == "quit":
            return
        if action == "controls":
            if controls_screen.run(clock) == "quit":
                return
            continue
        if action == "start":
            if play_game(env, screen, clock, leaderboard) == "quit":
                return
        if action == "watch":
            result, screen = watch_ai(screen, clock)
            menu = Menu(screen, leaderboard)
            controls_screen = ControlsScreen(screen)
            if result == "quit":
                return


def play_game(env, screen, clock, leaderboard):
    env.reset()

    updatable = env.updatable
    drawable = env.drawable
    asteroids = env.asteroids
    shots = env.shots
    player = env.player
    asteroid_field = env.asteroid_field
    score = env.score
    timer = env.timer

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "quit"

        actions = actions_from_keyboard()
        observation, reward, terminated, truncated, info = env.step(actions.to_array())

        for event_type in info["events"]:
            log_event(event_type)

        if terminated:
            end_game("player_hit", env.score, leaderboard)
            return "over"
        if truncated:
            end_game("time_limit_reached", env.score, leaderboard)
            return "over"

        screen.fill("black")
        for drawing in drawable:
            drawing.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
