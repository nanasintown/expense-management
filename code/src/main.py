from mainWindow import *
from user import *
import sys


def main():
    app = QApplication(sys.argv)
    reader = FileManager()
    user = User(reader)
    mainWind = MainWindow(user)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
