import random
import time
from enum import Enum


class LinkState(Enum):
    GOOD = "GOOD"
    DEGRADED = "DEGRADED"
    BAD = "BAD"
    OUTAGE = "OUTAGE"


class DynamicLinkModel:
    """
    Simulates time-varying satellite link conditions.
    """

    def __init__(self):
        self.start_time = time.time()
        self.current_state = LinkState.GOOD

    def update_state(self):
        """
        Update link state based on elapsed time.
        """
        elapsed = time.time() - self.start_time

        if elapsed < 30:
            self.current_state = LinkState.GOOD
        elif elapsed < 60:
            self.current_state = LinkState.DEGRADED
        elif elapsed < 90:
            self.current_state = LinkState.BAD
        elif elapsed < 110:
            self.current_state = LinkState.OUTAGE
        else:
            self.current_state = LinkState.GOOD

    def get_delay_ms(self) -> int:
        """
        Return delay based on current link state.
        """
        if self.current_state == LinkState.GOOD:
            return random.randint(300, 500)

        if self.current_state == LinkState.DEGRADED:
            return random.randint(700, 900)

        if self.current_state == LinkState.BAD:
            return random.randint(1200, 1500)

        return 0  # OUTAGE (no delay because packets are dropped)

    def should_drop_packet(self) -> bool:
        """
        Decide whether to drop packet based on link state.
        """
        if self.current_state == LinkState.GOOD:
            return random.random() < 0.02

        if self.current_state == LinkState.DEGRADED:
            return random.random() < 0.12

        if self.current_state == LinkState.BAD:
            return random.random() < 0.30

        return True  # OUTAGE → drop everything
