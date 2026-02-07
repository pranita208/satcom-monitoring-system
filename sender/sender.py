import socket
import time

from common.packet import create_packet, serialize
from sender.controller import AdaptiveRateController


# ---------------- CONFIG ----------------
SATELLITE_IP = "127.0.0.1"
SATELLITE_PORT = 5001

PAYLOAD_SIZE = 1024
SOURCE_ID = "GROUND_STATION"
DEST_ID = "RECEIVER"

HEALTH_FILE = "link_health.txt"
# ----------------------------------------


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    controller = AdaptiveRateController()
    send_interval = 1.0  # initial rate (seconds)

    seq_num = 0
    print("[SENDER] Adaptive sender started")

    try:
        while True:
            # --- Read link health score (if available) ---
            try:
                with open(HEALTH_FILE, "r") as f:
                    health_score = float(f.read().strip())
                    send_interval = controller.update(health_score)
            except (FileNotFoundError, ValueError):
                # Receiver not started yet or invalid data
                pass

            # --- Create and send packet ---
            packet = create_packet(
                seq_num=seq_num,
                payload_size=PAYLOAD_SIZE,
                src=SOURCE_ID,
                dest=DEST_ID
            )

            data = serialize(packet)
            sock.sendto(data, (SATELLITE_IP, SATELLITE_PORT))

            print(
                f"[SENDER] Sent packet | "
                f"seq={seq_num} | "
                f"interval={send_interval:.2f}s"
            )

            seq_num += 1
            time.sleep(send_interval)

    except KeyboardInterrupt:
        print("\n[SENDER] Shutting down sender")

    finally:
        sock.close()


if __name__ == "__main__":
    main()
