import os

from gym.envs.registration import register

register(
    id='DuckHunt-v0',
    entry_point='gym_duckhunt.envs:DuckHuntEnv',
)

ASSETS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "envs", "assets")
