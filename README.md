<p align="center"><img src="assets/covers/40-wifi-speed-test.jpg" alt="WiFi 测速 项目封面" width="100%"></p>

<h1 align="center">WiFi 网速测试</h1>

<p align="center">Windows 桌面测速小工具：看当前 Wi-Fi 信息，一键测延迟、下行与上行</p>

<p align="center">
  <a href="LICENSE">MIT 许可</a>
</p>

## 简介

双击就能用的测速软件：先显示当前连接的 Wi-Fi 名称、信号强度、本机 IP 和网关，再点一下测速，把 Ping、下载、上传三项结果摆出来。基于 speedtest.net 的全球节点，结果可比性较好。

## 功能

- **Wi-Fi 信息**：当前 SSID、信号强度、本机 IP、网关
- **一键测速**：延迟（Ping）、下载速度、上传速度
- **深色界面**：Tkinter 写的单窗口布局，信息分区清晰
- **真实节点**：调用 speedtest.net 测速节点，不做过场动画
- **一键启动**：附带 `启动测速.bat`，不必记命令

## 技术栈

Python 3.9+ · Tkinter（Windows 自带）· speedtest-cli ｜ 网络信息取 `netsh` / `ipconfig`

## 快速开始

```bash
git clone https://github.com/aiyangdie/wifi-speed-test.git
cd wifi-speed-test
pip install -r requirements.txt
python main.py
```

或直接双击 `启动测速.bat`。

## 项目结构

```
main.py            主程序（GUI 与测速流程）
network_info.py    Windows 网络信息获取
speed_test.py      测速核心逻辑
requirements.txt   依赖
启动测速.bat        一键启动
```

## 说明

测速结果受节点、时段与线路影响，同一网络多次测量取中位数更可靠。

## 许可证

[MIT](LICENSE) ｜ 作者 [@aiyangdie](https://github.com/aiyangdie) · aike1015@qq.com
