from enum import Enum
from typing import Optional, Union, Dict, List

from PySide6.QtCore import (
    QPoint,
    Qt,
    QSize,
    QByteArray,
    QPropertyAnimation,
    QEasingCurve,
    QParallelAnimationGroup,
    Signal,
    QRect,
    QTimer
)
from PySide6.QtGui import (
    QPixmap,
    QPainter,
    QCursor,
    QIcon,
    QFontMetrics,
    QPainterPath,
    QColor
)
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGraphicsOpacityEffect
)
from commons_lang import object_utils

from ...core.enum import Placement

DEFAULT_PLACEMENT: int = Placement.BottomRight
DEFAULT_WIDTH: int = 360
DEFAULT_ICON_SIZE: QSize = QSize(24, 24)
DEFAULT_TITLE_HEIGHT: int = 24
DEFAULT_DURATION: int = 5000


class NotificationType(Enum):
    """
    Notification Type
    """
    Info = "#1890FF"
    Success = "#07C160"
    Waring = "#FAAD14"
    Error = "#FF4D4F"


class NotificationIcons:
    """
    Notification Icons
    """

    _svg_icons = {
        NotificationType.Info.value: f"""<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{NotificationType.Info.value}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>""",
        NotificationType.Success.value: f"""<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{NotificationType.Success.value}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>""",
        NotificationType.Waring.value: f"""<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{NotificationType.Waring.value}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>""",
        NotificationType.Error.value: f"""<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{NotificationType.Error.value}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>"""
    }

    @staticmethod
    def get_icon_from_svg(svg_content: str) -> QIcon:
        pixmap = QPixmap(DEFAULT_ICON_SIZE)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer = QSvgRenderer(QByteArray(svg_content.encode()))
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    @staticmethod
    def get_icon(notice_type: Optional[NotificationType] = NotificationType.Info) -> QIcon:
        svg_content = object_utils.get(NotificationIcons._svg_icons, notice_type.value)
        return NotificationIcons.get_icon_from_svg(svg_content)


