# ⏱ CountTime - 多功能桌面计时器

![Python](https://img.shields.io/badge/Python-3.13+-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.11-green)
![License](https://img.shields.io/badge/License-MIT-orange)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

**CountTime** 是一款基于 PyQt5 构建的桌面计时器应用，支持 **6 种计时模式**、完整菜单栏操作、历史记录管理、配置保存/加载等丰富功能。深色主题设计，键盘快捷键支持，适合工作、学习、运动等多种场景。

---

## ✨ 功能特性

### 🎯 6 种计时模式

| 模式 | 说明 |
|------|------|
| **正计时** | 从 00:00:00 开始递增计时 |
| **倒计时** | 自定义时长，递减至零 |
| **番茄钟** | 25 分钟工作 / 5 分钟休息循环 |
| **间隔循环** | 自定义工作/休息时长交替 |
| **多段分段** | 按顺序执行多段不同时长的计时 |
| **秒表模式** | 精确计时，支持计次记录 |

### 🎮 操作方式

- **按钮控制**：开始（绿色）、暂停（橙色）、计次（蓝色）、重置（红色）
- **键盘快捷键**：`Space` 开始/暂停、`R` 重置、`L` 计次
- **菜单栏**：完整的菜单系统，覆盖所有功能入口

### 📊 数据管理

- 计时记录自动保存至 `config/history.json`
- 支持按日期筛选、批量删除历史记录
- 支持导出为 CSV 格式
- 支持计时配置的保存与加载（JSON）

### 🎨 界面定制

- 深色主题（默认）/ 浅色主题切换
- 字体大小与颜色自定义
- 时间格式切换（支持毫秒显示）
- 窗口置顶 / 全屏模式

### 🔔 辅助功能

- 计时完成提醒（系统音效）
- 后台运行模式
- 番茄钟自动循环
- 多任务计时（开发中）

---

## 🖥️ 界面预览

```
┌─────────────────────────────────────────────┐
│  文件  控制  模式  设置  历史记录  工具  帮助  │
├─────────────────────────────────────────────┤
│             正计时模式                        │
│                                             │
│             00:00:00                         │
│                                             │
│         ⏸ 已暂停  |  按 Space 开始           │
│                                             │
│      [▶ 开始] [⏸ 暂停] [⏱ 计次] [↺ 重置]    │
│                                             │
│  ☐ 窗口置顶          快捷键: Space/R/L       │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ 计次 #01  总: 00:01:23  单次: 00:01:23│   │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 方式一：直接运行（推荐）

确保已安装 Python 3.13+ 和 PyQt5：

```bash
# 安装依赖
pip install PyQt5

# 启动计时器
python main.py
```

### 方式二：使用启动脚本

双击 `start.bat`，脚本会自动检测环境并启动。

### 方式三：编译为 EXE

使用 PyInstaller 编译为独立可执行文件：

```bash
pip install pyinstaller
pyinstaller CountTime.spec
```

编译后的 exe 位于 `dist/CountTime/CountTime.exe`。

---

## 📁 项目结构

```
CountTime/
├── main.py                  # 主程序入口（~1200 行）
├── start.bat                # Windows 启动脚本
├── CountTime.spec           # PyInstaller 编译配置
├── config/
│   ├── settings.json        # 用户设置（自动生成）
│   └── history.json         # 计时历史记录（自动生成）
├── build/                   # PyInstaller 构建缓存
├── dist/                    # 编译输出目录
└── PRD/
    └── CountTime-计时器需求文档.md
```

---

## ⌨️ 快捷键一览

| 快捷键 | 功能 |
|--------|------|
| `Space` | 开始 / 暂停 |
| `R` | 重置 |
| `L` | 计次（正计时/秒表模式） |
| `Ctrl+N` | 新建计时 |
| `Ctrl+S` | 保存配置 |
| `Ctrl+O` | 加载配置 |
| `Ctrl+Q` | 退出程序 |
| `Ctrl+H` | 查看历史记录 |
| `Ctrl+R` | 归零 |
| `F1` | 使用说明 |
| `F11` | 全屏切换 |
| `Ctrl+U` | 正计时模式 |
| `Ctrl+D` | 倒计时模式 |
| `Ctrl+P` | 番茄钟模式 |
| `Ctrl+I` | 间隔循环模式 |
| `Ctrl+Shift+S` | 多段分段模式 |
| `Ctrl+W` | 秒表模式 |

---

## ⚙️ 配置说明

用户设置自动保存至 `config/settings.json`：

```json
{
  "show_milliseconds": false,
  "theme": "dark",
  "font_size": 72,
  "font_color": "#00ff88",
  "sound_enabled": true,
  "vibration_enabled": false,
  "always_on_top": false,
  "auto_start": false
}
```

---

## 🛠️ 技术栈

| 技术 | 版本 |
|------|------|
| Python | 3.13+ |
| PyQt5 | 5.15.11 |
| PyInstaller | (可选，用于编译) |

---

## 📝 开发说明

### 代码结构

`main.py` 包含完整的应用逻辑，主要类：

- **`TimerMode`** - 计时模式常量定义
- **`CountTime`** - 主窗口类，包含：
  - UI 初始化（`_init_ui`）
  - 菜单栏构建（`_init_menu`）
  - 计时逻辑（`_on_tick`、`_on_start`、`_on_pause` 等）
  - 数据持久化（`_save_settings`、`_save_history`）
  - 模式切换（`_on_switch_mode`）
  - 历史记录管理（查看、筛选、批量删除、统计）

### 扩展指南

如需添加新的计时模式：

1. 在 `TimerMode` 类中添加模式常量
2. 在 `_init_menu` 的模式菜单中添加菜单项
3. 在 `_on_switch_mode` 中添加模式初始化逻辑
4. 在 `_on_tick` 中添加该模式的计时逻辑

---

## 📄 License

MIT License

---

