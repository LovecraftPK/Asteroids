import pygame  # type: ignore
from constants import *
import sys
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from circleshape import *


def create_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    AsteroidField()
    Shot.containers = (shots, updatable, drawable)

    score = 0
    start_time = pygame.time.get_ticks()

    return updatable, drawable, asteroids, shots, player, score, start_time


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.Font(None, 50)
    big_font = pygame.font.Font(None, 80)

    updatable, drawable, asteroids, shots, player, score, start_time = create_game()
    game_over = False
    title_screen = True 

    final_score = 0
    final_time = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if title_screen and event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):

                    score = 0
                    start_time = pygame.time.get_ticks()
                    title_screen = False

            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    updatable, drawable, asteroids, shots, player, score, start_time = create_game()

                    final_score = 0
                    final_time = 0
                    game_over = False
                    title_screen = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        dt = clock.tick(60) / 1000.0
        screen.fill(BLACK)

        if title_screen:

            updatable.update(dt)
            for sprite in drawable:
                sprite.draw(screen)

            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, 128))
            screen.blit(fade_surface, (0, 0))

            title_text = big_font.render("ASTEROIDS", True, WHITE)
            subtitle_text = font.render("A Pygame Space Adventure", True, WHITE)
            movekey_text = font.render("WASD or Arrow Keys to Move. SPACE to shoot.", True, WHITE)


            blink = (pygame.time.get_ticks() // 500) % 3 == 0
            press_text = font.render("Press ", True, WHITE)
            space_text = font.render("SPACE", True, WHITE if blink else (150, 150, 150))
            to_start_text = font.render(" when ready", True, WHITE)

            total_width = press_text.get_width() + space_text.get_width() + to_start_text.get_width()
            y_pos = SCREEN_HEIGHT / 2 + 50
            x_start = SCREEN_WIDTH / 2 - total_width / 2

            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 300)))
            screen.blit(subtitle_text, subtitle_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 240)))
            screen.blit(movekey_text, movekey_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 0)))

            screen.blit(press_text, (x_start, y_pos))
            screen.blit(space_text, (x_start + press_text.get_width(), y_pos))
            screen.blit(to_start_text, (x_start + press_text.get_width() + space_text.get_width(), y_pos))

        elif not game_over:
            milliseconds = pygame.time.get_ticks() - start_time
            seconds = milliseconds / 1000

            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    print("Game over!")
                    print(f"Final Score = {score}")
                    game_over = True

                    final_score = score
                    final_time = int(seconds)

                    break

            if not game_over:
                for asteroid in asteroids:
                    for shot in shots:
                        if asteroid.collides_with(shot):
                            log_event("asteroid_shot")
                            asteroid.split()
                            score += 1
                            shot.kill()

            for sprite in drawable:
                sprite.draw(screen)

            time_text = font.render(f"Time: {int(seconds)}s", True, WHITE)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(time_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 55))
            screen.blit(score_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))

        else:
            blink = (pygame.time.get_ticks() // 500) % 5 == 0
            game_over_text = font.render("GAME OVER", True, (150, 150, 150) if blink else WHITE)
            restart_text = font.render("Press R to Restart", True, WHITE)
            quit_text = font.render("Press Q to Quit", True, WHITE)

            final_score_text = font.render(f"Final Score: {final_score}", True, WHITE)
            final_time_text = font.render(f"Time: {final_time}s", True, WHITE)

            center_x = SCREEN_WIDTH / 2
            center_y = SCREEN_HEIGHT / 2

            screen.blit(game_over_text, game_over_text.get_rect(center=(center_x, center_y - 80)))
            screen.blit(final_score_text, final_score_text.get_rect(center=(center_x, center_y - 20)))
            screen.blit(final_time_text, final_time_text.get_rect(center=(center_x, center_y + 20)))
            screen.blit(restart_text, restart_text.get_rect(center=(center_x, center_y + 70)))
            screen.blit(quit_text, quit_text.get_rect(center=(center_x, center_y + 120)))


        pygame.display.flip()


if __name__ == "__main__":
    main()
