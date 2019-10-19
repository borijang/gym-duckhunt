import os

import gym
import numpy as np
import pygame
from gym import spaces

from gym_duckhunt.envs.duckhunt_sprites import Move, Gun, Duck


class DuckHuntEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, demo=False):
        self.demo = demo
        self.seconds_left = 60
        self.spawn_duck_interval = 1300

        self.fps = 60
        self.total_score = 0

        self.width = 640
        self.height = 400
        self.move_amount = 1

        pygame.init()

        pygame.display.set_caption('DuckHunt-v0')
        self.screen = pygame.display.set_mode((self.width, self.height))
        if not self.demo:
            pygame.display.iconify()

        self.background = pygame.image.load(os.path.join("assets", "sprites", "background.png")).convert()
        self.foreground = pygame.image.load(os.path.join("assets", "sprites", "foreground.png")).convert()
        self.foreground.set_colorkey((9, 207, 252))

        self.gun = Gun(self.width, self.height, self.move_amount)
        self.ducks = pygame.sprite.Group()

        # Move in 8 directions + shoot
        self.action_space = spaces.Discrete(9)
        self.move_handler = {
            Move.N: self.gun.go_north,
            Move.NE: self.gun.go_northeast,
            Move.E: self.gun.go_east,
            Move.SE: self.gun.go_southeast,
            Move.S: self.gun.go_south,
            Move.SW: self.gun.go_southwest,
            Move.W: self.gun.go_west,
            Move.NW: self.gun.go_northwest
        }

        self.observation_space = spaces.Box(low=0, high=255, shape=(self.width, self.height, 3), dtype=np.uint8)
        self._render = False

        self.start_time = pygame.time.get_ticks()
        self.previous_spawn_time = 0

    def step(self, action):
        pygame.event.pump()

        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        game_over = True if elapsed >= 60 else False

        if action in list(self.move_handler):
            self.move_handler[action]()
            step_reward = 0

        else:
            step_reward = self.gun.shoot(self.ducks)

            self.total_score += step_reward

        if pygame.time.get_ticks() - self.previous_spawn_time >= self.spawn_duck_interval:
            Duck(self.ducks)  # Spawn a duck
            self.previous_spawn_time = pygame.time.get_ticks()

        self.ducks.update()

        surface = self.blit(pygame.Surface((self.width, self.height)))

        image_data = pygame.surfarray.array3d(surface)

        return image_data, step_reward, game_over, "info wip"

    def reset(self):
        self.seconds_left = 60
        self.total_score = 0
        self.gun = Gun(self.width, self.height, self.move_amount)
        self.ducks.empty()

        pygame.init()

    def render(self, mode='human', close=False):
        if self.demo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.blit(self.screen)
            pygame.display.flip()

    def blit(self, screen):
        screen.blit(self.background, (0, 0))

        self.ducks.draw(screen)

        screen.blit(self.foreground, (0, 0))

        self.gun.blit(screen)

        return screen

    def close(self):
        pass


if __name__ == "__main__":
    env = DuckHuntEnv(demo=True)
    total_reward = 0
    while True:
        env.render()
        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            print("Done. Total reward: %d" % total_reward)
            break
