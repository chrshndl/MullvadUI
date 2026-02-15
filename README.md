# MullvadUI

Minimal PySide6 desktop UI prototype developed inside a Fedora container using Distrobox.

This project is designed to run in a containerized development environment to keep host dependencies clean and reproducible.

---

## 🧱 Development Environment

- **Host OS:** Bazzite (Fedora Atomic)
- **Container:** Fedora 40 (via Distrobox)
- **Container Runtime:** Podman
- **Python:** Virtual environment (`.venv`)
- **GUI Framework:** PySide6 (Qt6)

---

# 🚀 Setup Instructions

## 1️⃣ Host Requirements

Ensure the following tools are installed on the host:

podman --version
distrobox --version


If missing (on Bazzite):

```bash
sudo rpm-ostree install podman
sudo systemctl reboot
```


Create Development Container

```bash
distrobox create -n dev -i fedora:40
distrobox enter dev
```
Veryfi you are inside the container

whoami



Install Required System Dependencies (Inside Container)

Qt requires OpenGL and display libraries:

```bash
sudo dnf -y update

sudo dnf -y install \
  python3 python3-pip python3-venv \
  mesa-libGL mesa-libEGL \
  libxkbcommon libxkbcommon-x11 \
  qt6-qtwayland \
  xcb-util-cursor
```

These fix common errors such as:
libGL.so.1
libxkbcommon.so.0
Qt platform plugin "xcb"
Wayland/X11 display issues

Clone the Repository

```bash
mkdir -p ~/projects
cd ~/projects
git clone <REPO_URL>
cd MullvadUI
```

Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install PySide6
```

Verify installation:

```bash
python -c "import PySide6; print('OK')"
```

Run the Application

```bash
source .venv/bin/activate
python main.py
```

Running the GUI (Important)
Recommended Workflow

Edit in VS Code, but run the GUI from a distrobox enter terminal:

```bash
distrobox enter dev
cd ~/projects/MullvadUI
source .venv/bin/activate
python main.py
```
This ensures proper Wayland/X11 forwarding.



If You See Display Errors

Errors like:

```bash
qt.qpa.xcb: could not connect to display
Authorization required, but no authorization protocol specified
```
Run the application from a distrobox enter terminal instead of VS Code debug.


🧪 Development Workflow

Activate environment:

```bash
source .venv/bin/activate
```
Install new packages:

```bash
pip install <package>
pip freeze > requirements.txt
```

📁 Project Structure
MullvadUI/
│
├── .venv/
├── main.py
├── requirements.txt
└── README.md

🐛 Common Issues & Fixes

ImportError: libGL.so.1

```bash
sudo dnf install mesa-libGL
```

ImportError: libxkbcommon.so.0

```bash
sudo dnf install libxkbcommon
```

Qt platform plugin "xcb" error

```bash
sudo dnf install xcb-util-cursor
```

🧠 Notes

Always use the local .venv

Avoid running development as root

Recreate the virtual environment if the container is rebuilt

Prefer Wayland over X11 when possible


📌 Future Improvements

Refactor into structured application layout

Add logging

Add CI pipeline

Add packaging (PyInstaller / Briefcase / fbs)