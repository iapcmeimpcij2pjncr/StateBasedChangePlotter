from TrapezoidalProfile import TrapezoidalProfile, sign

class SmoothedTrapezoidalProfile(TrapezoidalProfile):
    """
    This class is a smoothed trapezoidal profile. It is smooth, and will not have a jerk at the end of the profile.
    Basically acts like a Slew Rate Limiter, but with curved edges
    """
    def __init__(self, max_speed: float, max_acceleration: float):
        """
        :param max_speed: The speed the state can change at
        :param max_acceleration: How fast the speed accelerates to the max speed
        """
        super().__init__(max_speed)
        self.max_acceleration = max_acceleration
        self.acceleration_smoother = TrapezoidalProfile(max_acceleration) # gives the slope of the function

        # integral function = (direction * max_acceleration / 2) * (time_delta^2)
        # for acceleration to stop = max_speed/max_acceleration
        self.critical_duration = self.max_speed / self.max_acceleration
        self.critical_distance = (self.max_acceleration / 2) * (self.critical_duration ** 2)

    # if you don't understand derivitives, integrals, and power rule, this might be a bit weird
    def calculate_critical_distance(self) -> None:
        """
        Calculates the distance needed to go from the current speed to 0 acceleration
        """
        current_acceleration = self.acceleration_smoother.get_state()
        critical_duration = current_acceleration / self.max_acceleration # gets the duration till the derivitive is at 0
        critical_distance = (self.max_acceleration / 2) * (critical_duration ** 2) # integral calculation should stay the same
        return critical_distance

    def update(self, time_delta: float, target: float) -> (float, float):
        # update direction
        self.direction = sign(target - self.current_value)

        # update acceleration

        # handles accelerating up: checks that it is not within the "critical distance" of the target
        if abs(target - self.current_value) > self.calculate_critical_distance():
            self.current_value += self.acceleration_smoother.update(time_delta, self.direction * self.max_acceleration) * time_delta
        # if within tolerance just set current position to target
        # NOTE: might cause it to have some jittery motion at low fps
        elif self.acceleration_smoother.get_state() == 0 and abs(target - self.current_value) <= time_delta * self.max_acceleration:
            self.current_value = target
            self.acceleration_smoother.set_state(0)
            self.direction = 0
        # handles deaccelerating when in critical distance
        else:
            self.current_value += self.acceleration_smoother.update(time_delta, 0) * time_delta

        return self.current_value
