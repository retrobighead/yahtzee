from gym.envs.registration import register

register(
    id='yahtzeeenv-v0',
    entry_point='yahtzee_env.envs.yahtzee:YahtzeeEnv'
)
