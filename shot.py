import pygame # type: ignore
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, position):
        super().__init__(position.x, position.y, SHOT_RADIUS)
        self.radius = SHOT_RADIUS
        self.velocity = pygame.Vector2(0, 1)

    def draw(self, screen):
        white = (255,255,255)
        pygame.draw.circle(screen, white, self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt