from flask import Flask, render_template, request
from netmiko import ConnectHandler
import importlib
import os


def get_router_device():
    """Load router settings from router_config or environment variables."""
    try:
        return importlib.import_module("router_config").get_router_device()
    except ModuleNotFoundError as e:
        if e.name != "router_config":
            raise

    required = ("ROUTER_HOST", "ROUTER_USERNAME", "ROUTER_PASSWORD")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            "router_config.py is unavailable; set " + ", ".join(missing)
        )
    device = {
        "device_type": os.getenv("ROUTER_DEVICE_TYPE", "cisco_ios"),
        "host": os.environ["ROUTER_HOST"],
        "username": os.environ["ROUTER_USERNAME"],
        "password": os.environ["ROUTER_PASSWORD"],
    }
    if os.getenv("ROUTER_SECRET"):
        device["secret"] = os.environ["ROUTER_SECRET"]
    return device

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    error = None

    if request.method == "POST":
        commands_to_run = [
            "show version",
            "show ip interface brief",
            "show running-config"
        ]

        try:
            router_device = get_router_device()
            net_connect = ConnectHandler(**router_device)
            net_connect.enable()

            for cmd in commands_to_run:
                output = net_connect.send_command(cmd)
                results[cmd] = output

            net_connect.disconnect()

        except Exception as e:
            error = f"Connection failed: {e}"

    return render_template("index.html", results=results, error=error)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)