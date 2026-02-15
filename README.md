MullvadUI

Minimal PySide6 desktop UI prototype for controlling Mullvad VPN features (e.g. lockdown mode).

Runs directly on Bazzite (Fedora Atomic) using a local Python virtual environment.

📦 Requirements (At a Glance)
System Packages (Fedora / Bazzite)

Install once on the host:

```bash
sudo rpm-ostree install \
  python3 python3-pip python3-venv \
  mesa-libGL mesa-libEGL \
  libxkbcommon libxkbcommon-x11 \
  qt6-qtwayland \
  xcb-util-cursor
```

Reboot after installing:

```bash
systemctl reboot
```

Python Packages (inside venv)
PySide6


Installed via:

```bash
pip install -r requirements.txt
```

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


Verify:

```bash
python -c "import PySide6; print('OK')"
```

▶️ Run the Application

```bash
source .venv/bin/activate
python main.py
```

🧪 Development Workflow

Activate environment before working:

```bash
source .venv/bin/activate
´´´


Install new package:

```bash
pip install <package>
pip freeze > requirements.txt
```

📁 Project Structure
MullvadUI/
│
├── .venv/
├── main.py
├── mullvad_cli.py
├── lockdown_widget.py
├── requirements.txt
└── README.md

🐛 Common Issues
qt.qpa.xcb: could not connect to display

Make sure you're running inside a graphical session (Wayland or X11).

ImportError: libGL.so.1
sudo rpm-ostree install mesa-libGL

ImportError: libxkbcommon.so.0
sudo rpm-ostree install libxkbcommon

Git permission errors after container usage

If .git/ was previously owned by root:

sudo chown -R $USER:$USER .

🧠 Notes

Do not mix Tkinter and PySide6.

Always use the local .venv.

Avoid running development as root.

Mullvad CLI must be installed and working:

mullvad lockdown-mode get

📌 Future Improvements

Move to structured application layout (src/)

Add logging

Add background threading for CLI calls

Add system tray integration

Package as native RPM or AppImage