# Router diagnostics

A small Flask app that runs read-only Cisco IOS show commands through Netmiko.

## Setup on Windows

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set the router connection details in the current PowerShell session:

```powershell
$env:ROUTER_IP = "your-router-or-console-host"
$env:ROUTER_PORT = "32770"
$env:ROUTER_USERNAME = "your-username"
$env:ROUTER_PASSWORD = "your-password"
$env:ROUTER_ENABLE_SECRET = "your-enable-secret"
```

Start the web app:

```powershell
python api.py
```

Then open `http://127.0.0.1:5000/`. Keep credentials out of source control; `.env` files and virtual environments are ignored by Git.
