import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QPushButton, QLabel, QLineEdit, QTextEdit, QProgressBar,
    QMessageBox, QFileDialog # For Help and Drag&Drop demo
)
from PyQt6.QtGui import QFont, QColor, QPainter, QKeySequence, QShortcut, QPen
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QSize, QDate,
    QRectF, pyqtSignal, QSettings, QVariant, QTimer
)

# Additional imports for custom painting and specific widgets
from PyQt6.QtWidgets import QRadioButton, QComboBox, QDateEdit, QCheckBox, QSlider, QStyleOptionButton, QStyle


# --- Theme Management ---
THEME = "light" # "light" or "dark"

# Function to get color based on current theme and role
def get_color(role):
    if THEME == "dark":
        return DARK_COLORS.get(role, LIGHT_COLORS.get(role, QColor("magenta"))) # Fallback to magenta if color not found
    return LIGHT_COLORS.get(role, QColor("magenta"))

LIGHT_COLORS = {
    "background": QColor("#f8f8f8"),
    "background_secondary": QColor("#ffffff"),
    "text_primary": QColor("#1d1d1f"),
    "text_secondary": QColor("#6e6e73"),
    "accent": QColor("#007AFF"),
    "accent_hover": QColor("#005ecb"),
    "accent_pressed": QColor("#004a9e"),
    "separator": QColor("#d2d2d7"),
    "disabled_background": QColor("#e5e5e5"),
    "disabled_text": QColor("#a0a0a0"),
    "input_border": QColor("#c6c6c8"),
    "input_border_focus": QColor("#007AFF"), # Same as accent
    "input_border_error": QColor("#ff3b30"),
}

DARK_COLORS = {
    "background": QColor("#1c1c1e"),
    "background_secondary": QColor("#2c2c2e"),
    "text_primary": QColor("#ffffff"),
    "text_secondary": QColor("#8e8e93"),
    "accent": QColor("#0A84FF"),
    "accent_hover": QColor("#0060df"),
    "accent_pressed": QColor("#004fad"),
    "separator": QColor("#38383a"),
    "disabled_background": QColor("#3a3a3c"),
    "disabled_text": QColor("#636366"),
    "input_border": QColor("#48484a"),
    "input_border_focus": QColor("#0A84FF"), # Same as accent
    "input_border_error": QColor("#ff453a"),
}

BORDER_RADIUS = "8px"

