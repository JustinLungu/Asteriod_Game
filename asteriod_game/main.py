from asteriod_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteriod_game.logger import log_state, log_event
from asteriod_game.game.actions import Actions
from asteriod_game.leaderboard import Leaderboard
from asteriod_game.ui.menu import Menu
from asteriod_game.ui.controls_screen import ControlsScreen
from asteriod_game.rl.env import GameEnv
import pygame
import sys


def actions_from_keyboard():
    keys = pygame.key.get_pressed()
    return Actions(
        rotate_left=keys[pygame.K_a],
        rotate_right=keys[pygame.K_d],
        thrust_forward=keys[pygame.K_w],
        thrust_backward=keys[pygame.K_s],
        shoot=keys[pygame.K_SPACE],
    )


def actions_to_array(actions):
    return [
        int(actions.rotate_left),
        int(actions.rotate_right),
        int(actions.thrust_forward),
        int(actions.thrust_backward),
        int(actions.shoot),
    ]


def end_game(reason, score, leaderboard):
    log_event(reason, score=score.points)
    print("Game over!")
    print("Final score: " + str(score.points))

    if leaderboard.is_high_score(score.points):
        print("New high score!")
    leaderboard.submit(score.points)
    print("Leaderboard: " + str(leaderboard.scores))

    sys.exit()


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

    while True:
        action = menu.run(clock)
        if action == "quit":
            return
        if action == "controls":
            if controls_screen.run(clock) == "quit":
                return
            continue
        if action == "start":
            break

    env = GameEnv()
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
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return

        actions = actions_from_keyboard()
        observation, reward, terminated, truncated, info = env.step(actions_to_array(actions))

        for event_type in info["events"]:
            log_event(event_type)

        if terminated:
            end_game("player_hit", env.score, leaderboard)
        if truncated:
            end_game("time_limit_reached", env.score, leaderboard)

        screen.fill("black")
        for drawing in drawable:
            drawing.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
