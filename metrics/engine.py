class LinkHealthEngine:
    """
    Computes link health score from raw network metrics.
    """

    def __init__(self, expected_throughput: float):
        self.expected_throughput = expected_throughput

    def compute_health(
        self,
        avg_latency_ms: float,
        packet_loss_percent: float,
        throughput: float
    ) -> float:
        health = 100.0

        # ---- Latency penalty ----
        latency_penalty = min(avg_latency_ms / 20.0, 40.0)

        # ---- Packet loss penalty ----
        loss_penalty = packet_loss_percent * 1.5

        # ---- Throughput penalty ----
        if throughput < self.expected_throughput:
            throughput_penalty = (
                (self.expected_throughput - throughput)
                / self.expected_throughput
            ) * 20.0
        else:
            throughput_penalty = 0.0

        health -= latency_penalty
        health -= loss_penalty
        health -= throughput_penalty

        return max(0.0, min(100.0, health))