class AnimatedButton(QPushButton):
    """
    背景色のアニメーションを持つ基本的なボタンクラス。
    AppleStyleButtonのベースとなります。
    """
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        # Initialize animation object first, but don't fully configure yet
        self._animation = QPropertyAnimation() # No target or property name yet
        self._animation.setDuration(150) # アニメーション時間 (ミリ秒)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Initialize all color attributes, including _current_bg_color
        self._update_colors() # Load colors based on current theme

        # This is the crucial attribute for the backgroundColor property
        self._current_bg_color = self._default_bg_color

        # Now that all attributes are set, fully configure the animation.
        self._animation.setTargetObject(self)
        self._animation.setPropertyName(b"backgroundColor")

        self._apply_style()

    def _update_colors(self):
        self._default_bg_color = get_color("accent")
        self._hover_bg_color = get_color("accent_hover")
        self._pressed_bg_color = get_color("accent_pressed")
        self._disabled_bg_color = get_color("disabled_background")
        self._disabled_text_color = get_color("disabled_text")
        self._text_color = QColor("white") # Default for accent buttons

    def _apply_style(self):
        bg_color = self._current_bg_color
        text_color_name = self._text_color.name() # Use the instance variable
        if not self.isEnabled():
            bg_color = self._disabled_bg_color
            text_color_name = self._disabled_text_color.name()

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color.name()};
                color: {text_color_name};
                border: none; /* 通常は枠線なし */
                padding: 10px 20px;
                border-radius: {BORDER_RADIUS};
                font-size: 14px; /* 基本フォントサイズ */
                font-weight: 500; /* Medium weight for SF Pro Text like feel */
            }}
        """)

    @pyqtProperty(QColor)
    def backgroundColor(self):
        return self._current_bg_color

    @backgroundColor.setter
    def backgroundColor(self, color):
        if self._current_bg_color != color:
            self._current_bg_color = color
            self._apply_style() # Re-apply style with the new color

    def enterEvent(self, event):
        if self.isEnabled():
            self._animation.stop() # 既存のアニメーションを停止
            self._animation.setStartValue(self.backgroundColor)
            self._animation.setEndValue(self._hover_bg_color)
            self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.isEnabled():
            self._animation.stop()
            self._animation.setStartValue(self.backgroundColor)
            self._animation.setEndValue(self._default_bg_color)
            self._animation.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.isEnabled() and event.button() == Qt.MouseButton.LeftButton:
            self._animation.stop()
            self.backgroundColor = self._pressed_bg_color
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.isEnabled() and event.button() == Qt.MouseButton.LeftButton:
            if self.underMouse():
                self._animation.stop()
                self._animation.setStartValue(self.backgroundColor)
                self._animation.setEndValue(self._hover_bg_color)
                self._animation.start()
            else:
                # マウスがボタンの外でリリースされた場合
                self.backgroundColor = self._default_bg_color
        super().mouseReleaseEvent(event)

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        if enabled:
            self.backgroundColor = self._default_bg_color
        else:
            self.backgroundColor = self._disabled_bg_color
        self._apply_style()

    def update_theme(self):
        old_default_bg = self._default_bg_color # Store old default to check if it was a custom button
        self._update_colors()
        # If the button was using the standard accent color, update it.
        # If it was a custom styled button (like secondary), its _default_bg_color will be different
        # and should be re-evaluated by the caller (e.g., style_secondary_button).
        if self.backgroundColor == old_default_bg or not self.isEnabled():
            self.backgroundColor = self._default_bg_color if self.isEnabled() else self._disabled_bg_color
        else:
            # If it was a custom button, its colors might need specific re-application
            # This part is tricky, often handled by the styling function for that button type
            pass
        self._apply_style()


class AppleStyleButton(AnimatedButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        font = QFont()
        if sys.platform == "darwin": # macOS
            font.setFamily("SF Pro Text")
            font.setPointSize(15)
            font.setWeight(QFont.Weight.Medium)
        elif sys.platform == "win32": # Windows
            font.setFamily("Segoe UI")
            font.setPointSize(10)
            font.setWeight(QFont.Weight.DemiBold)
        else: # Linuxなど
            font.setFamily("Noto Sans")
            font.setPointSize(11)
            font.setWeight(QFont.Weight.Medium)
        self.setFont(font)


class AppleStyleLabel(QLabel):
    def __init__(self, text, parent=None, font_size=14, is_secondary=False):
        super().__init__(text, parent)
        font = QFont()
        if sys.platform == "darwin":
            font.setFamily("SF Pro Text")
            font.setPointSize(font_size)
        elif sys.platform == "win32":
            font.setFamily("Segoe UI")
            font.setPointSize(int(font_size * 0.8) if font_size * 0.8 >= 9 else 9)
        else:
            font.setFamily("Noto Sans")
            font.setPointSize(int(font_size * 0.9) if font_size * 0.9 >= 10 else 10)
        self.setFont(font)

        self.is_secondary = is_secondary
        self._apply_style()

    def _apply_style(self):
        text_color = get_color("text_secondary") if self.is_secondary else get_color("text_primary")
        self.setStyleSheet(f"""
            QLabel {{
                color: {text_color.name()};
                background-color: transparent;
                padding: 2px;
            }}
        """)
    def update_theme(self):
        self._apply_style()

class AppleStyleLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        font = QFont()
        if sys.platform == "darwin":
            font.setFamily("SF Pro Text")
            font.setPointSize(14)
        elif sys.platform == "win32":
            font.setFamily("Segoe UI")
            font.setPointSize(10)
        else:
            font.setFamily("Noto Sans")
            font.setPointSize(11)
        self.setFont(font)
        self._validation_state = "none" # "none", "error", "warning", "success"
        self._apply_style()

        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)


    def setValidationState(self, state):
        self._validation_state = state
        self._apply_style()

    def _apply_style(self):
        border_color = get_color("input_border")
        if self._validation_state == "error":
            border_color = get_color("input_border_error")

        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {get_color("background_secondary").name()};
                color: {get_color("text_primary").name()};
                border: 1px solid {border_color.name()};
                border-radius: {BORDER_RADIUS};
                padding: 8px 10px;
                min-height: 22px;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {get_color("input_border_focus").name()};
            }}
            QLineEdit:disabled {{
                background-color: {get_color("disabled_background").name()};
                color: {get_color("disabled_text").name()};
                border-color: {get_color("separator").name()};
            }}
        """)

    def update_theme(self):
        self._apply_style()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if url.isLocalFile():
                self.setText(url.toLocalFile())
                break

class AppleStyleTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        font = QFont()
        if sys.platform == "darwin":
            font.setFamily("SF Pro Text")
            font.setPointSize(14)
        elif sys.platform == "win32":
            font.setFamily("Segoe UI")
            font.setPointSize(10)
        else:
            font.setFamily("Noto Sans")
            font.setPointSize(11)
        self.setFont(font)
        self._apply_style()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)


    def _apply_style(self):
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {get_color("background_secondary").name()};
                color: {get_color("text_primary").name()};
                border: 1px solid {get_color("input_border").name()};
                border-radius: {BORDER_RADIUS};
                padding: 8px 10px;
            }}
            QTextEdit:focus {{
                border: 1.5px solid {get_color("input_border_focus").name()};
            }}
            QTextEdit:disabled {{
                background-color: {get_color("disabled_background").name()};
                color: {get_color("disabled_text").name()};
                border-color: {get_color("separator").name()};
            }}
        """)

    def update_theme(self):
        self._apply_style()

class AppleStyleCheckBox(QCheckBox):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        font = QFont()
        if sys.platform == "darwin": font.setFamily("SF Pro Text"); font.setPointSize(14)
        elif sys.platform == "win32": font.setFamily("Segoe UI"); font.setPointSize(10)
        else: font.setFamily("Noto Sans"); font.setPointSize(11)
        self.setFont(font)
        self._apply_style()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QCheckBox {{
                spacing: 8px;
                color: {get_color("text_primary").name()};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {get_color("input_border").name()};
                border-radius: 4px;
                background-color: {get_color("background_secondary").name()};
            }}
            QCheckBox::indicator:checked {{
                background-color: {get_color("accent").name()};
                border: 1px solid {get_color("accent").name()};
            }}
            QCheckBox::indicator:disabled {{
                background-color: {get_color("disabled_background").name()};
                border: 1px solid {get_color("separator").name()};
            }}
        """)
    def update_theme(self):
        self._apply_style()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.isChecked():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Get the rectangle for the indicator
            opt = QStyleOptionButton()
            self.initStyleOption(opt) # Initialize style option from the widget
            indicator_rect = self.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, opt, self)

            # Define checkmark properties
            pen = QPen(QColor("white")) # Checkmark color
            pen.setWidth(2) # Checkmark line thickness
            pen.setCapStyle(Qt.PenCapStyle.RoundCap) # Rounded ends for the checkmark
            painter.setPen(pen)

            # Calculate points for a simple "L" shaped checkmark
            # These are relative to the indicator_rect and might need adjustment for perfect centering/sizing
            padding = indicator_rect.width() * 0.25 # Padding from edges
            x1 = indicator_rect.left() + padding
            y1 = indicator_rect.top() + indicator_rect.height() * 0.5
            x2 = indicator_rect.left() + indicator_rect.width() * 0.45
            y2 = indicator_rect.top() + indicator_rect.height() - padding
            x3 = indicator_rect.right() - padding
            y3 = indicator_rect.top() + indicator_rect.height() * 0.35

            painter.drawLine(int(x1), int(y1), int(x2), int(y2)) # Draw first part of checkmark
            painter.drawLine(int(x2), int(y2), int(x3), int(y3)) # Draw second part of checkmark
            painter.end()

class AppleStyleSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(51, 31)
        self._checked = False
        self._circle_position = 3

        self._animation = QPropertyAnimation(self, b"circlePosition")
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_theme()

    @pyqtProperty(int)
    def circlePosition(self):
        return self._circle_position

    @circlePosition.setter
    def circlePosition(self, pos):
        self._circle_position = pos
        self.update()

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        if self._checked == checked:
            return
        self._checked = checked
        self._start_animation()
        self.toggled.emit(self._checked)
        self.update()

    def _start_animation(self):
        self._animation.stop()
        current_pos = self.circlePosition
        target_pos = self.width() - self.height() + 3 if self._checked else 3

        self._animation.setStartValue(current_pos)
        self._animation.setEndValue(target_pos)
        self._animation.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setChecked(not self.isChecked())
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        track_rect = self.rect()
        track_color = get_color("accent") if self._checked else get_color("separator")
        painter.setBrush(track_color)
        painter.setPen(Qt.PenStyle.NoPen)
        track_radius = track_rect.height() / 2
        painter.drawRoundedRect(track_rect, track_radius, track_radius)

        handle_radius = (self.height() / 2) - 2
        handle_diameter = handle_radius * 2
        y_pos = (self.height() - handle_diameter) / 2
        handle_rect = QRectF(self._circle_position, y_pos, handle_diameter, handle_diameter)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(handle_rect)
        painter.end()

    def update_theme(self):
        self.update()

    def sizeHint(self):
        return QSize(51, 31)


class AppleStyleSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self._apply_style()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event):
        # print(f"AppleStyleSlider wheelEvent: hasFocus() = {self.hasFocus()}")
        if self.hasFocus():
            # print("AppleStyleSlider: Processing wheel event")
            super().wheelEvent(event)
        else:
            # print("AppleStyleSlider: Ignoring wheel event")
            event.ignore()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: 1px solid {get_color("separator").name()};
                height: 4px;
                background: {get_color("separator").name()};
                margin: 2px 0;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {get_color("background_secondary").name()};
                border: 1px solid {get_color("separator").name()};
                width: 28px;
                height: 28px;
                margin: -12px 0;
                border-radius: 14px;
            }}
            QSlider::sub-page:horizontal {{
                background: {get_color("accent").name()};
                border: 1px solid {get_color("accent").name()};
                height: 4px;
                border-radius: 2px;
            }}
            QSlider::groove:vertical {{
                border: 1px solid {get_color("separator").name()};
                width: 4px;
                background: {get_color("separator").name()};
                margin: 0 2px;
                border-radius: 2px;
            }}
            QSlider::handle:vertical {{
                background: {get_color("background_secondary").name()};
                border: 1px solid {get_color("separator").name()};
                width: 28px;
                height: 28px;
                margin: 0 -12px;
                border-radius: 14px;
            }}
            QSlider::sub-page:vertical {{
                background: {get_color("accent").name()};
                border: 1px solid {get_color("accent").name()};
                width: 4px;
                border-radius: 2px;
            }}
        """)
    def update_theme(self):
        self._apply_style()

class AppleStyleRadioButton(QRadioButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        font = QFont()
        if sys.platform == "darwin": font.setFamily("SF Pro Text"); font.setPointSize(14)
        elif sys.platform == "win32": font.setFamily("Segoe UI"); font.setPointSize(10)
        else: font.setFamily("Noto Sans"); font.setPointSize(11)
        self.setFont(font)
        self._apply_style()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)


    def wheelEvent(self, event):
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QRadioButton {{
                spacing: 8px;
                color: {get_color("text_primary").name()};
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {get_color("input_border").name()};
                border-radius: 9px;
                background-color: {get_color("background_secondary").name()};
            }}
            QRadioButton::indicator:checked {{
                background-color: {get_color("background_secondary").name()};
                border: 1px solid {get_color("accent").name()};
            }}
            QRadioButton::indicator:disabled {{
                background-color: {get_color("disabled_background").name()};
                border: 1px solid {get_color("separator").name()};
            }}
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.isChecked():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            opt = QStyleOptionButton()
            self.initStyleOption(opt)
            indicator_rect = self.style().subElementRect(QStyle.SubElement.SE_RadioButtonIndicator, opt, self)
            dot_diameter = indicator_rect.width() / 2.5
            dot_rect = QRectF(
                (indicator_rect.width() - dot_diameter) / 2 + indicator_rect.x(),
                (indicator_rect.height() - dot_diameter) / 2 + indicator_rect.y(),
                dot_diameter, dot_diameter
            )
            painter.setBrush(get_color("accent"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(dot_rect)
            painter.end()

    def update_theme(self):
        self._apply_style()
        self.update() # Ensure repaint for the custom dot

class AppleStyleComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        font = QFont()
        if sys.platform == "darwin": font.setFamily("SF Pro Text"); font.setPointSize(14)
        elif sys.platform == "win32": font.setFamily("Segoe UI"); font.setPointSize(10)
        else: font.setFamily("Noto Sans"); font.setPointSize(11)
        self.setFont(font)
        self._apply_style()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)


    def wheelEvent(self, event):
        # print(f"AppleStyleComboBox wheelEvent: hasFocus() = {self.hasFocus()}")
        if self.hasFocus():
            # print("AppleStyleComboBox: Processing wheel event")
            super().wheelEvent(event)
        else:
            # print("AppleStyleComboBox: Ignoring wheel event")
            event.ignore()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QComboBox {{
                color: {get_color("text_primary").name()};
                background-color: {get_color("background_secondary").name()};
                border: 1px solid {get_color("input_border").name()};
                border-radius: {BORDER_RADIUS};
                padding: 5px 10px;
                min-height: 22px;
            }}
            QComboBox:focus {{
                border: 1.5px solid {get_color("input_border_focus").name()};
            }}
            QComboBox:disabled {{
                background-color: {get_color("disabled_background").name()};
                color: {get_color("disabled_text").name()};
            }}
            QComboBox QAbstractItemView {{
                background-color: {get_color("background_secondary").name()};
                color: {get_color("text_primary").name()};
                border: 1px solid {get_color("input_border").name()};
                selection-background-color: {get_color("accent").name()};
                selection-color: white;
                outline: 0px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: {get_color("separator").name()};
                border-left-style: solid;
                border-top-right-radius: {BORDER_RADIUS};
                border-bottom-right-radius: {BORDER_RADIUS};
            }}
            QComboBox::down-arrow {{
                width: 12px;
                height: 12px;
            }}
        """)
    def update_theme(self):
        self._apply_style()

class AppleStyleDateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        font = QFont()
        if sys.platform == "darwin": font.setFamily("SF Pro Text"); font.setPointSize(14)
        elif sys.platform == "win32": font.setFamily("Segoe UI"); font.setPointSize(10)
        else: font.setFamily("Noto Sans"); font.setPointSize(11)
        self.setFont(font)
        self.setCalendarPopup(True)
        self._apply_style()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event):
        # print(f"AppleStyleDateEdit wheelEvent: hasFocus() = {self.hasFocus()}")
        if self.hasFocus():
            # print("AppleStyleDateEdit: Processing wheel event")
            super().wheelEvent(event)
        else:
            # print("AppleStyleDateEdit: Ignoring wheel event")
            event.ignore()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QDateEdit {{
                color: {get_color("text_primary").name()};
                background-color: {get_color("background_secondary").name()};
                border: 1px solid {get_color("input_border").name()};
                border-radius: {BORDER_RADIUS};
                padding: 5px 10px;
                min-height: 22px;
            }}
            QDateEdit:focus {{
                border: 1.5px solid {get_color("input_border_focus").name()};
            }}
            QDateEdit:disabled {{
                background-color: {get_color("disabled_background").name()};
                color: {get_color("disabled_text").name()};
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: {get_color("separator").name()};
                border-left-style: solid;
                border-top-right-radius: {BORDER_RADIUS};
                border-bottom-right-radius: {BORDER_RADIUS};
            }}
            QDateEdit::down-arrow {{
            }}
            QCalendarWidget QWidget {{
                background-color: {get_color("background_secondary").name()};
                color: {get_color("text_primary").name()};
                alternate-background-color: {get_color("background").name()};
            }}
            QCalendarWidget QAbstractItemView {{
                selection-background-color: {get_color("accent").name()};
                selection-color: white;
            }}
            QCalendarWidget QToolButton {{
                color: {get_color("text_primary").name()};
                background-color: transparent;
                border: none;
                padding: 5px;
                margin: 2px;
                border-radius: {BORDER_RADIUS};
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: {get_color("separator").name()};
            }}
            QCalendarWidget QToolButton:pressed {{
                background-color: {get_color("accent_pressed").name()};
            }}
            QCalendarWidget QMenu {{
                background-color: {get_color("background_secondary").name()};
                color: {get_color("text_primary").name()};
                selection-background-color: {get_color("accent").name()};
            }}
        """)
    def update_theme(self):
        self._apply_style()

class AppleStyleProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setTextVisible(False)
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 5px;
                background-color: {get_color("separator").name()};
                height: 10px;
            }}
            QProgressBar::chunk {{
                background-color: {get_color("accent").name()};
                border-radius: 5px;
            }}
        """)

    def update_theme(self):
        self._apply_style()

