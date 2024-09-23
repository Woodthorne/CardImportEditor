from PySide6.QtCore import Qt
# from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget
)

from bll import BusinessLogic


class Interface(QMainWindow):
    def __init__(self, bll: BusinessLogic) -> None:
        super(Interface, self).__init__()
        self._bll = bll
    
        self.setWindowTitle('CardImportEditor')

        widget = QWidget()
        file_group = self._create_file_group()
        card_scroll = self._create_card_scroll()
        button_group = self._create_button_group()

        layout = QVBoxLayout()
        layout.addWidget(file_group)
        layout.addWidget(card_scroll)
        layout.addWidget(button_group)

        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def _create_file_group(self) -> QGroupBox:
        source, target = self._bll.get_source_target_paths()
        
        file_group = QGroupBox()
        source_label = QLabel(f'Source path: {source.absolute()}')
        target_label = QLabel(f'Target path: {target.absolute()}')

        layout = QVBoxLayout()
        layout.addWidget(source_label)
        layout.addWidget(target_label)

        file_group.setLayout(layout)

        return file_group
    
    def _create_card_scroll(self) -> QScrollArea:
        scroll = QScrollArea()
        card_list = QWidget()
        self.card_inputs: dict[str, dict[str, QLineEdit]] = {}

        list_layout = QGridLayout()
        name_label = QLabel('Card name')
        set_code_label = QLabel('Set Code')
        collector_number_label = QLabel('Collector Number')
        list_layout.addWidget(name_label, 0, 0)
        list_layout.addWidget(set_code_label, 0, 1)
        list_layout.addWidget(collector_number_label, 0, 2)
        for index, card in enumerate(self._bll.get_cards()):
            card_name = QLabel(card.name)
            card_set_code = QLineEdit()
            card_set_code.setText(card.set_code)
            card_set_code.setAlignment(Qt.AlignmentFlag.AlignRight)
            card_set_code.setFixedWidth(40)
            card_collector_number = QLineEdit()
            card_collector_number.setText(card.collector_number)
            card_collector_number.setAlignment(Qt.AlignmentFlag.AlignRight)
            card_collector_number.setFixedWidth(40)

            self.card_inputs[card.name] = {
                'set_code': card_set_code,
                'collector_number': card_collector_number
            }
            
            list_layout.addWidget(card_name, index + 1, 0)
            list_layout.addWidget(card_set_code, index + 1, 1)
            list_layout.addWidget(card_collector_number, index + 1, 2)
        
        card_list.setLayout(list_layout)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidget(card_list)

        return scroll
    
    def _create_button_group(self) -> QGroupBox:
        button_group = QGroupBox()

        import_button = QPushButton('Import')
        import_button.pressed.connect(self._import_cards)

        export_button = QPushButton('Export')
        export_button.pressed.connect(self._export_cards)

        layout = QHBoxLayout()
        layout.addWidget(import_button)
        layout.addWidget(export_button)

        button_group.setLayout(layout)

        return button_group
    
    def _import_cards(self) -> None:
        self._bll.import_cards()
    
    def _export_cards(self) -> None:
        for card in self._bll.get_cards():
            if card.name not in self.card_inputs:
                continue

            card.set_code = self.card_inputs[card.name]['set_code'].text()
            card.collector_number = self.card_inputs[card.name]['collector_number'].text()
        
        self._bll.export_cards()
    