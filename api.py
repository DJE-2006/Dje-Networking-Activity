from flask import Flask, render_template, request
from netmiko import ConnectHandler
from router_config import get_router_device

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