class AppleStyleMessageLabel(AppleStyleLabel):
    def __init__(self, parent=None):
        super().__init__("", parent, font_size=12, is_secondary=True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(20)
        self.hide()


class AppleStyleWindow(QMainWindow):
    def __init__(self, title="Apple Style App"):
        super().__init__()
        self.setWindowTitle(title)
        desktop = QApplication.primaryScreen().geometry()
        width = 700 # Increased width to accommodate more elements
        height = 750 # Increased height
        
        self.settings = QSettings("MyCompany", "AppleStyleApp")
        self._load_settings() # Load theme before setting up UI that depends on it
        self.setGeometry( (desktop.width() - width) // 2, (desktop.height() - height) // 2, width, height)
        # self.current_theme is set by _load_settings or defaults to THEME

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.scroll_content_widget = QWidget()
        self.layout = QVBoxLayout(self.scroll_content_widget)
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(18)
        
        self.message_label = AppleStyleMessageLabel(self.scroll_content_widget) # Create before _apply_theme_styles

        self.scroll_area.setWidget(self.scroll_content_widget)
        self.setCentralWidget(self.scroll_area)
        self._apply_theme_styles() # Apply theme after all base UI structure is set

    def _apply_theme_styles(self):
        if sys.platform != "darwin":
            self.setStyleSheet(f"QMainWindow {{ background-color: {get_color('background').name()}; }}")

        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {get_color('background').name()};
                border: none;
            }}
            QScrollBar:vertical {{
                border: none;
                background: {get_color('separator').name()};
                width: 10px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {get_color('text_secondary').name()};
                min-height: 20px;
                border-radius: 5px;
            }}
        """)
        self.scroll_content_widget.setStyleSheet(f"QWidget {{ background-color: {get_color('background').name()}; }}")

        # Update theme for all children that support it
        # Iterate through direct children of the layout first
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item is None: continue
            widget = item.widget()
            if widget and hasattr(widget, 'update_theme'):
                widget.update_theme()
            elif isinstance(widget, QWidget): # For generic QWidgets used as containers
                # This part might need refinement if complex nested layouts are used
                # without custom AppleStyle widgets.
                if widget.layout() is not None:
                     widget.setStyleSheet(f"QWidget {{ background-color: transparent; }}") # Make container transparent
                     # Recursively update children of this container widget if needed
                     for child_widget in widget.findChildren(QWidget):
                         if hasattr(child_widget, 'update_theme'):
                             child_widget.update_theme()
        
        if hasattr(self.message_label, 'update_theme'):
             self.message_label.update_theme()


    def _load_settings(self):
        global THEME
        # Ensure QSettings uses a valid format on all platforms
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        self.settings = QSettings("MyCompany", "AppleStyleApp")
        
        theme_setting = self.settings.value("theme", "light", type=str)
        THEME = theme_setting
        self.current_theme = THEME

    def _save_settings(self):
        self.settings.setValue("theme", self.current_theme)
        self.settings.sync() # Ensure settings are written to disk

    def set_theme(self, theme_name):
        global THEME
        THEME = theme_name
        self.current_theme = theme_name # Update instance variable
        self._save_settings()
        self._apply_theme_styles()

    def addContentWidget(self, widget):
        # If adding message label, ensure it's before stretch
        if self.layout.itemAt(self.layout.count() -1) and \
           self.layout.itemAt(self.layout.count() -1).spacerItem():
            # Insert before the stretch
            self.layout.insertWidget(self.layout.count() -1, widget)
        else:
            self.layout.addWidget(widget)

    def addStretch(self, stretch=1):
        # Remove existing stretch if any, to ensure only one at the end
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item and item.spacerItem():
                self.layout.removeItem(item)
                break
        self.layout.addStretch(stretch)

    def show_message(self, message, duration_ms=3000):
        self.message_label.setText(message)
        self.message_label.show()
        QTimer.singleShot(duration_ms, self.message_label.hide)

    def closeEvent(self, event):
        self._save_settings() # Save settings on close
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Ensure settings are initialized for the application
    QApplication.setOrganizationName("MyCompany")
    QApplication.setApplicationName("AppleStyleApp")


    main_window = AppleStyleWindow("My Apple-like Application")

    title_label = AppleStyleLabel("User Profile", font_size=22)
    title_label.setStyleSheet(title_label.styleSheet() + "font-weight: bold; padding-bottom: 10px;")
    main_window.addContentWidget(title_label)

    name_label = AppleStyleLabel("Full Name:")
    name_input = AppleStyleLineEdit()
    name_input.setPlaceholderText("Enter your full name")
    name_input.setToolTip("Enter your full name here. You can drag and drop a file path here.")
    main_window.addContentWidget(name_label)
    main_window.addContentWidget(name_input)

    email_label = AppleStyleLabel("Email Address:", is_secondary=True)
    email_input = AppleStyleLineEdit()
    email_input.setPlaceholderText("you@example.com")
    email_input.setToolTip("Enter your email address.")
    main_window.addContentWidget(email_label)
    main_window.addContentWidget(email_input)

    address_label = AppleStyleLabel("Address (Disabled):", is_secondary=True)
    address_input = AppleStyleLineEdit()
    address_input.setPlaceholderText("Your address here")
    address_input.setEnabled(False)
    main_window.addContentWidget(address_label)
    main_window.addContentWidget(address_input)

    bio_label = AppleStyleLabel("Biography:")
    bio_text_edit = AppleStyleTextEdit()
    bio_text_edit.setPlaceholderText("Tell us something about yourself...")
    bio_text_edit.setFixedHeight(100)
    bio_text_edit.setToolTip("Write a short biography.")
    main_window.addContentWidget(bio_label)
    main_window.addContentWidget(bio_text_edit)

    gender_label = AppleStyleLabel("Gender:")
    main_window.addContentWidget(gender_label)
    gender_layout_widget = QWidget() # Container for radio buttons
    gender_layout = QHBoxLayout(gender_layout_widget)
    gender_layout.setContentsMargins(0,0,0,0) # No extra margins for this internal layout
    male_radio = AppleStyleRadioButton("Male")
    female_radio = AppleStyleRadioButton("Female")
    other_radio = AppleStyleRadioButton("Other")
    gender_layout.addWidget(male_radio)
    gender_layout.addWidget(female_radio)
    gender_layout.addWidget(other_radio)
    male_radio.setChecked(True)
    main_window.addContentWidget(gender_layout_widget)


    occupation_label = AppleStyleLabel("Occupation:")
    main_window.addContentWidget(occupation_label)
    occupation_combo = AppleStyleComboBox()
    occupation_combo.addItems(["Student", "Engineer", "Designer", "Manager", "Other"])
    occupation_combo.setCurrentText("Other")
    occupation_combo.setToolTip("Select your occupation.")
    main_window.addContentWidget(occupation_combo)

    birthday_label = AppleStyleLabel("Birthday:")
    main_window.addContentWidget(birthday_label)
    birthday_edit = AppleStyleDateEdit()
    birthday_edit.setDisplayFormat("yyyy-MM-dd")
    birthday_edit.setDate(QDate.currentDate())
    birthday_edit.setToolTip("Select your birth date.")
    main_window.addContentWidget(birthday_edit)

    newsletter_label = AppleStyleLabel("Preferences:")
    main_window.addContentWidget(newsletter_label)
    newsletter_checkbox = AppleStyleCheckBox("Subscribe to newsletter")
    newsletter_checkbox.setChecked(True)
    newsletter_checkbox.setToolTip("Toggle newsletter subscription.")
    main_window.addContentWidget(newsletter_checkbox)

    enable_features_label = AppleStyleLabel("Enable Experimental Features:")
    main_window.addContentWidget(enable_features_label)
    feature_switch = AppleStyleSwitch()
    feature_switch.setToolTip("Toggle experimental features on or off.")
    main_window.addContentWidget(feature_switch)

    volume_label = AppleStyleLabel("Volume:")
    main_window.addContentWidget(volume_label)
    volume_slider = AppleStyleSlider(Qt.Orientation.Horizontal)
    volume_slider.setRange(0, 100)
    volume_slider.setValue(75)
    volume_slider.setToolTip("Adjust the volume level.")
    main_window.addContentWidget(volume_slider)

    progress_label = AppleStyleLabel("Task Progress:")
    main_window.addContentWidget(progress_label)
    progress_bar = AppleStyleProgressBar()
    progress_bar.setValue(50)
    progress_bar.setToolTip("Shows the progress of a task.")
    main_window.addContentWidget(progress_bar)

    # Add message label to the layout, typically before the final stretch
    main_window.layout.addWidget(main_window.message_label)


    # --- Buttons ---
    buttons_layout_widget = QWidget() # Container for main action buttons
    buttons_layout = QHBoxLayout(buttons_layout_widget)
    buttons_layout.setContentsMargins(0,0,0,0)


    theme_button = AppleStyleButton("Toggle Theme")
    def style_secondary_button(button): # Helper to style secondary buttons consistently
        button._update_colors()
        button._default_bg_color = get_color("separator")
        button._hover_bg_color = get_color("disabled_background")
        button._pressed_bg_color = get_color("input_border")
        button._text_color = get_color("text_primary") # Text color for secondary buttons
        button._current_bg_color = button._default_bg_color
        button._apply_style()


    def toggle_theme_and_buttons():
        current_theme_name = main_window.current_theme
        if current_theme_name == "light":
            main_window.set_theme("dark")
        else:
            main_window.set_theme("light")
        # Re-style secondary buttons after theme change
        style_secondary_button(theme_button)
        style_secondary_button(button_cancel)
        style_secondary_button(help_button)


    theme_button.clicked.connect(toggle_theme_and_buttons)
    style_secondary_button(theme_button) # Initial style
    theme_button.setToolTip("Switch between light and dark themes.")
    buttons_layout.addWidget(theme_button)


    help_button = AppleStyleButton("Help")
    def show_help():
        QMessageBox.information(main_window, "Help", "This is a sample application demonstrating Apple-like UI elements with various features.")
    help_button.clicked.connect(show_help)
    style_secondary_button(help_button)
    help_button.setToolTip("Show help information.")
    buttons_layout.addWidget(help_button)

    buttons_layout.addStretch(1) # Add stretch to push next buttons to the right

    button_submit = AppleStyleButton("Save Changes")
    save_shortcut = QShortcut(QKeySequence.StandardKey.Save, main_window)
    def on_submit():
        print(f"Name: {name_input.text()}")
        print(f"Email: {email_input.text()}")
        print(f"Bio: {bio_text_edit.toPlainText()}")
        main_window.show_message("Settings saved successfully!")
    button_submit.clicked.connect(on_submit)
    save_shortcut.activated.connect(on_submit)
    button_submit.setToolTip("Save your changes (Ctrl+S / Cmd+S)")
    buttons_layout.addWidget(button_submit)

    button_cancel = AppleStyleButton("Cancel")
    style_secondary_button(button_cancel)
    button_cancel.setToolTip("Discard changes and exit (not implemented).")
    buttons_layout.addWidget(button_cancel)
    
    main_window.addContentWidget(buttons_layout_widget)


    disabled_action_button = AppleStyleButton("Another Action (Disabled)")
    disabled_action_button.setEnabled(False)
    disabled_action_button.setToolTip("This action is currently disabled.")
    main_window.addContentWidget(disabled_action_button)

    main_window.addStretch()

    # Apply initial theme to secondary buttons after they are created
    # This is important if the loaded theme is dark
    if main_window.current_theme == "dark":
        style_secondary_button(theme_button)
        style_secondary_button(button_cancel)
        style_secondary_button(help_button)


    main_window.show()
    sys.exit(app.exec())
