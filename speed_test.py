"""网络测速模块 - 基于 speedtest.net"""

from dataclasses import dataclass
from typing import Callable


@dataclass
class SpeedResult:
    ping_ms: float = 0.0
    download_mbps: float = 0.0
    upload_mbps: float = 0.0
    server_name: str = ""
    server_location: str = ""
    isp: str = ""


def run_speed_test(
    on_status: Callable[[str], None] | None = None,
    on_progress: Callable[[str, float], None] | None = None,
) -> SpeedResult:
    """
    执行完整网速测试。
    on_status: 状态文字回调
    on_progress: 进度回调 (阶段名, 0~100)
    """
    import speedtest

    def status(msg: str) -> None:
        if on_status:
            on_status(msg)

    def progress(stage: str, pct: float) -> None:
        if on_progress:
            on_progress(stage, pct)

    st = speedtest.Speedtest(secure=True)

    status("正在寻找最佳测速服务器...")
    progress("server", 10)
    best = st.get_best_server()
    server_name = best.get("sponsor", "未知")
    server_location = f"{best.get('name', '')}, {best.get('country', '')}"

    status(f"已连接服务器: {server_name}")
    progress("server", 25)

    status("正在测试延迟 (Ping)...")
    progress("ping", 35)
    ping = st.results.ping

    status("正在测试下载速度...")
    progress("download", 50)
    download_bps = st.download(threads=None)
    download_mbps = download_bps / 1_000_000

    status("正在测试上传速度...")
    progress("upload", 75)
    upload_bps = st.upload(threads=None, pre_allocate=False)
    upload_mbps = upload_bps / 1_000_000

    progress("done", 100)
    status("测试完成！")

    return SpeedResult(
        ping_ms=round(ping, 1),
        download_mbps=round(download_mbps, 2),
        upload_mbps=round(upload_mbps, 2),
        server_name=server_name,
        server_location=server_location.strip(", "),
        isp=st.results.client.get("isp", "未知"),
    )
