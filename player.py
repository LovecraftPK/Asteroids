import pygame # type: ignore
from circleshape import *
from constants import *
from shot import *
import random

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.radius = PLAYER_RADIUS
        self.rotation = 0
        self.shot_counter = 0
        self.velocity = pygame.Vector2()
        self.thrust_particles = []

        # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        for p in self.thrust_particles:
            r = int(p["radius"])
            if r > 0:
                pygame.draw.circle(screen, "white", p["pos"], r)

        draw_object = self.triangle()
        white = (255,255,255)
        pygame.draw.polygon(screen, white, draw_object, LINE_WIDTH)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        self.rotation %= 360

    def update(self, dt):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        self.shot_counter -= dt

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)

        if keys[pygame.K_d] or keys[pygame.K_RIGHT] or mouse[1]:
            self.rotate(dt)

        thrust = 0

        if keys[pygame.K_w] or keys[pygame.K_UP] or mouse[0]:
            thrust += 1

        if keys[pygame.K_s] or keys[pygame.K_DOWN] or mouse[2]:
            thrust -= 1

        boosting = False
        if keys[pygame.K_LSHIFT]:
            thrust *= 2
            boosting = True

        if thrust != 0:
            self.accelerate(dt, thrust)

        if boosting and thrust > 0:
            self.spawn_thrust_particles()

        self.move(dt)
        self.update_particles(dt)

        if keys[pygame.K_SPACE]:
            self.shoot()
            boosting = True


    def accelerate(self, dt, thrust=1):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * thrust * dt

        max_speed = PLAYER_MAX_SPEED
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)        

    def move(self, dt,):
        self.position += self.velocity * dt
        Friction = 0.5
        self.velocity *= Friction ** dt
        self.wrap_around()

    def shoot(self):
        if self.shot_counter > 0:
            return
        else:

            self.shot_counter = PLAYER_SHOOT_COOLDOWN_SECONDS
            shot = Shot(self.position)
            shot.velocity = pygame.Vector2(0, 1)
            shot.velocity = shot.velocity.rotate(self.rotation)
            shot.velocity = shot.velocity * PLAYER_SHOOT_SPEED

    def wrap_around(self):

        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def spawn_thrust_particles(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        back_pos = self.position - forward * self.radius

        for _ in range(2):
            sideways = forward.rotate(90)
            offset = sideways * random.uniform(-8, 8)

            particle = {
                "pos": pygame.Vector2(back_pos + offset),
                "vel": -forward * 100 + sideways * random.uniform(-30, 30),
                "radius": 3,
                "life": 0.3,
            }
            self.thrust_particles.append(particle)

    def update_particles(self, dt):
        alive = []
        for p in self.thrust_particles:
            p["life"] -= dt*4
            if p["life"] <= 0:
                continue

            p["pos"] += p["vel"] * dt
            p["radius"] *= 1.2

            if p["radius"] > 0.5:
                alive.append(p)

        self.thrust_particles = alive


