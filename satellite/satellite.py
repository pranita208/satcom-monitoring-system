import socket
import time
import random

from common.packet import deserialize, serialize


# ---------------- CONFIG ----------------
LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 5001

RECEIVER_IP = "127.0.0.1"
RECEIVER_PORT = 5002

DELAY_MS = 600          # Simulated propagation delay (ms)
PACKET_LOSS_PROB = 0.1  # 10% packet loss
# ----------------------------------------


def main():
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_in.bind((LISTEN_IP, LISTEN_PORT))

    sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("[SATELLITE] Satellite node started")
    print(
        f"[SATELLITE] Delay={DELAY_MS} ms | "
        f"Packet Loss={PACKET_LOSS_PROB * 100:.0f}%"
    )

    try:
        while True:
            data, addr = sock_in.recvfrom(4096)
            packet = deserialize(data)

            # Simulate packet loss
            if random.random() < PACKET_LOSS_PROB:
                print(
                    f"[SATELLITE] DROPPED packet | "
                    f"seq={packet['seq_num']}"
                )
                continue

            # Simulate propagation delay
            time.sleep(DELAY_MS / 1000.0)

            # Decrement TTL (observational)
            packet["ttl"] -= 1
            if packet["ttl"] <= 0:
                print(
                    f"[SATELLITE] TTL EXPIRED | "
                    f"seq={packet['seq_num']}"
                )
                continue

            # Forward packet
            sock_out.sendto(
                serialize(packet),
                (RECEIVER_IP, RECEIVER_PORT)
            )

            print(
                f"[SATELLITE] FORWARDED packet | "
                f"seq={packet['seq_num']} | "
                f"ttl={packet['ttl']}"
            )

    except KeyboardInterrupt:
        print("\n[SATELLITE] Shutting down satellite node")

    finally:
        sock_in.close()
        sock_out.close()


if __name__ == "__main__":
    main()
