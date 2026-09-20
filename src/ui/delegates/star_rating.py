from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtGui import QPainter, QColor, QFontMetrics
from PyQt6.QtCore import Qt, QSize, QEvent

class StarRatingDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.star_inactive = QColor('#3d444d')
        self.font_size = 16
        
    def get_rating_color(self, rating):
        if rating == 1: return QColor('#ef4444')
        if rating == 2: return QColor('#f97316')
        if rating == 3: return QColor('#eab308')
        if rating == 4: return QColor('#22c55e')
        if rating == 5: return QColor('#a855f7')
        return QColor('#fbbf24')

    def paint(self, painter: QPainter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rating = index.data(Qt.ItemDataRole.EditRole)
        try:
            rating = int(rating)
        except (ValueError, TypeError):
            rating = 0
            
        font = painter.font()
        font.setPointSize(self.font_size)
        painter.setFont(font)
        
        rect = option.rect
        fm = painter.fontMetrics()
        star_width = fm.horizontalAdvance("★ ")
        
        total_width = star_width * 5
        start_x = rect.x() + (rect.width() - total_width) // 2
        y = rect.y() + (rect.height() + fm.ascent() - fm.descent()) // 2
        
        active_color = self.get_rating_color(rating)
        
        for i in range(5):
            painter.setPen(active_color if i < rating else self.star_inactive)
            painter.drawText(start_x + i * star_width, y, "★ ")
            
        painter.restore()
        
    def sizeHint(self, option, index):
        font = option.font
        font.setPointSize(self.font_size)
        fm = QFontMetrics(font)
        return QSize(fm.horizontalAdvance("★ ") * 5 + 10, fm.height() + 10)
        
    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease:
            rect = option.rect
            font = option.font
            font.setPointSize(self.font_size)
            fm = QFontMetrics(font)
            star_width = fm.horizontalAdvance("★ ")
            total_width = star_width * 5
            start_x = rect.x() + (rect.width() - total_width) // 2
            
            click_x = event.position().x()
            if start_x <= click_x <= start_x + total_width:
                rating = int((click_x - start_x) // star_width) + 1
                model.setData(index, rating, Qt.ItemDataRole.EditRole)
                return True
        return super().editorEvent(event, model, option, index)
