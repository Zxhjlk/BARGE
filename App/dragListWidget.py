from PyQt6.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal


class DraggableListWidget(QListWidget):
    itemDropped = pyqtSignal(QListWidgetItem, QListWidget, QListWidget)

    def __init__(self, type, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.type = type

    def dragEnterEvent(self, e):
        e.accept() if e.mimeData().hasFormat(
            "application/x-qabstractitemmodeldatalist"
        ) else e.ignore()

    def dragMoveEvent(self, e):
        e.accept() if e.mimeData().hasFormat(
            "application/x-qabstractitemmodeldatalist"
        ) else e.ignore()

    def dropEvent(self, e):
        if e.source() == self:
            e.setDropAction(Qt.DropAction.MoveAction)
            super().dropEvent(e)
        else:
            sourceListWidget = e.source()
            item = sourceListWidget.currentItem()

            self.itemDropped.emit(item, sourceListWidget, self)
            e.accept()
