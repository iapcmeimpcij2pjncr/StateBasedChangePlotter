from Plotter import StateBase


def sign(x: float) -> int:
    """
    Returns the sign of the number: 1 if positive, -1 if negative, 0 if 0
    :param x:
    :return:
    """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


class TrapezoidalProfile(StateBase):
    """
    This class is a simple trapezoidal profile. It is not smooth, and will have a jerk at the end of the profile.
    Basically acts like a Slew Rate Limiter
    """
    def __init__(self, max_speed: float):
        """
        :param max_speed:
        """
        self.current_value = 0
        self.direction = 0
        self.max_speed = max_speed

    def update(self, time_delta: float, target: float) -> float:
        # if within tolerance just set current position to target
        if abs(target - self.current_value) < self.max_speed * time_delta:
            self.current_value = target
            self.direction = 0
            return self.current_value

        # update direction
        self.direction = sign(target - self.current_value)

        # update current value
        self.current_value += self.direction * self.max_speed * time_delta

        return self.current_value

    def set_state(self, value: float) -> None:
        self.current_value = value
        self.direction = 0

    def get_state(self) -> float:
        return self.current_value

    def is_at_target(self) -> bool:
        return self.direction == 0
