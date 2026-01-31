import json
import time
import uuid

DEFAULT_TTL = 64


def create_packet(
    seq_num: int,
    payload_size: int = 1024,
    src: str = "GROUND_STATION",
    dest: str = "RECEIVER",
    ttl: int = DEFAULT_TTL
) -> dict:
    """
    Create a canonical satellite communication packet.
    """
    packet = {
        "packet_id": str(uuid.uuid4()),
        "seq_num": seq_num,
        "send_ts": time.time(),
        "payload_size": payload_size,
        "ttl": ttl,
        "src": src,
        "dest": dest
    }
    return packet


def serialize(packet: dict) -> bytes:
    """
    Convert packet dictionary to bytes for UDP transmission.
    """
    return json.dumps(packet).encode("utf-8")


def deserialize(packet_bytes: bytes) -> dict:
    """
    Convert received bytes back into packet dictionary.
    """
    return json.loads(packet_bytes.decode("utf-8"))
