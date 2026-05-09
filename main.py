"""
CountTime - 基于 PyQt5 的计时器应用
功能：开始/暂停/重置/计次计时，支持键盘快捷键，完整菜单栏
"""

import sys
import csv
import json
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QCheckBox,
    QFrame, QAbstractItemView, QMenuBar, QAction, QFileDialog,
    QMessageBox, QDialog, QDialogButtonBox, QComboBox, QSpinBox,
    QFormLayout, QTabWidget, QGroupBox, QRadioButton, QButtonGroup,
    QSlider, QLineEdit, QDateEdit, QTimeEdit
)
from PyQt5.QtCore import QTimer, Qt, QDate
from PyQt5.QtGui import QFont, QKeySequence, QIcon, QPixmap, QColor


class TimerMode:
    """计时模式常量"""
    COUNT_UP = "count_up"
    COUNT_DOWN = "count_down"
    POMODORO = "pomodoro"
    INTERVAL = "interval"
    MULTI_SEGMENT = "multi_segment"
    STOPWATCH = "stopwatch"


class CountTime(QMainWindow):
    """主计时器窗口"""

    STYLE_SHEET = """
        QMainWindow { background-color: #1a1a2e; }
        QMenuBar {
            background-color: #16213e; color: #cccccc;
            border-bottom: 1px solid #0f3460; font-size: 13px; padding: 2px;
        }
        QMenuBar::item { padding: 4px 12px; background: transparent; }
        QMenuBar::item:selected { background-color: #0f3460; border-radius: 4px; }
        QMenu {
            background-color: #16213e; color: #ffffff;
            border: 1px solid #0f3460; border-radius: 6px; padding: 4px;
        }
        QMenu::item { padding: 6px 24px 6px 16px; border-radius: 4px; color: #ffffff; }
        QMenu::item:selected { background-color: #0f3460; color: #00ff88; }
        QMenu::separator { height: 1px; background-color: #0f3460; margin: 4px 8px; }
        QMenu::indicator { width: 13px; height: 13px; }
        QLabel#timeDisplay {
            color: #00ff88; background-color: #16213e;
            border: 2px solid #0f3460; border-radius: 15px; padding: 20px;
            font-size: 72px; font-weight: bold;
            font-family: 'Consolas', 'Courier New', monospace;
        }
        QPushButton { font-size: 13px; font-weight: bold; padding: 8px 20px; border-radius: 6px; border: none; min-width: 70px; }
        QPushButton#btnStart { background-color: #00c853; color: white; }
        QPushButton#btnStart:hover { background-color: #00e676; }
        QPushButton#btnPause { background-color: #ff6d00; color: white; }
        QPushButton#btnPause:hover { background-color: #ff9100; }
        QPushButton#btnReset { background-color: #d50000; color: white; }
        QPushButton#btnReset:hover { background-color: #ff1744; }
        QPushButton#btnLap { background-color: #2979ff; color: white; }
        QPushButton#btnLap:hover { background-color: #448aff; }
        QPushButton#btnLap:disabled { background-color: #555555; color: #888888; }
        QLabel#statusLabel { color: #aaaaaa; font-size: 14px; }
        QLabel#shortcutLabel { color: #666666; font-size: 12px; }
        QListWidget {
            background-color: #16213e; border: 1px solid #0f3460;
            border-radius: 8px; color: #ffffff; font-size: 14px;
            font-family: 'Consolas', 'Courier New', monospace; padding: 5px;
        }
        QListWidget::item { padding: 4px 8px; border-bottom: 1px solid #0f3460; color: #ffffff; }
        QListWidget::item:last { border-bottom: none; }
        QCheckBox { color: #ffffff; font-size: 13px; spacing: 6px; }
        QCheckBox::indicator { width: 16px; height: 16px; border-radius: 3px; border: 2px solid #0f3460; background-color: #16213e; }
        QCheckBox::indicator:checked { background-color: #2979ff; border-color: #2979ff; }
        QDialog { background-color: #1a1a2e; color: #ffffff; }
        QDialog QLabel { color: #ffffff; }
        QDialog QLabel#sectionTitle { color: #00ff88; }
        QDialog QGroupBox { color: #00ff88; }
        QDialog QGroupBox QLabel { color: #cccccc; }
        QDialog QPushButton { color: #ffffff; }
        QDialog QCheckBox { color: #ffffff; }
        QDialog QRadioButton { color: #ffffff; }
        QDialog QComboBox { color: #ffffff; background-color: #16213e; }
        QDialog QSpinBox { color: #ffffff; background-color: #16213e; }
        QDialog QLineEdit { color: #ffffff; background-color: #16213e; }
        QDialog QDateEdit { color: #ffffff; background-color: #16213e; }
        QDialog QTimeEdit { color: #ffffff; background-color: #16213e; }
        QDialog QListWidget { color: #ffffff; background-color: #16213e; }
        QDialog QListWidget::item { color: #ffffff; }
        QDialogButtonBox QPushButton {
            color: #ffffff; background-color: #0f3460;
            border: 1px solid #2979ff; border-radius: 4px;
            padding: 6px 16px; min-width: 60px;
        }
        QDialogButtonBox QPushButton:hover { background-color: #2979ff; }
        QGroupBox { color: #00ff88; border: 1px solid #0f3460; border-radius: 6px; margin-top: 10px; padding-top: 10px; font-size: 13px; font-weight: bold; }
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        QComboBox { background-color: #16213e; color: #ffffff; border: 1px solid #0f3460; border-radius: 4px; padding: 4px 8px; font-size: 13px; }
        QComboBox::drop-down { border: none; }
        QComboBox QAbstractItemView { background-color: #16213e; color: #ffffff; border: 1px solid #0f3460; selection-background-color: #0f3460; }
        QSpinBox, QTimeEdit, QDateEdit, QLineEdit { background-color: #16213e; color: #ffffff; border: 1px solid #0f3460; border-radius: 4px; padding: 4px 8px; font-size: 13px; }
        QSlider::groove:horizontal { height: 6px; background: #16213e; border-radius: 3px; }
        QSlider::handle:horizontal { background: #2979ff; width: 16px; height: 16px; margin: -5px 0; border-radius: 8px; }
        QSlider::sub-page:horizontal { background: #00ff88; border-radius: 3px; }
        QRadioButton { color: #ffffff; font-size: 13px; spacing: 6px; }
        QRadioButton::indicator { width: 14px; height: 14px; border-radius: 7px; border: 2px solid #0f3460; background-color: #16213e; }
        QRadioButton::indicator:checked { background-color: #00ff88; border-color: #00ff88; }
        QLabel#sectionTitle { color: #00ff88; font-size: 16px; font-weight: bold; padding: 8px 0; }
    """

    def __init__(self):
        super().__init__()
        self._init_data()
        self._init_ui()
        self._init_menu()

    def _init_data(self):
        """初始化数据"""
        self._running = False
        self._elapsed_seconds = 0
        self._lap_count = 0
        self._lap_times = []
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)

        self._mode = TimerMode.COUNT_UP
        self._countdown_target = 0
        self._pomodoro_work = 25 * 60
        self._pomodoro_break = 5 * 60
        self._pomodoro_phase = "work"
        self._pomodoro_count = 0
        self._interval_work = 30
        self._interval_rest = 10
        self._interval_phase = "work"
        self._loop_enabled = False
        self._segments = []
        self._current_segment = 0

        self._show_milliseconds = False
        self._theme = "dark"
        self._font_size = 72
        self._font_color = "#00ff88"
        self._sound_enabled = True
        self._vibration_enabled = False
        self._always_on_top = False
        self._auto_start = False

        self._history = []

        self._config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
        self._history_file = os.path.join(self._config_dir, "history.json")
        self._config_file = os.path.join(self._config_dir, "settings.json")
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        os.makedirs(self._config_dir, exist_ok=True)
        self._load_history()
        self._load_settings()

    def _load_settings(self):
        try:
            if os.path.exists(self._config_file):
                with open(self._config_file, "r", encoding="utf-8") as f:
                    s = json.load(f)
                    self._show_milliseconds = s.get("show_milliseconds", False)
                    self._theme = s.get("theme", "dark")
                    self._font_size = s.get("font_size", 72)
                    self._font_color = s.get("font_color", "#00ff88")
                    self._sound_enabled = s.get("sound_enabled", True)
                    self._vibration_enabled = s.get("vibration_enabled", False)
                    self._always_on_top = s.get("always_on_top", False)
                    self._auto_start = s.get("auto_start", False)
        except Exception:
            pass

    def _save_settings(self):
        try:
            with open(self._config_file, "w", encoding="utf-8") as f:
                json.dump({
                    "show_milliseconds": self._show_milliseconds,
                    "theme": self._theme, "font_size": self._font_size,
                    "font_color": self._font_color, "sound_enabled": self._sound_enabled,
                    "vibration_enabled": self._vibration_enabled,
                    "always_on_top": self._always_on_top, "auto_start": self._auto_start,
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存设置失败: {e}")

    def _load_history(self):
        try:
            if os.path.exists(self._history_file):
                with open(self._history_file, "r", encoding="utf-8") as f:
                    self._history = json.load(f)
        except Exception:
            self._history = []

    def _save_history(self):
        try:
            with open(self._history_file, "w", encoding="utf-8") as f:
                json.dump(self._history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")

    def _init_ui(self):
        self.setWindowTitle("CountTime 计时器")
        self.setFixedSize(560, 560)
        self.setStyleSheet(self.STYLE_SHEET)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 10, 24, 20)

        self._mode_label = QLabel("正计时模式")
        self._mode_label.setObjectName("sectionTitle")
        self._mode_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._mode_label)

        self._time_label = QLabel("00:00:00")
        self._time_label.setObjectName("timeDisplay")
        self._time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._time_label)

        self._status_label = QLabel("⏸ 已暂停  |  按 Space 开始")
        self._status_label.setObjectName("statusLabel")
        self._status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._status_label)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(18)

        self._btn_start = QPushButton("▶ 开始")
        self._btn_start.setObjectName("btnStart")
        self._btn_start.clicked.connect(self._on_start)

        self._btn_pause = QPushButton("⏸ 暂停")
        self._btn_pause.setObjectName("btnPause")
        self._btn_pause.clicked.connect(self._on_pause)
        self._btn_pause.setEnabled(False)

        self._btn_lap = QPushButton("⏱ 计次")
        self._btn_lap.setObjectName("btnLap")
        self._btn_lap.clicked.connect(self._on_lap)
        self._btn_lap.setEnabled(False)

        self._btn_reset = QPushButton("↺ 重置")
        self._btn_reset.setObjectName("btnReset")
        self._btn_reset.clicked.connect(self._on_reset)

        btn_layout.addStretch()
        btn_layout.addWidget(self._btn_start)
        btn_layout.addWidget(self._btn_pause)
        btn_layout.addWidget(self._btn_lap)
        btn_layout.addWidget(self._btn_reset)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        option_layout = QHBoxLayout()
        self._cb_topmost = QCheckBox("窗口置顶")
        self._cb_topmost.stateChanged.connect(self._on_topmost_changed)
        option_layout.addWidget(self._cb_topmost)
        option_layout.addStretch()

        shortcut_label = QLabel("快捷键: Space=开始/暂停  R=重置  L=计次")
        shortcut_label.setObjectName("shortcutLabel")
        option_layout.addWidget(shortcut_label)
        layout.addLayout(option_layout)

        self._lap_list = QListWidget()
        self._lap_list.setMaximumHeight(160)
        self._lap_list.setSelectionMode(QAbstractItemView.NoSelection)
        layout.addWidget(self._lap_list)

    def _init_menu(self):
        menubar = self.menuBar()

        # 文件菜单
        fm = menubar.addMenu("文件(&F)")
        a = QAction("新建计时(&N)", self)
        a.setShortcut(QKeySequence("Ctrl+N"))
        a.triggered.connect(self._on_new_timer)
        fm.addAction(a)
        fm.addSeparator()
        a = QAction("保存计时配置(&S)", self)
        a.setShortcut(QKeySequence("Ctrl+S"))
        a.triggered.connect(self._on_save_config)
        fm.addAction(a)
        a = QAction("加载历史配置(&L)", self)
        a.setShortcut(QKeySequence("Ctrl+O"))
        a.triggered.connect(self._on_load_config)
        fm.addAction(a)
        fm.addSeparator()
        em = fm.addMenu("导出记录")
        a = QAction("导出为 CSV", self)
        a.triggered.connect(lambda: self._on_export("csv"))
        em.addAction(a)
        a = QAction("导出为 Excel", self)
        a.triggered.connect(lambda: self._on_export("excel"))
        em.addAction(a)
        fm.addSeparator()
        a = QAction("退出程序(&X)", self)
        a.setShortcut(QKeySequence("Ctrl+Q"))
        a.triggered.connect(self.close)
        fm.addAction(a)

        # 控制菜单
        cm = menubar.addMenu("控制(&C)")
        self._menu_start = QAction("开始", self)
        self._menu_start.setShortcut(QKeySequence("Space"))
        self._menu_start.triggered.connect(self._on_start)
        cm.addAction(self._menu_start)
        self._menu_pause = QAction("暂停", self)
        self._menu_pause.setShortcut(QKeySequence("Space"))
        self._menu_pause.triggered.connect(self._on_pause)
        self._menu_pause.setEnabled(False)
        cm.addAction(self._menu_pause)
        self._menu_continue = QAction("继续", self)
        self._menu_continue.setShortcut(QKeySequence("Space"))
        self._menu_continue.triggered.connect(self._on_start)
        self._menu_continue.setEnabled(False)
        cm.addAction(self._menu_continue)
        cm.addSeparator()
        a = QAction("重置(&R)", self)
        a.setShortcut(QKeySequence("R"))
        a.triggered.connect(self._on_reset)
        cm.addAction(a)
        a = QAction("归零", self)
        a.setShortcut(QKeySequence("Ctrl+R"))
        a.triggered.connect(self._on_zero)
        cm.addAction(a)
        cm.addSeparator()
        self._menu_loop = QAction("循环计时", self)
        self._menu_loop.setCheckable(True)
        self._menu_loop.triggered.connect(self._on_toggle_loop)
        cm.addAction(self._menu_loop)
        a = QAction("全屏计时", self)
        a.setShortcut(QKeySequence("F11"))
        a.triggered.connect(self._on_fullscreen)
        cm.addAction(a)

        # 模式菜单
        mm = menubar.addMenu("模式(&M)")
        self._mode_actions = {}
        for text, mid, sc in [
            ("正计时(&U)", TimerMode.COUNT_UP, "Ctrl+U"),
            ("倒计时(&D)", TimerMode.COUNT_DOWN, "Ctrl+D"),
            ("番茄钟模式(&P)", TimerMode.POMODORO, "Ctrl+P"),
            ("间隔循环计时(&I)", TimerMode.INTERVAL, "Ctrl+I"),
            ("多段分段计时(&S)", TimerMode.MULTI_SEGMENT, "Ctrl+Shift+S"),
            ("秒表模式(&W)", TimerMode.STOPWATCH, "Ctrl+W"),
        ]:
            a = QAction(text, self)
            a.setCheckable(True)
            if sc:
                a.setShortcut(QKeySequence(sc))
            a.triggered.connect(lambda checked, m=mid: self._on_switch_mode(m))
            mm.addAction(a)
            self._mode_actions[mid] = a
        self._mode_actions[TimerMode.COUNT_UP].setChecked(True)

        # 设置菜单
        sm = menubar.addMenu("设置(&S)")
        a = QAction("时间格式设置...", self)
        a.triggered.connect(self._on_time_format_settings)
        sm.addAction(a)
        tm = sm.addMenu("外观主题")
        a = QAction("浅色", self)
        a.triggered.connect(lambda: self._on_set_theme("light"))
        tm.addAction(a)
        a = QAction("深色", self)
        a.triggered.connect(lambda: self._on_set_theme("dark"))
        tm.addAction(a)
        a = QAction("自定义...", self)
        a.triggered.connect(self._on_custom_theme)
        tm.addAction(a)
        a = QAction("字体大小/颜色调整...", self)
        a.triggered.connect(self._on_font_settings)
        sm.addAction(a)
        sm.addSeparator()
        sm2 = sm.addMenu("提醒音效选择")
        a = QAction("无音效", self)
        a.triggered.connect(lambda: self._on_set_sound("none"))
        sm2.addAction(a)
        a = QAction("默认音效", self)
        a.triggered.connect(lambda: self._on_set_sound("default"))
        sm2.addAction(a)
        a = QAction("自定义音效...", self)
        a.triggered.connect(self._on_custom_sound)
        sm2.addAction(a)
        self._menu_vibration = QAction("震动提醒", self)
        self._menu_vibration.setCheckable(True)
        self._menu_vibration.triggered.connect(self._on_toggle_vibration)
        sm.addAction(self._menu_vibration)
        sm.addSeparator()
        self._menu_topmost = QAction("置顶窗口", self)
        self._menu_topmost.setCheckable(True)
        self._menu_topmost.triggered.connect(self._on_toggle_topmost)
        sm.addAction(self._menu_topmost)
        self._menu_autostart = QAction("开机自启", self)
        self._menu_autostart.setCheckable(True)
        self._menu_autostart.triggered.connect(self._on_toggle_autostart)
        sm.addAction(self._menu_autostart)
        sm.addSeparator()
        a = QAction("快捷键设置...", self)
        a.triggered.connect(self._on_shortcut_settings)
        sm.addAction(a)

        # 历史记录菜单
        hm = menubar.addMenu("历史记录(&H)")
        a = QAction("查看所有计时记录", self)
        a.setShortcut(QKeySequence("Ctrl+H"))
        a.triggered.connect(self._on_view_history)
        hm.addAction(a)
        hm.addSeparator()
        a = QAction("清空记录", self)
        a.triggered.connect(self._on_clear_history)
        hm.addAction(a)
        a = QAction("按日期筛选...", self)
        a.triggered.connect(self._on_filter_history)
        hm.addAction(a)
        a = QAction("批量删除...", self)
        a.triggered.connect(self._on_batch_delete)
        hm.addAction(a)
        hm.addSeparator()
        a = QAction("统计时长汇总", self)
        a.triggered.connect(self._on_show_stats)
        hm.addAction(a)

        # 工具菜单
        tm = menubar.addMenu("工具(&T)")
        a = QAction("批量倒计时...", self)
        a.triggered.connect(self._on_batch_timer)
        tm.addAction(a)
        a = QAction("多任务同时计时...", self)
        a.triggered.connect(self._on_multi_task)
        tm.addAction(a)
        tm.addSeparator()
        a = QAction("时间校准", self)
        a.triggered.connect(self._on_calibrate)
        tm.addAction(a)
        self._menu_background = QAction("后台运行", self)
        self._menu_background.setCheckable(True)
        self._menu_background.triggered.connect(self._on_toggle_background)
        tm.addAction(self._menu_background)

        # 帮助菜单
        hm = menubar.addMenu("帮助(&A)")
        a = QAction("使用说明(&U)", self)
        a.setShortcut(QKeySequence("F1"))
        a.triggered.connect(self._on_show_usage)
        hm.addAction(a)
        hm.addSeparator()
        a = QAction("关于我们(&A)", self)
        a.triggered.connect(self._on_show_about)
        hm.addAction(a)
        a = QAction("检查更新(&C)", self)
        a.triggered.connect(self._on_check_update)
        hm.addAction(a)
        a = QAction("反馈建议(&F)", self)
        a.triggered.connect(self._on_feedback)
        hm.addAction(a)

    def _format_time(self, total_seconds: int, show_ms: bool = False) -> str:
        if show_ms:
            h = total_seconds // 3600
            m = (total_seconds % 3600) // 60
            s = total_seconds % 60
            return f"{h:02d}:{m:02d}:{s:02d}.00"
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def _update_display(self):
        self._time_label.setText(self._format_time(self._elapsed_seconds, self._show_milliseconds))

    def _update_mode_label(self):
        names = {
            TimerMode.COUNT_UP: "正计时模式", TimerMode.COUNT_DOWN: "倒计时模式",
            TimerMode.POMODORO: "番茄钟模式", TimerMode.INTERVAL: "间隔循环计时",
            TimerMode.MULTI_SEGMENT: "多段分段计时", TimerMode.STOPWATCH: "秒表模式",
        }
        self._mode_label.setText(names.get(self._mode, "计时模式"))

    def _on_tick(self):
        if self._mode == TimerMode.COUNT_DOWN:
            self._elapsed_seconds -= 1
            if self._elapsed_seconds <= 0:
                self._elapsed_seconds = 0
                self._on_timer_complete()
        elif self._mode == TimerMode.POMODORO:
            self._elapsed_seconds -= 1
            if self._elapsed_seconds <= 0:
                self._on_pomodoro_phase_complete()
        elif self._mode == TimerMode.INTERVAL:
            self._elapsed_seconds -= 1
            if self._elapsed_seconds <= 0:
                self._on_interval_phase_complete()
        elif self._mode == TimerMode.MULTI_SEGMENT:
            self._elapsed_seconds -= 1
            if self._elapsed_seconds <= 0:
                self._on_segment_complete()
        else:
            self._elapsed_seconds += 1
        self._update_display()

    def _on_timer_complete(self):
        self._timer.stop()
        self._running = False
        self._update_button_states()
        self._status_label.setText("⏰ 计时完成！")
        self._add_history_record(self._mode, 0, "计时完成")
        self._save_history()
        self._show_notification("计时完成", "倒计时已结束！")

    def _on_pomodoro_phase_complete(self):
        if self._pomodoro_phase == "work":
            self._pomodoro_count += 1
            self._pomodoro_phase = "break"
            self._elapsed_seconds = self._pomodoro_break
            self._status_label.setText(f"🍅 番茄 #{self._pomodoro_count} 完成，休息 {self._pomodoro_break//60} 分钟")
            self._show_notification("番茄钟", f"番茄 #{self._pomodoro_count} 完成！开始休息")
        else:
            self._pomodoro_phase = "work"
            self._elapsed_seconds = self._pomodoro_work
            self._status_label.setText(f"🍅 休息结束，开始番茄 #{self._pomodoro_count + 1}")
            self._show_notification("番茄钟", "休息结束，开始新的番茄！")
        if not self._loop_enabled:
            self._timer.stop()
            self._running = False
            self._update_button_states()

    def _on_interval_phase_complete(self):
        if self._interval_phase == "work":
            self._interval_phase = "rest"
            self._elapsed_seconds = self._interval_rest
            self._status_label.setText(f"⏳ 工作完成，休息 {self._interval_rest} 秒")
        else:
            self._interval_phase = "work"
            self._elapsed_seconds = self._interval_work
            self._status_label.setText(f"⏳ 休息结束，工作 {self._interval_work} 秒")
        if not self._loop_enabled:
            self._timer.stop()
            self._running = False
            self._update_button_states()

    def _on_segment_complete(self):
        self._current_segment += 1
        if self._current_segment < len(self._segments):
            name, seconds = self._segments[self._current_segment]
            self._elapsed_seconds = seconds
            self._status_label.setText(f"📋 当前段: {name} ({self._format_time(seconds)})")
        else:
            self._timer.stop()
            self._running = False
            self._update_button_states()
            self._status_label.setText("✅ 所有分段完成！")
            self._show_notification("分段计时", "所有分段计时已完成！")

    def _on_start(self):
        if not self._running:
            if self._mode == TimerMode.COUNT_DOWN and self._countdown_target <= 0:
                self._on_set_countdown()
                return
            if self._mode == TimerMode.POMODORO and self._elapsed_seconds <= 0:
                self._elapsed_seconds = self._pomodoro_work
                self._pomodoro_phase = "work"
            if self._mode == TimerMode.INTERVAL and self._elapsed_seconds <= 0:
                self._elapsed_seconds = self._interval_work
                self._interval_phase = "work"
            if self._mode == TimerMode.MULTI_SEGMENT and self._elapsed_seconds <= 0 and self._segments:
                self._current_segment = 0
                name, seconds = self._segments[0]
                self._elapsed_seconds = seconds
                self._status_label.setText(f"📋 当前段: {name} ({self._format_time(seconds)})")
            self._timer.start(1000)
            self._running = True
            self._update_button_states()
            self._status_label.setText("▶ 计时中...  |  按 Space 暂停")

    def _on_pause(self):
        if self._running:
            self._timer.stop()
            self._running = False
            self._update_button_states()
            self._status_label.setText("⏸ 已暂停  |  按 Space 继续")

    def _on_lap(self):
        if self._running:
            self._lap_count += 1
            self._lap_times.append(self._elapsed_seconds)
            ld = self._elapsed_seconds if self._lap_count == 1 else self._elapsed_seconds - self._lap_times[-2]
            item = QListWidgetItem(f"计次 #{self._lap_count:02d}   总: {self._format_time(self._elapsed_seconds)}   单次: {self._format_time(ld)}")
            self._lap_list.insertItem(0, item)

    def _on_reset(self):
        self._timer.stop()
        self._running = False
        self._elapsed_seconds = 0
        self._lap_count = 0
        self._lap_times.clear()
        self._update_display()
        self._update_button_states()
        self._lap_list.clear()
        self._status_label.setText("↺ 已重置  |  按 Space 开始")

    def _on_zero(self):
        self._on_reset()
        self._pomodoro_count = 0
        self._pomodoro_phase = "work"
        self._interval_phase = "work"
        self._current_segment = 0
        self._status_label.setText("↺ 已归零  |  按 Space 开始")

    def _update_button_states(self):
        self._btn_start.setEnabled(not self._running)
        self._btn_pause.setEnabled(self._running)
        self._btn_lap.setEnabled(self._running and self._mode in [TimerMode.COUNT_UP, TimerMode.STOPWATCH])
        self._menu_start.setEnabled(not self._running)
        self._menu_pause.setEnabled(self._running)
        self._menu_continue.setEnabled(not self._running and self._elapsed_seconds > 0)

    def _on_new_timer(self):
        self._on_reset()
        self._mode = TimerMode.COUNT_UP
        self._update_mode_label()
        self._update_display()
        self._status_label.setText("↺ 新建计时  |  按 Space 开始")

    def _on_save_config(self):
        fp, _ = QFileDialog.getSaveFileName(self, "保存计时配置", self._config_dir, "JSON 文件 (*.json)")
        if fp:
            try:
                with open(fp, "w", encoding="utf-8") as f:
                    json.dump({
                        "mode": self._mode, "elapsed_seconds": self._elapsed_seconds,
                        "countdown_target": self._countdown_target,
                        "pomodoro_work": self._pomodoro_work, "pomodoro_break": self._pomodoro_break,
                        "interval_work": self._interval_work, "interval_rest": self._interval_rest,
                        "loop_enabled": self._loop_enabled, "segments": self._segments,
                    }, f, ensure_ascii=False, indent=2)
                self._status_label.setText(f"✅ 配置已保存: {os.path.basename(fp)}")
            except Exception as e:
                QMessageBox.warning(self, "保存失败", f"无法保存配置: {e}")

    def _on_load_config(self):
        fp, _ = QFileDialog.getOpenFileName(self, "加载计时配置", self._config_dir, "JSON 文件 (*.json)")
        if fp:
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    c = json.load(f)
                self._on_reset()
                self._mode = c.get("mode", TimerMode.COUNT_UP)
                self._countdown_target = c.get("countdown_target", 0)
                self._pomodoro_work = c.get("pomodoro_work", 25 * 60)
                self._pomodoro_break = c.get("pomodoro_break", 5 * 60)
                self._interval_work = c.get("interval_work", 30)
                self._interval_rest = c.get("interval_rest", 10)
                self._loop_enabled = c.get("loop_enabled", False)
                self._segments = c.get("segments", [])
                self._update_mode_label()
                self._update_display()
                self._status_label.setText(f"✅ 配置已加载: {os.path.basename(fp)}")
            except Exception as e:
                QMessageBox.warning(self, "加载失败", f"无法加载配置: {e}")

    def _on_export(self, fmt: str):
        if not self._history:
            QMessageBox.information(self, "导出", "暂无历史记录可导出")
            return
        if fmt == "csv":
            fp, _ = QFileDialog.getSaveFileName(self, "导出为 CSV", os.path.join(self._config_dir, "计时记录.csv"), "CSV 文件 (*.csv)")
            if fp:
                try:
                    with open(fp, "w", encoding="utf-8-sig", newline="") as f2:
                        w = csv.writer(f2)
                        w.writerow(["时间", "模式", "时长(秒)", "备注"])
                        for r in self._history:
                            w.writerow([r.get("timestamp", ""), r.get("mode", ""), r.get("duration", 0), r.get("note", "")])
                    self._status_label.setText(f"✅ 已导出 CSV: {os.path.basename(fp)}")
                except Exception as e:
                    QMessageBox.warning(self, "导出失败", str(e))
        else:
            QMessageBox.information(self, "导出", "Excel 导出功能需要安装 openpyxl 库\n请使用 CSV 格式导出")

    def _on_toggle_loop(self, checked: bool):
        self._loop_enabled = checked

    def _on_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _on_switch_mode(self, mode_id: str):
        if self._running:
            self._on_pause()
        self._on_reset()
        self._mode = mode_id
        self._update_mode_label()
        for mid, a in self._mode_actions.items():
            a.setChecked(mid == mode_id)
        self._btn_lap.setVisible(mode_id in [TimerMode.COUNT_UP, TimerMode.STOPWATCH])
        if mode_id == TimerMode.COUNT_DOWN and self._countdown_target > 0:
            self._elapsed_seconds = self._countdown_target
            self._update_display()
            self._status_label.setText(f"⏰ 倒计时 {self._format_time(self._countdown_target)}  |  按 Space 开始")
        elif mode_id == TimerMode.POMODORO:
            self._elapsed_seconds = self._pomodoro_work
            self._update_display()
            self._status_label.setText(f"🍅 番茄钟 {self._pomodoro_work//60} 分工作 / {self._pomodoro_break//60} 分休息")
        elif mode_id == TimerMode.INTERVAL:
            self._elapsed_seconds = self._interval_work
            self._update_display()
            self._status_label.setText(f"⏳ 间隔循环 {self._interval_work}秒工作 / {self._interval_rest}秒休息")
        elif mode_id == TimerMode.MULTI_SEGMENT:
            if self._segments:
                self._current_segment = 0
                name, seconds = self._segments[0]
                self._elapsed_seconds = seconds
                self._update_display()
                self._status_label.setText(f"📋 多段分段: {len(self._segments)} 段")
            else:
                self._on_set_segments()
        elif mode_id == TimerMode.STOPWATCH:
            self._status_label.setText("⏱ 秒表模式  |  按 Space 开始")
        else:
            self._status_label.setText("⏸ 已暂停  |  按 Space 开始")

    def _on_set_countdown(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("设置倒计时")
        dialog.setFixedSize(300, 200)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        h_spin = QSpinBox()
        h_spin.setRange(0, 99)
        m_spin = QSpinBox()
        m_spin.setRange(0, 59)
        m_spin.setValue(25)
        s_spin = QSpinBox()
        s_spin.setRange(0, 59)
        form.addRow("小时:", h_spin)
        form.addRow("分钟:", m_spin)
        form.addRow("秒:", s_spin)
        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        if dialog.exec_() == QDialog.Accepted:
            total = h_spin.value() * 3600 + m_spin.value() * 60 + s_spin.value()
            if total > 0:
                self._countdown_target = total
                self._elapsed_seconds = total
                self._update_display()
                self._status_label.setText(f"⏰ 倒计时 {self._format_time(total)}  |  按 Space 开始")

    def _on_set_segments(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("设置分段计时")
        dialog.setFixedSize(400, 300)
        layout = QVBoxLayout(dialog)
        segment_list = QListWidget()
        layout.addWidget(QLabel("当前分段:"))
        layout.addWidget(segment_list)
        add_layout = QHBoxLayout()
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("分段名称")
        h_spin = QSpinBox()
        h_spin.setRange(0, 99)
        m_spin = QSpinBox()
        m_spin.setRange(0, 59)
        m_spin.setValue(5)
        s_spin = QSpinBox()
        s_spin.setRange(0, 59)
        add_layout.addWidget(name_edit)
        add_layout.addWidget(QLabel("时"))
        add_layout.addWidget(h_spin)
        add_layout.addWidget(QLabel("分"))
        add_layout.addWidget(m_spin)
        add_layout.addWidget(QLabel("秒"))
        add_layout.addWidget(s_spin)

        def add_segment():
            name = name_edit.text().strip() or f"分段 {segment_list.count() + 1}"
            total = h_spin.value() * 3600 + m_spin.value() * 60 + s_spin.value()
            if total > 0:
                segment_list.addItem(f"{name}: {self._format_time(total)}")
                name_edit.clear()
                h_spin.setValue(0)
                m_spin.setValue(5)
                s_spin.setValue(0)

        add_btn = QPushButton("添加")
        add_btn.clicked.connect(add_segment)
        add_layout.addWidget(add_btn)
        layout.addLayout(add_layout)

        def remove_segment():
            row = segment_list.currentRow()
            if row >= 0:
                segment_list.takeItem(row)

        remove_btn = QPushButton("删除选中")
        remove_btn.clicked.connect(remove_segment)
        layout.addWidget(remove_btn)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted:
            self._segments = []
            for i in range(segment_list.count()):
                text = segment_list.item(i).text()
                parts = text.split(": ")
                if len(parts) == 2:
                    name = parts[0]
                    time_str = parts[1]
                    time_parts = time_str.split(":")
                    if len(time_parts) == 3:
                        total = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])
                        self._segments.append((name, total))
            if self._segments:
                self._current_segment = 0
                name, seconds = self._segments[0]
                self._elapsed_seconds = seconds
                self._update_display()
                self._status_label.setText(f"📋 已设置 {len(self._segments)} 个分段")

    def _on_time_format_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("时间格式设置")
        dialog.setFixedSize(300, 150)
        layout = QVBoxLayout(dialog)
        cb = QCheckBox("显示毫秒")
        cb.setChecked(self._show_milliseconds)
        layout.addWidget(cb)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        if dialog.exec_() == QDialog.Accepted:
            self._show_milliseconds = cb.isChecked()
            self._update_display()
            self._save_settings()

    def _on_set_theme(self, theme: str):
        self._theme = theme
        if theme == "light":
            self._time_label.setStyleSheet("color: #1a1a2e; background-color: #f0f0f0; border: 2px solid #cccccc; border-radius: 15px; padding: 20px; font-size: 72px; font-weight: bold; font-family: 'Consolas', 'Courier New', monospace;")
        else:
            self._time_label.setStyleSheet("color: #00ff88; background-color: #16213e; border: 2px solid #0f3460; border-radius: 15px; padding: 20px; font-size: 72px; font-weight: bold; font-family: 'Consolas', 'Courier New', monospace;")
        self._save_settings()

    def _on_custom_theme(self):
        QMessageBox.information(self, "自定义主题", "自定义主题功能开发中...")

    def _on_font_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("字体设置")
        dialog.setFixedSize(350, 200)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        size_spin = QSpinBox()
        size_spin.setRange(24, 120)
        size_spin.setValue(self._font_size)
        form.addRow("字体大小:", size_spin)
        color_edit = QLineEdit(self._font_color)
        form.addRow("颜色 (HEX):", color_edit)
        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        if dialog.exec_() == QDialog.Accepted:
            self._font_size = size_spin.value()
            self._font_color = color_edit.text().strip()
            self._time_label.setStyleSheet(
                f"color: {self._font_color}; background-color: #16213e; "
                f"border: 2px solid #0f3460; border-radius: 15px; padding: 20px; "
                f"font-size: {self._font_size}px; font-weight: bold; "
                f"font-family: 'Consolas', 'Courier New', monospace;"
            )
            self._save_settings()

    def _on_set_sound(self, sound: str):
        self._sound_enabled = sound != "none"
        self._save_settings()

    def _on_custom_sound(self):
        fp, _ = QFileDialog.getOpenFileName(self, "选择音效文件", "", "音频文件 (*.wav *.mp3 *.ogg)")
        if fp:
            self._sound_enabled = True
            self._save_settings()
            self._status_label.setText(f"🔊 已选择音效: {os.path.basename(fp)}")

    def _on_toggle_vibration(self, checked: bool):
        self._vibration_enabled = checked
        self._save_settings()

    def _on_toggle_topmost(self, checked: bool):
        self._always_on_top = checked
        self._cb_topmost.setChecked(checked)
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()
        self._save_settings()

    def _on_toggle_autostart(self, checked: bool):
        self._auto_start = checked
        self._save_settings()
        if checked:
            QMessageBox.information(self, "开机自启", "开机自启功能需要管理员权限\n请手动添加快捷方式到启动文件夹\nWin+R → shell:startup")
        else:
            QMessageBox.information(self, "开机自启", "已关闭开机自启")

    def _on_shortcut_settings(self):
        QMessageBox.information(self, "快捷键设置",
            "当前快捷键:\n\n"
            "Space - 开始/暂停\n"
            "R - 重置\n"
            "L - 计次\n"
            "Ctrl+N - 新建计时\n"
            "Ctrl+S - 保存配置\n"
            "Ctrl+O - 加载配置\n"
            "Ctrl+Q - 退出\n"
            "Ctrl+H - 查看历史\n"
            "F1 - 使用说明\n"
            "F11 - 全屏\n\n"
            "快捷键自定义功能开发中...")

    def _on_view_history(self):
        if not self._history:
            QMessageBox.information(self, "历史记录", "暂无计时记录")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("计时历史记录")
        dialog.resize(500, 400)
        layout = QVBoxLayout(dialog)
        lw = QListWidget()
        for r in reversed(self._history):
            lw.addItem(f"[{r.get('timestamp', '')}] {r.get('mode', '')} - {self._format_time(r.get('duration', 0))} - {r.get('note', '')}")
        layout.addWidget(lw)
        btn = QPushButton("关闭")
        btn.clicked.connect(dialog.close)
        layout.addWidget(btn)
        dialog.exec_()

    def _on_clear_history(self):
        if not self._history:
            QMessageBox.information(self, "清空记录", "暂无记录")
            return
        r = QMessageBox.question(self, "清空记录", "确定要清空所有计时记录吗？", QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            self._history.clear()
            self._save_history()
            self._status_label.setText("🗑 已清空所有记录")

    def _on_filter_history(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("按日期筛选")
        dialog.setFixedSize(300, 150)
        layout = QVBoxLayout(dialog)
        de = QDateEdit()
        de.setCalendarPopup(True)
        de.setDate(QDate.currentDate())
        layout.addWidget(QLabel("选择日期:"))
        layout.addWidget(de)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        if dialog.exec_() == QDialog.Accepted:
            sd = de.date().toString("yyyy-MM-dd")
            fl = [r for r in self._history if r.get("timestamp", "").startswith(sd)]
            if fl:
                msg = f"📅 {sd} 共 {len(fl)} 条记录\n"
                msg += f"总时长: {self._format_time(sum(r.get('duration', 0) for r in fl))}"
                QMessageBox.information(self, "筛选结果", msg)
            else:
                QMessageBox.information(self, "筛选结果", f"{sd} 无记录")

    def _on_batch_delete(self):
        if not self._history:
            QMessageBox.information(self, "批量删除", "暂无记录")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("批量删除")
        dialog.setFixedSize(400, 300)
        layout = QVBoxLayout(dialog)
        lw = QListWidget()
        lw.setSelectionMode(QAbstractItemView.MultiSelection)
        for i, r in enumerate(reversed(self._history)):
            item = QListWidgetItem(f"[{r.get('timestamp', '')}] {r.get('mode', '')} - {self._format_time(r.get('duration', 0))}")
            item.setData(Qt.UserRole, len(self._history) - 1 - i)
            lw.addItem(item)
        layout.addWidget(QLabel("选择要删除的记录:"))

        def delete_selected():
            sel = lw.selectedItems()
            if not sel:
                return
            idxs = sorted([item.data(Qt.UserRole) for item in sel], reverse=True)
            for idx in idxs:
                if 0 <= idx < len(self._history):
                    self._history.pop(idx)
            self._save_history()
            self._status_label.setText(f"🗑 已删除 {len(sel)} 条记录")
            dialog.accept()

        bl = QHBoxLayout()
        db = QPushButton("删除选中")
        db.clicked.connect(delete_selected)
        cb = QPushButton("取消")
        cb.clicked.connect(dialog.reject)
        bl.addWidget(db)
        bl.addWidget(cb)
        layout.addLayout(bl)
        dialog.exec_()

    def _on_show_stats(self):
        if not self._history:
            QMessageBox.information(self, "统计", "暂无记录")
            return
        total_records = len(self._history)
        total_duration = sum(r.get("duration", 0) for r in self._history)
        mode_stats = {}
        for r in self._history:
            m = r.get("mode", "unknown")
            mode_stats[m] = mode_stats.get(m, 0) + r.get("duration", 0)
        msg = f"📊 统计汇总\n\n"
        msg += f"总记录数: {total_records}\n"
        msg += f"总计时时长: {self._format_time(total_duration)}\n\n"
        msg += "各模式时长:\n"
        for mode, duration in sorted(mode_stats.items(), key=lambda x: -x[1]):
            msg += f"  {mode}: {self._format_time(duration)}\n"
        QMessageBox.information(self, "统计汇总", msg)

    def _on_batch_timer(self):
        QMessageBox.information(self, "批量倒计时", "批量倒计时功能开发中...")

    def _on_multi_task(self):
        QMessageBox.information(self, "多任务计时", "多任务同时计时功能开发中...")

    def _on_calibrate(self):
        QMessageBox.information(self, "时间校准", "时间校准功能开发中...")

    def _on_toggle_background(self, checked: bool):
        if checked:
            self.hide()
            self._status_label.setText("⏳ 后台运行中...")
        else:
            self.show()
            self._status_label.setText("▶ 已恢复前台显示")

    def _on_show_usage(self):
        QMessageBox.information(self, "使用说明",
            "CountTime 计时器 - 使用说明\n\n"
            "基本操作:\n"
            "  Space - 开始/暂停计时\n"
            "  R - 重置计时\n"
            "  L - 记录计次\n\n"
            "计时模式:\n"
            "  正计时 - 从0开始递增\n"
            "  倒计时 - 设置时间后递减\n"
            "  番茄钟 - 25分工作/5分休息\n"
            "  间隔循环 - 工作/休息交替\n"
            "  多段分段 - 按顺序执行多段计时\n"
            "  秒表模式 - 精确计时\n\n"
            "数据管理:\n"
            "  计时记录自动保存到 config/history.json\n"
            "  支持 CSV 导出\n"
            "  支持配置保存/加载\n\n"
            "快捷键: 设置菜单中查看全部快捷键")

    def _on_show_about(self):
        QMessageBox.about(self, "关于 CountTime",
            "CountTime 计时器 v2.0\n\n"
            "基于 PyQt5 的桌面计时器应用\n\n"
            "功能特性:\n"
            "  • 6 种计时模式\n"
            "  • 完整菜单栏操作\n"
            "  • 历史记录管理\n"
            "  • 配置保存/加载\n"
            "  • 键盘快捷键\n"
            "  • 窗口置顶/全屏\n\n"
            "技术栈: Python 3 + PyQt5")

    def _on_check_update(self):
        QMessageBox.information(self, "检查更新", "当前已是最新版本 v2.0")

    def _on_feedback(self):
        QMessageBox.information(self, "反馈建议",
            "如有问题或建议，请联系:\n\n"
            "📧 Email: support@counttime.app\n"
            "🐛 GitHub: github.com/counttime\n\n"
            "感谢您的使用！")

    def _add_history_record(self, mode: str, duration: int, note: str = ""):
        self._history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": mode, "duration": duration, "note": note
        })

    def _show_notification(self, title: str, message: str):
        self._status_label.setText(f"🔔 {title}: {message}")
        if self._sound_enabled:
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            except Exception:
                pass

    def _on_topmost_changed(self, state):
        if state == Qt.Checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self._always_on_top = True
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self._always_on_top = False
        self.show()
        self._save_settings()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Space:
            if self._running:
                self._on_pause()
            else:
                self._on_start()
        elif key == Qt.Key_R or key == Qt.Key_Delete:
            self._on_reset()
        elif key == Qt.Key_L:
            self._on_lap()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = CountTime()
    window.show()
    sys.exit(app.exec_())
