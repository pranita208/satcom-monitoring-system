class AdaptiveRateController:
    """
    Controls sender transmission rate based on link health score.
    """

    def __init__(
        self,
        min_interval: float = 0.2,
        max_interval: float = 3.0,
        step: float = 0.2
    ):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.step = step
        self.current_interval = 1.0  # start conservative

    def update(self, health_score: float) -> float:
        """
        Update send interval based on health score.
        """
        if health_score >= 80:
            # Link is healthy → speed up
            self.current_interval -= self.step

        elif health_score >= 60:
            # Stable → keep rate
            pass

        elif health_score >= 40:
            # Degraded → slow down
            self.current_interval += self.step

        elif health_score >= 20:
            # Poor → slow down aggressively
            self.current_interval += self.step * 2

        else:
            # Critical → emergency throttle
            self.current_interval = self.max_interval

        # Clamp interval to safe bounds
        self.current_interval = max(
            self.min_interval,
            min(self.max_interval, self.current_interval)
        )

        return self.current_interval
