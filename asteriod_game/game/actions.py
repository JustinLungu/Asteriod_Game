from dataclasses import dataclass

@dataclass
class Actions:
    rotate_left: bool = False
    rotate_right: bool = False
    thrust_forward: bool = False
    thrust_backward: bool = False
    shoot: bool = False
