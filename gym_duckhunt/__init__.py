from gym.envs.registration import register

register(
    id='duckhunt-v0',
    entry_point='gym_duckhunt.envs:DuckHuntEnv',
)