import socket
import time

from common.packet import deserialize


# ---------------- CONFIG ----------------
LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 5002

LOG_INTERVAL_SEC = 5
# ----------------------------------------


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))

    print("[RECEIVER] Receiver node started")
    print(f"[RECEIVER] Listening on {LISTEN_IP}:{LISTEN_PORT}")

    expected_seq = 0
    received_packets = 0
    lost_packets = 0
    total_bytes = 0
    start_time = time.time()
    last_log_time = start_time

    try:
        while True:
            data, addr = sock.recvfrom(4096)
            now = time.time()

            packet = deserialize(data)

            seq = packet["seq_num"]
            send_ts = packet["send_ts"]
            payload_size = packet["payload_size"]

            # Latency calculation (ms)
            latency_ms = (now - send_ts) * 1000

            # Packet loss detection
            if seq > expected_seq:
                lost_packets += (seq - expected_seq)

            expected_seq = seq + 1
            received_packets += 1
            total_bytes += payload_size

            print(
                f"[RECEIVER] Packet received | "
                f"seq={seq} | "
                f"latency={latency_ms:.2f} ms"
            )

            # Periodic metrics log
            if now - last_log_time >= LOG_INTERVAL_SEC:
                elapsed = now - start_time
                throughput = total_bytes / elapsed if elapsed > 0 else 0
                loss_percent = (
                    (lost_packets / (received_packets + lost_packets)) * 100
                    if (received_packets + lost_packets) > 0 else 0
                )

                print("\n[RECEIVER METRICS]")
                print(f"  Received packets : {received_packets}")
                print(f"  Lost packets     : {lost_packets}")
                print(f"  Packet loss (%)  : {loss_percent:.2f}")
                print(f"  Throughput       : {throughput:.2f} bytes/sec\n")

                last_log_time = now

    except KeyboardInterrupt:
        print("\n[RECEIVER] Shutting down receiver")

    finally:
        sock.close()


if __name__ == "__main__":
    main()
