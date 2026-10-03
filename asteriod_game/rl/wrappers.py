from asteriod_game.game.actions import Actions
from gymnasium import ActionWrapper, spaces
import numpy as np

N_ACTION_BITS = len(Actions().to_array())

class DiscreteActionWrapper(ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = spaces.Discrete(2 ** N_ACTION_BITS)

    def action(self, action):
        '''
        The function takes the number DQN picks and writes it in binary. 
        Each digit of that binary number becomes one action: 1 means the 
        action is on, 0 means it's off.

        The append line is just collecting those digits into a list, 
        one per loop pass, from the rightmost digit to the leftmost. (reverse)
        Thus, we can have combinations of actions, like rotate left and shoot.
        '''
        bits = []
        for i in range(N_ACTION_BITS):
            bits.append((int(action) >> i) & 1)
        return np.array(bits, dtype=np.int8)