class Notification(QWidget):
    closed = Signal()

    _margin: int = 16
    _spacing: int = 10
    _animation_pos_offset: int = 50

    def __init__(
            self,
            notice_type: NotificationType,
            title: str,
            message: Optional[str] = None,
            width: Optional[int] = DEFAULT_WIDTH,
            placement: Optional[Placement] = DEFAULT_PLACEMENT,
            duration: Optional[int] = DEFAULT_DURATION,
            icon: Optional[Union[QIcon, str]] = None,
            parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self.notice_type = notice_type
        self.title = title
        self.message = message
        self.width = width
        self.placement = placement
        self.duration = duration
        self.icon = icon
        self.opacity = 0.0
        self.visible = False
        self.corner_radius = 8
        self.indicator_width = 4

        self._init_ui()
        self._target_position = self._calculate_taget_position()
        self._start_position = self._calculate_start_position()
        self._setup_animations()
        self._setup_timers()

    def start(self):
        self.show()
        self.show_animation.start()

    def close_with_animation(self):
        if self.hide_animation.state() == QParallelAnimationGroup.State.Running:
            return

        self.close_timer.stop()

        self.hide_opacity_animation.setStartValue(1.0)
        self.hide_opacity_animation.setEndValue(0.0)

        exit_pos = QPoint(self.pos())
        if self.placement in [Placement.Top, Placement.TopLeft, Placement.TopRight]:
            exit_pos.setY(exit_pos.y() - self._animation_pos_offset)
        elif self.placement in [Placement.Bottom, Placement.BottomLeft, Placement.BottomRight]:
            exit_pos.setY(exit_pos.y() + self._animation_pos_offset)

        if self.placement in [Placement.TopLeft, Placement.BottomLeft]:
            exit_pos.setX(exit_pos.x() - self._animation_pos_offset)
        elif self.placement in [Placement.TopRight, Placement.BottomRight]:
            exit_pos.setX(exit_pos.x() + self._animation_pos_offset)

        self.hide_pos_animation.setStartValue(self.pos())
        self.hide_pos_animation.setEndValue(exit_pos)

        self.hide_animation.start()

    @staticmethod
    def get_screen():
        return QApplication.screenAt(QCursor().pos()) or QApplication.primaryScreen()

    def _init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(self._margin, self._margin, self._margin, self._margin)
        main_layout.setSpacing(self._spacing)

        # Header layout with title and close button
        header_layout = QHBoxLayout()
        header_layout.setSpacing(self._spacing)

        self.icon_label = self._build_icon()
        header_layout.addWidget(self.icon_label, 0)

        self.title_label = self._build_title()
        header_layout.addWidget(self.title_label, 1)

        self.close_btn = self._build_close_btn()
        header_layout.addWidget(self.close_btn, 0)

        main_layout.addLayout(header_layout)
        if self.message:
            self.message_label = self._build_message_label()
            main_layout.addWidget(self.message_label)

        # Fixed width
        self.setFixedWidth(self.width)
        # Dynami height
        self.height = self._calculate_height()
        self.setFixedHeight(self.height)

        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create rounded rect path for the main background
        rect = QRect(0, 0, self.width - 1, self.height - 1)
        main_path = QPainterPath()
        main_path.addRoundedRect(rect, self.corner_radius, self.corner_radius)
        painter.fillPath(main_path, QColor("#FFFFFF"))

        # Draw shadow (subtle drop shadow)
        painter.setPen(Qt.NoPen)
        shadow_color = QColor(0, 0, 0, 15)
        shadow_offset = 2
        shadow_rect = rect.adjusted(0, 0, shadow_offset, shadow_offset)
        shadow_path = QPainterPath()
        shadow_path.addRoundedRect(shadow_rect, self.corner_radius, self.corner_radius)
        painter.fillPath(shadow_path, shadow_color)

        # Create a clipping path for the colored indicator
        # This ensures the indicator respects the rounded corners on the left side
        painter.setClipPath(main_path)

        # Draw colored indicator on left side (now properly clipped to respect rounded corners)
        indicator_rect = QRect(0, 0, self.indicator_width, self.height)
        painter.fillRect(indicator_rect, QColor(self.notice_type.value))

        painter.drawPath(main_path)

    def _calculate_height(self) -> int:
        # height = title-height + message-height + margin * 2
        height = self.title_label.height() + self._margin * 2

        #  If message label exists
        if self.message_label:
            fm = QFontMetrics(self.message_label.font())
            text_width = self.width - self._margin * 2  # Account for margins
            text_height = fm.boundingRect(
                QRect(0, 0, text_width, 1000),
                Qt.TextFlag.TextWordWrap,
                self.message
            ).height()
            height = height + text_height + self._spacing

        return height

    def _calculate_taget_position(self) -> QPoint:
        return self.get_target_position()

    def _calculate_start_position(self) -> QPoint:
        """
        Calculate starting positon. for entrance animations.
        :return:
        """
        start_position = QPoint(self._target_position)

        if self.placement in [Placement.Top, Placement.TopLeft, Placement.TopRight]:
            start_position.setY(start_position.y() - self._animation_pos_offset)
        elif self.placement in [Placement.Bottom, Placement.BottomLeft, Placement.BottomRight]:
            start_position.setY(start_position.y() + self._animation_pos_offset)

        if self.placement in [Placement.TopLeft, Placement.BottomLeft]:
            start_position.setX(start_position.x() - self._animation_pos_offset)
        elif self.placement in [Placement.TopRight, Placement.BottomRight]:
            start_position.setX(start_position.x() + self._animation_pos_offset)

        return start_position

    def _setup_animations(self):
        # Opacity effect for fade animation.
        self.opacity_effects = QGraphicsOpacityEffect(self)
        self.opacity_effects.setOpacity(0.0)
        self.setGraphicsEffect(self.opacity_effects)

        ###################### Showing animation ######################

        # Show Opacity animation (fade in/out)
        self.show_opacity_animation = QPropertyAnimation(self.opacity_effects, b"opacity")
        self.show_opacity_animation.setDuration(250)
        self.show_opacity_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        # Setup opacity animation for showing
        self.show_opacity_animation.setStartValue(0.0)
        self.show_opacity_animation.setEndValue(1.0)

        # Show Position animation (slide in/out)
        self.show_pos_animation = QPropertyAnimation(self, b"pos")
        self.show_pos_animation.setDuration(300)
        self.show_pos_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        # Setup position animation for showing
        self.show_pos_animation.setStartValue(self._start_position)
        self.show_pos_animation.setEndValue(self._target_position)

        # Combine animations for showing
        self.show_animation = QParallelAnimationGroup()
        self.show_animation.addAnimation(self.show_opacity_animation)
        self.show_animation.addAnimation(self.show_pos_animation)
        self.show_animation.finished.connect(self._on_show_finished)

        ###################### Hiding animation ######################

        # Hide Opacity animation (fade in/out)
        self.hide_opacity_animation = QPropertyAnimation(self.opacity_effects, b"opacity")
        self.hide_opacity_animation.setDuration(250)
        self.hide_opacity_animation.setEasingCurve(QEasingCurve.Type.InCubic)

        # Hide Position animation (slide in/out)
        self.hide_pos_animation = QPropertyAnimation(self, b"pos")
        self.hide_pos_animation.setDuration(300)
        self.hide_pos_animation.setEasingCurve(QEasingCurve.Type.InCubic)

        # Combine animations for hiding
        self.hide_animation = QParallelAnimationGroup()
        self.hide_animation.addAnimation(self.hide_opacity_animation)
        self.hide_animation.addAnimation(self.hide_pos_animation)
        self.hide_animation.finished.connect(self._on_hide_finished)

    def _setup_timers(self):
        self.close_timer = QTimer(self)
        self.close_timer.setSingleShot(True)
        self.close_timer.timeout.connect(self.close_with_animation)
        if self.duration > 0:
            self.close_timer.start(self.duration)

    def _on_show_finished(self):
        self.visible = True

    def _on_hide_finished(self):
        self.visible = False
        self.hide()
        self.closed.emit()
        NotificationManager.unregister(self)
        self.deleteLater()

    def _build_icon(self) -> QLabel:
        icon_label = QLabel()
        icon_label.setFixedSize(DEFAULT_ICON_SIZE)

        if isinstance(self.icon, QIcon):
            icon = self.icon
        elif isinstance(self.icon, str):
            icon = NotificationIcons.get_icon_from_svg(self.icon)
        else:
            icon = NotificationIcons.get_icon(self.notice_type)

        icon_pixmap = icon.pixmap(DEFAULT_ICON_SIZE)
        icon_label.setPixmap(icon_pixmap)
        return icon_label

    def _build_title(self) -> QLabel:
        title_label = QLabel(self.title)
        title_label.setStyleSheet(f"""
            font-weight: bold;
            color: #000000;
            font-size: 16px;
        """)
        title_label.setFixedHeight(DEFAULT_TITLE_HEIGHT)
        return title_label

    def _build_close_btn(self) -> QPushButton:
        close_btn = QPushButton()
        close_btn.setFixedSize(DEFAULT_ICON_SIZE)
        close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: #999999;
            }
            QPushButton:hover {
                color: #666666;
            }
            QPushButton:pressed {
                color: #333333;
            }
        """)

        close_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#999999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
           <line x1="18" y1="6" x2="6" y2="18"></line>
           <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>"""
        close_icon = NotificationIcons.get_icon_from_svg(close_icon_svg)
        close_btn.setIcon(close_icon)
        close_btn.setIconSize(DEFAULT_ICON_SIZE)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.close_with_animation)

        return close_btn

    def _build_message_label(self) -> QLabel:
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("""
            font-size: 14px;
            color: #666666;
        """)
        return message_label

    def get_target_position(self) -> QPoint:
        screen = self.get_screen()
        screen_geometry = screen.availableGeometry()
        width, height = self.width, self.height

        spacing = NotificationManager.get_spacing()
        if self.placement == Placement.Top:
            x = screen_geometry.center().x() - width // 2
            y = screen_geometry.top() + spacing
        elif self.placement == Placement.Bottom:
            x = screen_geometry.center().x() - width // 2
            y = screen_geometry.bottom() - height - spacing
        elif self.placement == Placement.TopLeft:
            x = screen_geometry.left() + spacing
            y = screen_geometry.top() + spacing
        elif self.placement == Placement.TopRight:
            x = screen_geometry.right() - width - spacing
            y = screen_geometry.top() + spacing
        elif self.placement == Placement.BottomLeft:
            x = screen_geometry.left() + spacing
            y = screen_geometry.bottom() - height - spacing
        elif self.placement == Placement.BottomRight:
            x = screen_geometry.right() - width - spacing
            y = screen_geometry.bottom() - height - spacing
        else:  # Placement.BottomRight
            x = screen_geometry.right() - width - spacing
            y = screen_geometry.bottom() - height - spacing

        x = max(screen_geometry.left(), min(x, screen_geometry.right() - width))
        y = max(screen_geometry.top(), min(y, screen_geometry.bottom() - height))

        return QPoint(x, y)

    def update_target_position(self, position: QPoint):
        exit_pos = self.pos()
        if exit_pos.x() != position.x() or exit_pos.y() != position.y():
            self.move(position)


