from constants import SCREEN_HEIGHT , SCREEN_WIDTH

screen_width = SCREEN_WIDTH
screen_height = SCREEN_HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font for displaying time
font = pygame.font.Font(None, 74)

milliseconds = pygame.time.get_ticks()
seconds = milliseconds / 1000
time_text = font.render(f"Time: {int(seconds)}s", True, WHITE)
screen.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, 
                            screen_height // 2 - time_text.get_height() // 2))