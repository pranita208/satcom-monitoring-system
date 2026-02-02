import socket
import time

from common.packet import deserialize, serialize
from satellite.link_model import DynamicLinkModel


# ---------------- CONFIG ----------------
LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 5001

RECEIVER_IP = "127.0.0.1"
RECEIVER_PORT = 5002
# ----------------------------------------


def main():
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_in.bind((LISTEN_IP, LISTEN_PORT))

    sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Create dynamic link model
    link_model = DynamicLinkModel()

    print("[SATELLITE] Satellite node started")
    print("[SATELLITE] Dynamic link model enabled")

    try:
        while True:
            data, addr = sock_in.recvfrom(4096)
            packet = deserialize(data)

            # Update link state based on time
            link_model.update_state()

            # Decide packet loss
            if link_model.should_drop_packet():
                print(
                    f"[SATELLITE] DROPPED | "
                    f"state={link_model.current_state.value} | "
                    f"seq={packet['seq_num']}"
                )
                continue

            # Apply dynamic delay
            delay_ms = link_model.get_delay_ms()
            time.sleep(delay_ms / 1000.0)

            # Decrement TTL
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
                f"[SATELLITE] FORWARDED | "
                f"state={link_model.current_state.value} | "
                f"delay={delay_ms} ms | "
                f"seq={packet['seq_num']}"
            )

    except KeyboardInterrupt:
        print("\n[SATELLITE] Shutting down satellite node")

    finally:
        sock_in.close()
        sock_out.close()


if __name__ == "__main__":
    main()
