import sys

from PySide6.QtWidgets import QApplication

from bll import BusinessLogic
from dal import DataAccess
from interface import Interface

def run() -> None:
    dal = DataAccess()
    dal.import_cards()
    bll = BusinessLogic(dal = dal)

    app = QApplication([])

    window = Interface(bll = bll)
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    run()