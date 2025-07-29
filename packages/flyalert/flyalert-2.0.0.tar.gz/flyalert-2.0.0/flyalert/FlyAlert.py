from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog,
    QGraphicsDropShadowEffect, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

import sys


class FlyAlert(QDialog):
    ICONS = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'question': '❓'
    }

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.position = config.get("position", "center")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 300)
        self.auto_close_time = config.get("timer")

        self.opacity_anim = None
        self.close_anim = None
        self.init_ui()
        self.start_animation()
        self.start_auto_close_timer()

    def init_ui(self):
        self.container = QWidget(self)
        self.container.setGeometry(10, 10, 380, 280)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 4)
        self.container.setGraphicsEffect(shadow)
        self.container.setStyleSheet("background-color: white; border-radius: 15px;")

        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        if self.config.get("close_button", False):
            close_btn = QPushButton("×")
            close_btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #999;
                    font-size: 28px;
                    font-weight: bold;
                    border: none;
                    padding: 0;
                    min-width: 24px;
                    max-width: 24px;
                    min-height: 24px;
                    max-height: 24px;
                }
                QPushButton:hover {
                    color: #666;
                }
                QPushButton:pressed {
                    color: #333;
                }
            """)
            close_btn.clicked.connect(self.close_animation)

            close_layout = QHBoxLayout()
            close_layout.addStretch()
            close_layout.addWidget(close_btn)
            close_layout.setContentsMargins(0, 0, 0, 10)
            main_layout.addLayout(close_layout)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)

        icon_label = QLabel(self.ICONS.get(self.config.get("icon", "info"), 'ℹ️'))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Arial", 50))
        content_layout.addWidget(icon_label)

        title_label = QLabel(self.config.get("title", "Default Title"))
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label)

        message_label = QLabel(self.config.get("message", "Default Message"))
        message_label.setFont(QFont("Arial", 12))
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        content_layout.addWidget(message_label)

        main_layout.addLayout(content_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        if self.config.get("rtl", False):
            self.add_button(button_layout, "ConfirmButton", "#4CAF50", self.accept)
            self.add_button(button_layout, "InfoButton", "#2196F3", self.accept)
            self.add_button(button_layout, "CancelButton", "#F44336", self.reject)
        else:
            self.add_button(button_layout, "CancelButton", "#F44336", self.reject)
            self.add_button(button_layout, "InfoButton", "#2196F3", self.accept)
            self.add_button(button_layout, "ConfirmButton", "#4CAF50", self.accept)

        main_layout.addLayout(button_layout)

    def add_button(self, layout: QHBoxLayout, button_key: str, default_color: str, default_action):
        def get_hover_style(bg_color):
            color = QColor(bg_color)
            hover_color = color.lighter(80)
            return hover_color.name()

        if self.config.get(button_key, False):
            def btn_clicked():
                function = self.config.get(f"{button_key}Clicked", default_action)
                self.close_animation(function)

            btn = QPushButton(self.config.get(f"{button_key}Text", f"{button_key.replace('Button', '')}"))
            btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.config.get(f"{button_key}Color", default_color)};
                        color: white;
                        padding: 8px 16px;
                        border: none;
                        border-radius: 8px;
                        transition: all 0.3s ease;
                    }}
                    QPushButton:hover {{
                        background-color: {get_hover_style(self.config.get(f"{button_key}Color", default_color))};
                    }}
                """)
            btn.clicked.connect(btn_clicked)
            layout.addWidget(btn)

    def start_animation(self):
        self.setWindowOpacity(0.0)
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(300)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)
        self.opacity_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.opacity_anim.start()

    def close_animation(self, function=None):
        self.close_anim = QPropertyAnimation(self, b"windowOpacity")
        self.close_anim.setDuration(300)
        self.close_anim.setStartValue(1.0)
        self.close_anim.setEndValue(0.0)
        self.close_anim.setEasingCurve(QEasingCurve.InQuad)
        self.close_anim.start()
        QTimer.singleShot(300, function or self.close)

    def start_auto_close_timer(self):
        if self.auto_close_time:
            QTimer.singleShot(self.auto_close_time, self.close_animation)

    def show(self, parent_window=None):
        if parent_window:
            parent_pos = parent_window.mapToGlobal(parent_window.rect().topLeft())

            positions = {
                "top-right": (parent_pos.x() + parent_window.width() - self.width() - 20,
                              parent_pos.y() + 20),
                "top-left": (parent_pos.x() + 20, parent_pos.y() + 20),
                "bottom-right": (parent_pos.x() + parent_window.width() - self.width() - 20,
                                 parent_pos.y() + parent_window.height() - self.height() - 20),
                "bottom-left": (parent_pos.x() + 20,
                                parent_pos.y() + parent_window.height() - self.height() - 20),
                "center": (parent_pos.x() + (parent_window.width() - self.width()) // 2,
                           parent_pos.y() + (parent_window.height() - self.height()) // 2)
            }
        else:
            screen = QApplication.primaryScreen()
            available_geometry = screen.availableGeometry()
            positions = {
                "top-right": (available_geometry.width() - self.width() - 20, 20),
                "top-left": (20, 20),
                "bottom-right": (available_geometry.width() - self.width() - 20,
                                 available_geometry.height() - self.height() - 20),
                "bottom-left": (20, available_geometry.height() - self.height() - 20),
                "center": (available_geometry.center().x() - self.width() // 2,
                           available_geometry.center().y() - self.height() // 2)
            }

        pos_x, pos_y = positions.get(self.position, positions["center"])
        self.move(pos_x, pos_y)

        return super().exec_()


class MinimalFlyAlert(FlyAlert):
    def __init__(self, config: dict):
        super().__init__(config)
        self.auto_close_time = self.config.get("timer", 2000)
        self.position = config.get("position", "center")
        self.setFixedSize(410, 90)

        self.init_ui()
        self.start_auto_close_timer()

    def init_ui(self):
        self.container = QWidget(self)
        self.container.setGeometry(10, 10, 390, 70)
        self.container.setStyleSheet("background-color: white; border-radius: 10px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 4)
        self.container.setGraphicsEffect(shadow)
        layout = QGridLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)

        icon_label = QLabel(self.ICONS.get(self.config.get("icon", "info"), 'ℹ️'))
        icon_label.setFont(QFont("Arial", 32))

        message_label = QLabel(self.config.get("message", "Default Message"))
        message_label.setFont(QFont("Arial", 14))

        close_button = QPushButton("✖")
        close_button.setFont(QFont("Arial", 24))
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent; font-size: 24px; border: none;
                color: black;
            }
            QPushButton:hover {
                color: red;
                font-size: 26px;
            }
        """)
        close_button.clicked.connect(self.close_animation)

        layout.addWidget(icon_label, 0, 0)
        layout.addWidget(message_label, 0, 1)
        layout.addWidget(close_button, 0, 2)

    def start_auto_close_timer(self):
        if self.auto_close_time:
            QTimer.singleShot(self.auto_close_time, self.close_animation)
