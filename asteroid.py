import pygame # type: ignore
from circleshape import *
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.radius = radius

    def draw(self, screen):
        white = (255,255,255)
        pygame.draw.circle(screen, white, self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt