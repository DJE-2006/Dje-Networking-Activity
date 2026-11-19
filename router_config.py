import os


def get_router_device():
    required = ("ROUTER_IP", "ROUTER_USERNAME", "ROUTER_PASSWORD", "ROUTER_ENABLE_SECRET")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise RuntimeError(
            "Set the following environment variables before connecting: "
            + ", ".join(missing)
        )

    try:
        port = int(os.getenv("ROUTER_PORT", "32770"))
    except ValueError as exc:
        raise RuntimeError("ROUTER_PORT must be an integer") from exc

    return {
        "device_type": "cisco_ios_telnet",
        "ip": os.environ["ROUTER_IP"],
        "port": port,
        "username": os.environ["ROUTER_USERNAME"],
        "password": os.environ["ROUTER_PASSWORD"],
        "secret": os.environ["ROUTER_ENABLE_SECRET"],
    }
