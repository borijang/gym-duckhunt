import os
from enum import IntEnum

import pygame
from numpy import sum
from numpy.random import randint, choice
from pygame.rect import Rect
from pygame.sprite import Sprite

duck_points = {"blue": 25, "red": 50, "black": 75}
duck_directions = {"west": -1, "east": 1}
duck_altitude = {"straight": 0, "up": -1}


class Move(IntEnum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7


class Gun(Sprite):
    def __init__(self, width, height, move_amount):
        super().__init__()

        self.width = width
        self.height = height
        self.move_amount = move_amount

        self.image = pygame.image.load(os.path.join('assets', 'sprites', 'crosshair.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 35))
        rect = self.image.get_rect()
        self.rect = Rect(rect.left + 5, rect.top + 5, rect.width - 10, rect.height - 10).move(width // 2, height // 2)

    def blit(self, surface):
        surface.blit(self.image, self.rect)

    def shoot(self, ducks):
        hit_ducks = pygame.sprite.spritecollide(self, ducks, dokill=False)

        return sum([duck.got_shot() for duck in hit_ducks if duck.alive])

    def go_north(self):
        self.rect.move_ip(0, -self.move_amount)

    def go_northeast(self):
        self.rect.move_ip(self.move_amount, -self.move_amount)

    def go_east(self):
        self.rect.move_ip(self.move_amount, 0)

    def go_southeast(self):
        self.rect.move_ip(self.move_amount, self.move_amount)

    def go_south(self):
        self.rect.move_ip(0, self.move_amount)

    def go_southwest(self):
        self.rect.move_ip(-self.move_amount, self.move_amount)

    def go_west(self):
        self.rect.move_ip(-self.move_amount, 0)

    def go_northwest(self):
        self.rect.move_ip(-self.move_amount, -self.move_amount)

    def update(self):
        if self.rect.x >= self.width:
            self.rect.move_ip(-(self.rect.x - self.width + 1), 0)

        if self.rect.x < 0:
            self.rect.move_ip(-self.rect.x + 1, 0)

        if self.rect.y >= self.height:
            self.rect.move_ip(0, -(self.rect.y - self.height + 1))

        if self.rect.y < 0:
            self.rect.move_ip(0, (-self.rect.y + 1))


class Duck(Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.alive = True

        color = choice(list(duck_points))
        self.worth = duck_points[color]
        self.fetch_sprites(color)

        self.altitude = "up"
        self.direction = choice(list(duck_directions))
        self.set_new_frames()

        self.image = self.frames[0]
        rect = self.image.get_rect()
        self.rect = Rect(rect.left + 5, rect.top + 5, rect.width - 10, rect.height - 10).move(randint(10, 470), 350)

        self.dx = duck_directions[self.direction]
        self.dy = -1

        self.die_delay = 0
        self.bamboozle_ticks = 0
        self.animation_ticks = 0
        self.frame_ticks = 0

    def try_bamboozle(self):
        # 20% chance to switch direction (horizontal bamboozle)
        if choice([True, False], p=[0.2, 0.8]):
            self.direction = "west" if self.direction == "east" else "east"
            self.dx = duck_directions[self.direction]
            self.bamboozle_ticks = 0
            self.set_new_frames()

        # 20% chance to switch altitude direction (vertical bamboozle)
        if choice([True, False], p=[0.2, 0.8]):
            self.altitude = "straight" if self.altitude == "up" else "up"
            self.dx = duck_directions[self.direction]
            self.dy = duck_altitude[self.altitude]
            self.bamboozle_ticks = 0
            self.set_new_frames()

    def update(self):
        if self.alive:
            if self.rect.bottom <= 0 or self.rect.right <= 0 or self.rect.left >= 640:
                self.kill()
                return

            if self.bamboozle_ticks < 100:
                self.bamboozle_ticks += 1
            else:
                self.try_bamboozle()

        else:
            if self.image != self.frames[0]:
                self.dy = 1  # Start falling

            if self.rect.bottom >= 370:  # Birb reached the ground, destroy it
                self.kill()
                return

        try:
            self.image = self.frames[self.frame_ticks // (len(self.frames) * 4)]

        except IndexError:
            self.frame_ticks = 0
            self.image = self.frames[self.frame_ticks]

        self.frame_ticks += 1
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect().move(x + self.dx, y + self.dy)

    def got_shot(self):
        self.alive = False
        self.set_new_frames()

        self.image = self.frames[self.frame_ticks]
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect().move(x, y)

        self.dx = 0
        self.dy = 0  # Freeze for a short time before starting to fall

        return self.worth

    def destroy(self):
        pass

    def fetch_sprites(self, color):
        self.fly_northeast = [pygame.image.load(os.path.join("assets", "sprites", color, "duck1.png")).convert(),
                              pygame.image.load(os.path.join("assets", "sprites", color, "duck2.png")).convert(),
                              pygame.image.load(os.path.join("assets", "sprites", color, "duck3.png")).convert()]

        self.fly_east = [pygame.image.load(os.path.join("assets", "sprites", color, "duck4.png")).convert(),
                         pygame.image.load(os.path.join("assets", "sprites", color, "duck5.png")).convert(),
                         pygame.image.load(os.path.join("assets", "sprites", color, "duck6.png")).convert()]

        self.fly_northwest = [pygame.image.load(os.path.join("assets", "sprites", color, "duck7.png")).convert(),
                              pygame.image.load(os.path.join("assets", "sprites", color, "duck8.png")).convert(),
                              pygame.image.load(os.path.join("assets", "sprites", color, "duck9.png")).convert()]

        self.fly_west = [pygame.image.load(os.path.join("assets", "sprites", color, "duck10.png")).convert(),
                         pygame.image.load(os.path.join("assets", "sprites", color, "duck11.png")).convert(),
                         pygame.image.load(os.path.join("assets", "sprites", color, "duck12.png")).convert()]

        self.die_ = [pygame.image.load(os.path.join("assets", "sprites", color, "duck_die1.png")).convert(),
                     pygame.image.load(os.path.join("assets", "sprites", color, "duck_die2.png")).convert(),
                     pygame.image.load(os.path.join("assets", "sprites", color, "duck_die3.png")).convert()]

        for item in self.fly_northeast + self.fly_east + self.fly_northwest + self.fly_west + self.die_:
            item.set_colorkey((163, 239, 165))

    def set_new_frames(self):
        self.frame_ticks = 0

        if not self.alive:
            self.frames = [self.die_[0], self.die_[1], self.die_[2]]
        elif self.direction == "east" and self.altitude == "straight":
            self.frames = [self.fly_east[1], self.fly_east[0], self.fly_east[1], self.fly_east[2]]
        elif self.direction == "east" and self.altitude == "up":
            self.frames = [self.fly_northeast[1], self.fly_northeast[0],
                           self.fly_northeast[1], self.fly_northeast[2]]
        elif self.direction == "west" and self.altitude == "straight":
            self.frames = [self.fly_west[1], self.fly_west[0], self.fly_west[1], self.fly_west[2]]
        else:
            self.frames = [self.fly_northwest[1], self.fly_northwest[0],
                           self.fly_northwest[1], self.fly_northwest[2]]
