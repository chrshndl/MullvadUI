from __future__ import annotations
import subprocess


class MullvadCliError(RuntimeError):
    pass


def _run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = (p.stdout or "").strip()
    err = (p.stderr or "").strip()
    if p.returncode != 0:
        raise MullvadCliError(err or out or f"Command failed: {' '.join(cmd)}")
    return out


def get_lockdown_state() -> bool:
    """
    Returns True if lockdown mode is ON, False if OFF.

    Example output:
      "Block traffic when the VPN is disconnected: on"
    """
    out = _run(["mullvad", "lockdown-mode", "get"]).lower()

    # robust parse: look for the last token 'on'/'off' or substring
    if out.strip().endswith(" on") or out.strip() == "on" or ": on" in out:
        return True
    if out.strip().endswith(" off") or out.strip() == "off" or ": off" in out:
        return False

    raise MullvadCliError(f"Unrecognized output from mullvad: {out}")


def set_lockdown_state(enabled: bool) -> None:
    """
    Sets lockdown mode on/off.
    """
    val = "on" if enabled else "off"
    _run(["mullvad", "lockdown-mode", "set", val])
