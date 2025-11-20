import pygame # type: ignore
import sys
from constants import *
from logger import log_state , log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from circleshape import *


#Game loop
def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    AsteroidField()
    Shot.containers = (shots, updatable, drawable)

    #colors for time
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Font for displaying time
    font = pygame.font.Font(None, 50)

    score = 0
    
    while True:
        log_state() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        dt = clock.tick(60) / 1000

        milliseconds = pygame.time.get_ticks()
        seconds = milliseconds / 1000
        time_text = font.render(f"Time: {int(seconds)}s", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)

        screen.fill(BLACK)
 
        updatable.update(dt) 
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                print(f"Final Score = {score}")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    score += 1
                    shot.kill()
        
        for sprite in drawable:
            sprite.draw(screen)

        screen.blit(time_text, (SCREEN_WIDTH - 200 , SCREEN_HEIGHT - 55))
        screen.blit(score_text, (SCREEN_WIDTH - 200 , SCREEN_HEIGHT - 100))

        pygame.display.flip()


if __name__ == "__main__":
    main()
