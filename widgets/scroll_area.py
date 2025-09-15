from PyQt5.QtWidgets import (
    QApplication, QScrollArea, QWidget, QVBoxLayout,
    QLabel, QHBoxLayout, QGridLayout, QScroller,QSizePolicy
)
from PyQt5.QtCore import Qt, QObject, QEvent, QPoint


class ScrollableWidget(QWidget, QObject):
    """
    A QWidget that provides a scrollable area with hidden scrollbars.
    Supports vertical, horizontal, or both-direction scrolling.
    
    Public API:
        - contentLayout() -> QLayout
            Returns the current layout inside the scrollable area.
            You can directly add widgets to it (default: QVBoxLayout).
        
        - setContentLayout(layout: QLayout)
            Replaces the default content layout with your own.
            The widget auto-detects scroll direction:
                * QVBoxLayout  -> vertical scrolling
                * QHBoxLayout  -> horizontal scrolling
                * Other layouts -> both directions

    Features:
        - Always hides scrollbars
        - Scroll with touch (if available)
        - Scroll with mouse drag (panning)
        - Mouse wheel support (maps to horizontal when using QHBoxLayout)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Outer layout (no margins)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.setStyleSheet("background: transparent;outline:none;border:0px solid #ffffff;")

        # Content widget (holds user layout)
        self.content = QWidget()
        self.scroll.setWidget(self.content)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        # Default layout = vertical
        self._content_layout = QVBoxLayout(self.content)
        self._content_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.scroll)

        # State
        self._orientation = Qt.Vertical
        self._panning = False
        self._press_global = QPoint()
        self._start_v = 0
        self._start_h = 0
        self._dragged = False
        self._drag_threshold = QApplication.startDragDistance()

        # Setup gestures + drag fallback
        self._enableTouchScrolling()
        self._installEventFilters()

        # Hide scrollbars
        self._hideScrollbars()

    # ----------- Public API -----------

    def contentLayout(self):
        """Return the current layout inside the scrollable content."""
        return self._content_layout

    def setContentLayout(self, layout):
        """
        Replace the default layout with a custom one.
        Scroll direction is auto-detected:
            - QVBoxLayout  -> vertical scrolling
            - QHBoxLayout  -> horizontal scrolling
            - Other layout -> both directions
        """
        QWidget().setLayout(self._content_layout)  # detach old layout
        self._content_layout = layout
        self.content.setLayout(layout)

        self._detectOrientation(layout)
        self._installEventFilters()

    # ----------- Internals -----------

    def _detectOrientation(self, layout):
        """Set orientation mode based on layout type."""
        if isinstance(layout, QVBoxLayout):
            self._orientation = Qt.Vertical
        elif isinstance(layout, QHBoxLayout):
            self._orientation = Qt.Horizontal
        else:
            self._orientation = None  # both

    def _hideScrollbars(self):
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def _enableTouchScrolling(self):
        vp = self.scroll.viewport()
        vp.setAttribute(Qt.WA_AcceptTouchEvents, True)
        try:
            QScroller.grabGesture(vp, QScroller.TouchGesture)
        except Exception:
            pass  # some platforms may not support touch

    def _installEventFilters(self):
        """Watch viewport + children for drag/wheel events."""
        vp = self.scroll.viewport()
        vp.installEventFilter(self)
        self.content.installEventFilter(self)
        for w in self.content.findChildren(QWidget):
            w.installEventFilter(self)

    def eventFilter(self, obj, event):
        et = event.type()

        # Track new children so we keep filtering
        if et == QEvent.ChildAdded:
            child = event.child()
            if isinstance(child, QWidget):
                child.installEventFilter(self)
            return False

        # --- Mouse pan fallback ---
        if et == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self._panning = True
            self._dragged = False
            self._press_global = event.globalPos()
            self._start_v = self.scroll.verticalScrollBar().value()
            self._start_h = self.scroll.horizontalScrollBar().value()
            return False  # don’t swallow yet (might be click)

        if et == QEvent.MouseMove and self._panning:
            delta = event.globalPos() - self._press_global
            if not self._dragged and (abs(delta.x()) > self._drag_threshold or abs(delta.y()) > self._drag_threshold):
                self._dragged = True

            if self._dragged:
                if self._orientation in (None, Qt.Vertical):
                    self.scroll.verticalScrollBar().setValue(self._start_v - delta.y())
                if self._orientation in (None, Qt.Horizontal):
                    self.scroll.horizontalScrollBar().setValue(self._start_h - delta.x())
                event.accept()
                return True
            return False

        if et == QEvent.MouseButtonRelease and self._panning:
            self._panning = False
            if self._dragged:
                event.accept()
                return True
            return False

        # --- Mouse wheel → horizontal remap ---
        if et == QEvent.Wheel and self._orientation == Qt.Horizontal:
            dy = event.angleDelta().y()
            sb = self.scroll.horizontalScrollBar()
            sb.setValue(sb.value() - dy)
            event.accept()
            return True

        return False