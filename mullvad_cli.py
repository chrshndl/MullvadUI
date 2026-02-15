from __future__ import annotations
import subprocess
import time


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

def get_connection_state() -> bool:
    """
    Returns True if connection mode is ON, False if OFF.

    Example output:
      "Block traffic when the VPN is disconnected: on"
    """
    out = _run(["mullvad", "status"]).lower().strip()

    if out.lower().startswith("connected"):
        return True
    
    if out.lower().startswith("disconnected"):
        return False    
    
    if "connecting" in out or "disconnecting" in out:
        raise MullvadCliError("Connection state transitional")

    raise MullvadCliError(f"Unrecognized output from mullvad: {out}")


def connect() -> None:
    """
    Docstring for connect

    Connects the Mullvad VPN

    Verifies connection
    """
    _run(["mullvad", "connect"])
    wait_for_connection_state(True)
    
def disconnect() -> None:
    """
    Docstring for disconnect

    Disconnects the Mullvad VPN

    Verifies disconnection
    """
    _run(["mullvad", "disconnect"])
    wait_for_connection_state(False)
    
def toggle_connection() -> bool:
    """
    Docstring for toggle_connection
    
    :return: True if connected, False otherwise.
    :rtype: bool
    """
    current_state = get_connection_state()

    if current_state:
        disconnect()
        return False
    else:
        connect()
        return True

#region helpers

def wait_for_connection_state(target: bool, timeout: float=10.0) -> None:
    """
    Docstring for wait_for_connection_state
    
    :param target: ignored
    :type target: bool
    :param timeout: Time to wait for connect/disconnect procedure
    :type timeout: float
    """
    start = time.time()

    while time.time() - start < timeout:
        try:
            state = get_connection_state()
            if state == target:
                return
        except MullvadCliError:
            pass

        time.sleep(0.5)

    raise MullvadCliError(
        f"Timeout waiting for mullvad to become"
        f"{'connected' if target else 'disconnected'}."
        )


#endregion helpers 