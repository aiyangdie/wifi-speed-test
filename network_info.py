"""Windows 网络信息获取模块"""

import re
import socket
import subprocess
from dataclasses import dataclass


@dataclass
class NetworkStatus:
    ssid: str = "未知"
    signal: str = "未知"
    ip: str = "未知"
    gateway: str = "未知"
    connected: bool = False


def _run_cmd(args: list[str]) -> str:
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding="gbk",
            errors="replace",
            timeout=10,
        )
        return result.stdout or result.stderr or ""
    except (subprocess.TimeoutExpired, OSError):
        return ""


def get_local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "未知"


def get_wifi_info() -> NetworkStatus:
    """获取当前 WiFi 连接信息（Windows）"""
    status = NetworkStatus(ip=get_local_ip())

    output = _run_cmd(["netsh", "wlan", "show", "interfaces"])
    if not output:
        return status

    ssid_match = re.search(r"SSID\s*:\s*(.+)", output)
    signal_match = re.search(r"信号\s*:\s*(.+)|Signal\s*:\s*(.+)", output, re.I)
    state_match = re.search(r"状态\s*:\s*(.+)|State\s*:\s*(.+)", output, re.I)

    if ssid_match:
        status.ssid = ssid_match.group(1).strip()

    if signal_match:
        status.signal = (signal_match.group(1) or signal_match.group(2) or "未知").strip()

    if state_match:
        state = (state_match.group(1) or state_match.group(2) or "").strip()
        status.connected = "已连接" in state or "connected" in state.lower()

    ipconfig = _run_cmd(["ipconfig"])
    gateway_match = re.search(r"默认网关.*?:\s*([\d.]+)", ipconfig, re.I)
    if not gateway_match:
        gateway_match = re.search(r"Default Gateway.*?:\s*([\d.]+)", ipconfig, re.I)
    if gateway_match:
        status.gateway = gateway_match.group(1).strip()

    return status
