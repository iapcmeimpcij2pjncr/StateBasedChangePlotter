from abc import ABC, abstractmethod


class StateBase(ABC):
    @abstractmethod
    def update(self, time_delta : float, target: float) -> float:
        """
        Updates the current value of the profile based on the time delta and the target. Returns the updated value.
        :param time_delta: time since last update
        :param target:
        :return: the updated value
        """
        pass

    @abstractmethod
    def set_state(self, value: float) -> None:
        """
        Sets the current value of the profile to the given value, and sets the direction to 0
        :param value: New value of the profile
        """
        pass

    @abstractmethod
    def get_state(self) -> float:
        """
        Returns the current value of the profile
        """
        pass

    @abstractmethod
    def is_at_target(self) -> bool:
        """
        Returns true if the profile is at the target
        :return: True if the profile is at the target, else false
        """
        pass


class Plotter:
    """
    This class is used to plot the output of a StateBase object over time.
    """
    def __init__(self, state: StateBase):
        self.state = state

    def plot(self, start: float, end: float, duration: float, time_delta: float, padding: (float, float) = (0, 0)):
        """
        Returns an array representing the output of the state over time
        :param start: The value to start the profile at
        :param end: The value to make the profile try and reach
        :param duration: The simulated amount of seconds (Use -1 to stop it when it reaches the target)
        :param time_delta: Time between each update
        :param padding: The amount of time to wait before and after the profile starts and ends, as a tuple (before, after)
        :return:
        """

        self.state.set_state(start)

        results = []

        print(padding)
        for _ in range(round(padding[0]/time_delta)):
            results.append(self.state.update(time_delta, start))

        print(len(results))

        if duration == -1:
            i = 0
            # prevent initalization problems
            results.append(self.state.update(time_delta, end))
            while not self.state.is_at_target() and i < 10000: # prevent infinite loop
                results.append(self.state.update(time_delta, end))
                i += 1
            print(i)

        else:
            cycles = int(duration / time_delta)
            results += [self.state.update(time_delta, end) for _ in range(cycles)]

        for _ in range(round(padding[1]/time_delta)):
            results.append(self.state.update(time_delta, end))
        return results
