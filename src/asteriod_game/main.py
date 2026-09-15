from asteriod_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteriod_game.game.constants import SCORE_PER_ASTEROID_HIT
from asteriod_game.logger import log_state, log_event
from asteriod_game.game.player import Player
from asteriod_game.game.asteroid import Asteroid
from asteriod_game.game.asteroidfield import AsteroidField
from asteriod_game.game.shot import Shot
from asteriod_game.game.score import Score
from asteriod_game.leaderboard import Leaderboard
from asteriod_game.ui.menu import Menu
from asteriod_game.ui.controls_screen import ControlsScreen
import pygame
import sys


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
