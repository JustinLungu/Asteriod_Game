from asteriod_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteriod_game.rl.policy import LoadedPolicy
import argparse
import os
import pygame

LABEL_FONT_SIZE = 28
LABEL_MARGIN = 10

def play_watch(policy, screen, clock, label):
    env = policy.make_env()
    observation, _ = env.reset()
    game = env.unwrapped
    font = pygame.font.Font(None, LABEL_FONT_SIZE)
    label_surface = font.render(label, True, "white")
    label_rect = label_surface.get_rect(bottomleft=(LABEL_MARGIN, SCREEN_HEIGHT - LABEL_MARGIN))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", game.score.points
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu", game.score.points

        observation, reward, terminated, truncated, info = env.step(policy.act(observation))
        if terminated or truncated:
            return "over", game.score.points

        screen.fill("black")
        for drawing in game.drawable:
            drawing.draw(screen)
        screen.blit(label_surface, label_rect)
        pygame.display.flip()
        clock.tick(60)

def main():
    parser = argparse.ArgumentParser(description="Watch a trained model play one game")
    parser.add_argument("--model", required=True, help="path to a final or checkpoint .zip")
    args = parser.parse_args()

    policy = LoadedPolicy(args.model)
    label = policy.algo + " " + os.path.basename(args.model)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    result, points = play_watch(policy, screen, clock, label)
    print("Watched " + label + " -> " + result + ", score " + str(points))

if __name__ == "__main__":
    main()
