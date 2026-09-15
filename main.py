from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score import Score
from leaderboard import Leaderboard
from menu import Menu
import pygame
import sys


def main():
    print("Starting Asteroids with pygame version: " + pygame.version.ver)
    print("Screen width: " + str(SCREEN_WIDTH))
    print("Screen height: " + str(SCREEN_HEIGHT))

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    menu = Menu(screen)
    if not menu.run(clock):
        return

    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()


    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Shot.containers = (shots, updatable, drawable)

    Score.containers = (updatable, drawable)
    score = Score()

    leaderboard = Leaderboard()


    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
            
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit", score=score.points)
                print("Game over!")
                print("Final score: " + str(score.points))

                if leaderboard.is_high_score(score.points):
                    print("New high score!")
                leaderboard.submit(score.points)
                print("Leaderboard: " + str(leaderboard.scores))

                sys.exit()
            
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    score.add_points(SCORE_PER_ASTEROID_HIT)
        
        screen.fill("black")
        for drawing in drawable:
            drawing.draw(screen)
            
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0

        
        
        


if __name__ == "__main__":
    main()
