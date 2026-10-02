from dataclasses import dataclass

@dataclass
class Actions:
    rotate_left: bool = False
    rotate_right: bool = False
    thrust_forward: bool = False
    thrust_backward: bool = False
    shoot: bool = False

    def to_array(self):
        return [
            int(self.rotate_left),
            int(self.rotate_right),
            int(self.thrust_forward),
            int(self.thrust_backward),
            int(self.shoot),
        ]

    @classmethod
    def from_array(cls, action):
        return cls(
            rotate_left=bool(action[0]),
            rotate_right=bool(action[1]),
            thrust_forward=bool(action[2]),
            thrust_backward=bool(action[3]),
            shoot=bool(action[4]),
        )
