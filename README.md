MullvadUI

Minimal PySide6 desktop tray UI for controlling Mullvad VPN features
(e.g. lockdown mode, connect/disconnect).

Designed to run on Bazzite / Fedora Atomic using a local Python virtual environment.


📦 Requirements
System (Fedora / Bazzite)

Only Python and venv support are required:

```bash
sudo rpm-ostree install python3 python3-venv
```


Reboot once after installing:

```bash
systemctl reboot
```


No additional Qt system packages required.
PySide6 is installed locally inside the virtual environment.

🚀 Repository Setup

1️⃣ Clone

```bash
mkdir -p ~/projects
cd ~/projects
git clone <REPO_URL>
cd MullvadUI
```

2️⃣ Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
```


Verify installation:

```bash
python -c "import PySide6; print('OK')"
```

▶️ Run the Application

```bash
source .venv/bin/activate
python main.py
```

```bash
🔁 Development Workflow
```

Activate environment before working:

```bash
cd ~/projects/MullvadUI
source .venv/bin/activate
```


Install new package:

```bash
pip install <package>
pip freeze > requirements.txt
```

🖥 Autostart (KDE Plasma)

Create a start script:

```bash
start.sh
```

```bash
#!/usr/bin/env bash
cd /var/home/$USER/projects/MullvadUI || exit 1
source .venv/bin/activate
exec python main.py
```


Make it executable:

```bash
chmod +x start.sh
```


Create autostart entry:

```bash
~/.config/autostart/mullvadui.desktop
```

[Desktop Entry]
Type=Application
Name=MullvadUI
Exec=/var/home/$USER/projects/MullvadUI/start.sh
X-KDE-autostart-after=panel

🧠 Wayland Notes

Window positioning cannot be forced pixel-perfect under Wayland.

The app uses a tool-style window that behaves like a tray popup.

Last window position is remembered automatically.

📁 Project Structure
MullvadUI/
│
├── .venv/
├── main.py
├── mullvad_cli.py
├── lockdown_widget.py
├── connect_disconnect.py
├── requirements.txt
└── README.md

🐛 Common Issues
PySide6 not found

You are not inside the virtual environment:

source .venv/bin/activate

Running outside graphical session

If you see:

qt.qpa.xcb: could not connect to display


Ensure you're inside a Wayland or X11 session.

Git permission errors

If .git was created as root:

sudo chown -R $USER:$USER .

🔐 Requirements

Mullvad CLI must be installed and working:

mullvad status
mullvad lockdown-mode get

📌 Future Improvements

Structured application layout (src/)

Logging

Background threading for CLI calls

Packaging via PyInstaller (portable binary)

systemd --user service instead of KDE autostart

Warum das jetzt "perfekt passend" ist

Kein übertriebenes Atomic Layering

Kein unnötiges Qt System-Package Chaos

venv-first Ansatz (Best Practice für Atomic)

Tray + Wayland korrekt berücksichtigt

README passt exakt zu deinem aktuellen Code