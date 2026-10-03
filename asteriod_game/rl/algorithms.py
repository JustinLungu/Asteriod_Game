from stable_baselines3 import DQN, PPO

ALGORITHMS = {
    "ppo": (PPO, False),
    "dqn": (DQN, True),
}
