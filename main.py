"""WiFi 网速测试 - 主界面"""

import threading
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

from network_info import get_wifi_info
from speed_test import run_speed_test


class WiFiSpeedApp(tk.Tk):
    COLORS = {
        "bg": "#0f172a",
        "card": "#1e293b",
        "accent": "#3b82f6",
        "accent_hover": "#2563eb",
        "success": "#22c55e",
        "text": "#f1f5f9",
        "muted": "#94a3b8",
        "border": "#334155",
    }

    def __init__(self) -> None:
        super().__init__()
        self.title("WiFi 网速测试 - 艾阳开发版")
        self.geometry("720x640")
        self.minsize(640, 580)
        self.configure(bg=self.COLORS["bg"])
        self.resizable(True, True)

        self._testing = False
        self._setup_styles()
        self._build_ui()
        self.refresh_network_info()

    def _setup_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Accent.Horizontal.TProgressbar",
            troughcolor=self.COLORS["card"],
            background=self.COLORS["accent"],
            bordercolor=self.COLORS["border"],
            lightcolor=self.COLORS["accent"],
            darkcolor=self.COLORS["accent"],
            thickness=8,
        )

    def _build_ui(self) -> None:
        c = self.COLORS
        title_font = tkfont.Font(family="Microsoft YaHei UI", size=22, weight="bold")
        label_font = tkfont.Font(family="Microsoft YaHei UI", size=10)
        value_font = tkfont.Font(family="Consolas", size=11)
        big_font = tkfont.Font(family="Microsoft YaHei UI", size=28, weight="bold")
        unit_font = tkfont.Font(family="Microsoft YaHei UI", size=12)

        header = tk.Frame(self, bg=c["bg"])
        header.pack(fill="x", padx=24, pady=(20, 8))
        tk.Label(
            header,
            text="📶 WiFi 网速测试",
            font=title_font,
            fg=c["text"],
            bg=c["bg"],
        ).pack(side="left")
        tk.Label(
            header,
            text="艾阳开发版 v1.0",
            font=label_font,
            fg=c["muted"],
            bg=c["bg"],
        ).pack(side="right", pady=8)

        self._info_frame = self._make_card()
        self._info_frame.pack(fill="x", padx=24, pady=8)

        info_title = tk.Label(
            self._info_frame,
            text="当前网络信息",
            font=tkfont.Font(family="Microsoft YaHei UI", size=12, weight="bold"),
            fg=c["text"],
            bg=c["card"],
        )
        info_title.grid(row=0, column=0, columnspan=4, sticky="w", padx=16, pady=(12, 8))

        self._info_labels: dict[str, tk.Label] = {}
        fields = [("WiFi 名称", "ssid"), ("信号强度", "signal"), ("本机 IP", "ip"), ("网关", "gateway")]
        for i, (label, key) in enumerate(fields):
            row, col = divmod(i, 2)
            tk.Label(
                self._info_frame,
                text=f"{label}:",
                font=label_font,
                fg=c["muted"],
                bg=c["card"],
            ).grid(row=row + 1, column=col * 2, sticky="w", padx=(16, 4), pady=4)
            val = tk.Label(
                self._info_frame,
                text="--",
                font=value_font,
                fg=c["text"],
                bg=c["card"],
            )
            val.grid(row=row + 1, column=col * 2 + 1, sticky="w", padx=(0, 24), pady=4)
            self._info_labels[key] = val

        refresh_btn = tk.Button(
            self._info_frame,
            text="刷新",
            font=label_font,
            fg=c["text"],
            bg=c["border"],
            activebackground=c["accent"],
            activeforeground=c["text"],
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=2,
            command=self.refresh_network_info,
        )
        refresh_btn.grid(row=3, column=0, columnspan=4, sticky="e", padx=16, pady=(4, 12))

        result_frame = self._make_card()
        result_frame.pack(fill="both", expand=True, padx=24, pady=8)

        self._speed_cards: dict[str, dict] = {}
        metrics = [
            ("ping", "延迟", "ms", c["accent"]),
            ("download", "下载", "Mbps", c["success"]),
            ("upload", "上传", "Mbps", "#a855f7"),
        ]
        for i, (key, name, unit, color) in enumerate(metrics):
            card = tk.Frame(result_frame, bg=c["bg"])
            card.grid(row=0, column=i, padx=8, pady=16, sticky="nsew")
            result_frame.columnconfigure(i, weight=1)

            tk.Label(card, text=name, font=label_font, fg=c["muted"], bg=c["bg"]).pack()
            val = tk.Label(card, text="--", font=big_font, fg=color, bg=c["bg"])
            val.pack(pady=(4, 0))
            unit_lbl = tk.Label(card, text=unit, font=unit_font, fg=c["muted"], bg=c["bg"])
            unit_lbl.pack()
            self._speed_cards[key] = {"value": val, "unit": unit_lbl}

        self._status_label = tk.Label(
            result_frame,
            text="点击「开始测速」检测您的网络速度",
            font=label_font,
            fg=c["muted"],
            bg=c["card"],
        )
        self._status_label.grid(row=1, column=0, columnspan=3, pady=(0, 8))

        self._progress = ttk.Progressbar(
            result_frame,
            style="Accent.Horizontal.TProgressbar",
            mode="determinate",
            maximum=100,
        )
        self._progress.grid(row=2, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 8))

        self._server_label = tk.Label(
            result_frame,
            text="",
            font=label_font,
            fg=c["muted"],
            bg=c["card"],
        )
        self._server_label.grid(row=3, column=0, columnspan=3, pady=(0, 12))

        btn_frame = tk.Frame(self, bg=c["bg"])
        btn_frame.pack(fill="x", padx=24, pady=(0, 20))

        self._start_btn = tk.Button(
            btn_frame,
            text="▶  开始测速",
            font=tkfont.Font(family="Microsoft YaHei UI", size=14, weight="bold"),
            fg="white",
            bg=c["accent"],
            activebackground=c["accent_hover"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=32,
            pady=12,
            command=self.start_test,
        )
        self._start_btn.pack()

        footer = tk.Label(
            self,
            text="开源项目 · 作者: 艾阳 (aiyangdie) · 基于 speedtest.net",
            font=tkfont.Font(family="Microsoft YaHei UI", size=9),
            fg=c["muted"],
            bg=c["bg"],
        )
        footer.pack(pady=(0, 12))

    def _make_card(self) -> tk.Frame:
        frame = tk.Frame(self, bg=self.COLORS["card"], highlightbackground=self.COLORS["border"], highlightthickness=1)
        return frame

    def refresh_network_info(self) -> None:
        def task() -> None:
            info = get_wifi_info()
            self.after(0, lambda: self._update_info(info))

        threading.Thread(target=task, daemon=True).start()

    def _update_info(self, info) -> None:
        self._info_labels["ssid"].config(text=info.ssid)
        self._info_labels["signal"].config(text=info.signal)
        self._info_labels["ip"].config(text=info.ip)
        self._info_labels["gateway"].config(text=info.gateway)

    def start_test(self) -> None:
        if self._testing:
            return
        self._testing = True
        self._start_btn.config(state="disabled", text="测速中...")
        self._progress["value"] = 0
        self._server_label.config(text="")
        for key in self._speed_cards:
            self._speed_cards[key]["value"].config(text="--")

        def task() -> None:
            try:
                result = run_speed_test(
                    on_status=lambda msg: self.after(0, lambda m=msg: self._status_label.config(text=m)),
                    on_progress=lambda stage, pct: self.after(0, lambda p=pct: self._progress.configure(value=p)),
                )
                self.after(0, lambda: self._show_result(result))
            except Exception as exc:
                self.after(0, lambda: self._show_error(str(exc)))
            finally:
                self.after(0, self._test_finished)

        threading.Thread(target=task, daemon=True).start()

    def _show_result(self, result) -> None:
        self._speed_cards["ping"]["value"].config(text=str(result.ping_ms))
        self._speed_cards["download"]["value"].config(text=str(result.download_mbps))
        self._speed_cards["upload"]["value"].config(text=str(result.upload_mbps))
        self._status_label.config(text="测试完成！")
        self._server_label.config(
            text=f"服务器: {result.server_name} ({result.server_location}) · ISP: {result.isp}"
        )

    def _show_error(self, message: str) -> None:
        self._status_label.config(text=f"测试失败: {message}")

    def _test_finished(self) -> None:
        self._testing = False
        self._start_btn.config(state="normal", text="▶  开始测速")


def main() -> None:
    app = WiFiSpeedApp()
    app.mainloop()


if __name__ == "__main__":
    main()
