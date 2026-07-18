from enum import StrEnum


class ConnectionState(StrEnum):
    CONNECTING = "connecting"
    CONNECTED = "connected"
    STOPPING = "stopping"
    STOPPED = "stopped"
