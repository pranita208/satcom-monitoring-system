import socket
import time

from common.packet import create_packet, serialize


# ---------------- CONFIG ----------------
SATELLITE_IP = "127.0.0.1"
SATELLITE_PORT = 5001

SEND_INTERVAL_SEC = 1       # packet every 1 second
PAYLOAD_SIZE = 1024         # bytes
SOURCE_ID = "GROUND_STATION"
DEST_ID = "RECEIVER"
# ----------------------------------------


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    seq_num = 0
    print("[SENDER] Ground station sender started")

    while True:
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
            f"size={PAYLOAD_SIZE} bytes"
        )

        seq_num += 1
        time.sleep(SEND_INTERVAL_SEC)


if __name__ == "__main__":
    main()
