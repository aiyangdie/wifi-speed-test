# WiFi 网速测试软件

一款简洁美观的 Windows WiFi / 网络测速工具，由 **艾阳** 开发并开源。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## 功能特性

- 📶 **WiFi 信息展示** — 显示当前连接的 WiFi 名称、信号强度、本机 IP、网关
- ⚡ **一键测速** — 测试延迟 (Ping)、下载速度、上传速度
- 🎨 **现代化界面** — 深色主题，简洁直观
- 🌐 **基于 speedtest.net** — 使用全球测速节点，结果准确可靠

## 环境要求

- Windows 10 / 11
- Python 3.9 或更高版本

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/aiyangdie/wifi-speed-test.git
cd wifi-speed-test
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行

```bash
python main.py
```

也可以双击 `启动测速.bat` 一键启动。

## 项目结构

```
├── main.py           # 主程序（GUI 界面）
├── network_info.py   # Windows 网络信息获取
├── speed_test.py     # 测速核心逻辑
├── requirements.txt  # Python 依赖
├── 启动测速.bat      # 一键启动脚本
├── LICENSE           # MIT 开源协议
└── README.md         # 项目说明
```

## 技术栈

| 组件 | 说明 |
|------|------|
| Python + Tkinter | 跨平台 GUI（Windows 内置） |
| speedtest-cli | speedtest.net 官方 Python 库 |
| netsh / ipconfig | Windows 原生网络信息 |

## 作者

- **艾阳** — [GitHub @aiyangdie](https://github.com/aiyangdie)
- 邮箱: aike1015@qq.com

## 开源协议

本项目采用 [MIT License](LICENSE) 开源，可自由使用、修改和分发。

## 贡献

欢迎提交 Issue 和 Pull Request！