class NotificationManager:
    """
    Notification Manager
    """
    _spacing: int = 16
    _instances: Dict[Placement, List[Notification]] = {}
    _notifications: List[Notification] = []

    @classmethod
    def config(cls, spacing: int = 16):
        cls._spacing = spacing

    @classmethod
    def get_spacing(cls) -> int:
        return cls._spacing

    @classmethod
    def create(
            cls,
            notice_type: NotificationType,
            title: str,
            message: Optional[str] = None,
            placement: Optional[Placement] = DEFAULT_PLACEMENT,
            duration: Optional[int] = DEFAULT_DURATION,
            icon: Optional[Union[QIcon, str]] = None
    ) -> Notification:
        notification = Notification(notice_type, title, message, placement=placement, duration=duration, icon=icon)
        cls.register(placement, notification)
        notification.start()
        return notification

    @classmethod
    def register(cls, placement: Placement, notification: Notification):
        if placement not in cls._instances:
            cls._instances[placement] = []
        cls._instances[placement].append(notification)
        cls._notifications.append(notification)
        # cls._arrange(placement)

    @classmethod
    def unregister(cls, notification: Notification):
        placement = notification.placement
        if placement in cls._instances and notification in cls._instances[placement]:
            cls._instances[placement].remove(notification)
            if notification in cls._notifications:
                cls._notifications.remove(notification)
            cls._arrange(placement)

    @classmethod
    def _arrange(cls, placement: Placement):
        if placement not in cls._instances:
            return

        notifications = cls._instances[placement]
        if not notifications:
            return

        if notifications:
            first = notifications[0]
            screen = first.get_screen()
            screen_rect = screen.availableGeometry()

            if placement in [Placement.Top, Placement.TopLeft, Placement.TopRight]:
                current_y = screen_rect.top() + cls._spacing
                for notification in notifications:
                    height = notification.height
                    target_pos = notification.get_target_position()
                    target_pos.setY(current_y)
                    notification.update_target_position(target_pos)
                    current_y += (height + cls._spacing)
            else:
                notifications.reverse()
                current_y = screen_rect.bottom() - cls._spacing
                for notification in notifications:
                    height = notification.height
                    target_pos = notification.get_target_position()
                    target_pos.setY(current_y - height)
                    notification.update_target_position(target_pos)
                    current_y -= (height + cls._spacing)
                notifications.reverse()

    @classmethod
    def success(
            cls,
            title: str,
            message: Optional[str] = None,
            placement: Optional[Placement] = DEFAULT_PLACEMENT,
            duration: Optional[int] = DEFAULT_DURATION,
            icon: Optional[Union[QIcon, str]] = None
    ) -> Notification:
        return NotificationManager.create(NotificationType.Success, title, message, placement, duration, icon)

    @classmethod
    def info(
            cls,
            title: str,
            message: Optional[str] = None,
            placement: Optional[Placement] = DEFAULT_PLACEMENT,
            duration: Optional[int] = DEFAULT_DURATION,
            icon: Optional[Union[QIcon, str]] = None
    ) -> Notification:
        return NotificationManager.create(NotificationType.Info, title, message, placement, duration, icon)

    @classmethod
    def warning(
            cls,
            title: str,
            message: Optional[str] = None,
            placement: Placement = DEFAULT_PLACEMENT,
            duration: int = DEFAULT_DURATION,
            icon: Optional[Union[QIcon, str]] = None
    ) -> Notification:
        return NotificationManager.create(NotificationType.Waring, title, message, placement, duration, icon)

    @classmethod
    def error(
            cls,
            title: str,
            message: Optional[str] = None,
            placement: Placement = DEFAULT_PLACEMENT,
            duration: int = DEFAULT_DURATION,
            icon: Optional[Union[QIcon, str]] = None
    ):
        return NotificationManager.create(NotificationType.Error, title, message, placement, duration, icon)

    @classmethod
    def close_all(cls):
        for notification in NotificationManager._notifications:
            notification.close_with_animation()
