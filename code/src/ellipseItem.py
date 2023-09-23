from PyQt6.QtWidgets import QGraphicsEllipseItem, QLabel, QGraphicsScene


class EllipseItem(QGraphicsEllipseItem):
    def __init__(self, key: str, values: list, expenses_total: float, graph_scene: QGraphicsScene, parent=None):
        super().__init__(parent)
        self.proxy = None
        self.setRect(10, -105, 400, 400)
        self.key = key
        self.values = values
        self.expenses_total = expenses_total
        self.graph_scene = graph_scene
        self.legend: QLabel = QLabel()
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.change_pie_label_colour()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.pie_label_to_original()

    def change_pie_label_colour(self):
        self.legend.setStyleSheet("background-color:transparent; color:rgb(255,0,0)")

    def pie_label_to_original(self):
        self.legend.setStyleSheet("background-color:transparent; color:rgb(0,0,0)")

    def add_legend(self, added_legend: QLabel):
        self.legend = added_legend
