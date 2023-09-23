from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QMainWindow, \
 QListWidgetItem, QPlainTextEdit, QCheckBox, QScrollArea, QGraphicsScene, QGraphicsView, \
    QGraphicsProxyWidget, QGraphicsRectItem
from PyQt6.QtGui import QPen, QLinearGradient, QColor, QIcon, QGradient, QFont, QAction
from PyQt6.QtCore import Qt, QPointF
from PyQt6 import QtGui, QtCore
from user import *
from listBoxWidget import *
from lineEditWidget import *
from ellipseItem import *
import random as rand
import threading


class MainWindow(QMainWindow):
    def __init__(self, user: User):
        super().__init__()
        self.user = user
        self.file_imported = False  # True when csv-file has been imported
        self.last_clicked = False  # True for income; False for expenses
        self.other_process = False  # Controls what messages to output when creating the pie charts
        self.income = self.user.get_income()
        self.expenses: dict[str, list] = self.user.get_expenses()
        self.savings_expenses: dict[str, list] = {}
        self.expenses_total: float = sum([value[0] for value in self.expenses.values()])
        self.income_total: float = sum([value[0] for value in self.income.values()])
        self.last_input: str = ""
        self.savings_amount: float = 0.0
        self.show_sum: float = 0.0
        self.show_savings_sum: float = 0.0
        self.setGeometry(100, 100, 1280, 600)
        self.resize(1280, 1024)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create Grid layout on which all the widget will be build
        self.grid = QGridLayout(self.centralWidget())
        self.grid.setRowStretch(1, 4)
        self.grid.setRowStretch(2, 1)
        self.grid.setColumnStretch(0, 5)
        self.grid.setColumnStretch(1, 5)
        self.grid.setColumnStretch(2, 3)
        self.grid.setColumnStretch(3, 3)

        # Create widgets
        self.create_upper_buttons()
        self.create_info()
        self.create_menu_bar()
        self.create_status_bar()
        self.create_drag_and_drop()
        self.create_warning_display()
        self.create_important_button()
        self.create_unimportant_button()
        self.create_save_money_button()
        self.create_group_button()
        self.create_group_text_field()
        self.create_box()
        self.create_upper_label_sum()
        self.create_upper_label_savings()
        self.create_save_text_field()

        self.show()

    def update_warning_display(self, warning_message: str):
        self.warning_label.setText("  " + warning_message)

    def create_warning_display(self):
        self.warning_label = QLabel()
        self.warning_label.setText("  " + "Welcome to MyMoney Manager.")
        self.warning_label.setStyleSheet("background:#FFFBEB; color:#EB6440;")
        self.warning_label.setStatusTip("Warning message box.")
        self.grid.addWidget(self.warning_label, 4, 0, 1, 1)

    def savings_algorithm(self):
        important_expenses: dict = {}
        unimportant_expenses: dict = {}
        self.savings_expenses: dict = {}
        try:
            if not self.file_imported:
                self.update_warning_display("No files have been imported yet.")  # MESSAGE
            elif self.savings_amount >= 0:
                for key, values in self.expenses.items():
                    if values[1]:
                        important_expenses[key] = values.copy()
                    else:
                        unimportant_expenses[key] = values.copy()

                unimp_exp_sum = sum([values[0] for key, values in unimportant_expenses.items()])

                if abs(unimp_exp_sum) >= self.savings_amount:   # check if savings amount is bigger than the sum of unimportant expenses.
                    savings_share: dict = {key: ((values[0] / unimp_exp_sum) * self.savings_amount) for key, values in
                                           unimportant_expenses.items()}
                    for key in unimportant_expenses.keys():
                        unimportant_expenses[key][0] = unimportant_expenses[key][0] + savings_share[key]

                    self.savings_expenses.update(unimportant_expenses)
                    self.savings_expenses.update(important_expenses)
                    self.graph_savings_plot()
                    self.checkbox_on_stateChanged()
                    self.update_warning_display("Savings pie chart created successfully.")  # MESSAGE
                else:
                    self.update_warning_display("Savings amount should be smaller.")  # MESSAGE
                    self.change_save_text_field_colour()

            else:
                self.update_warning_display("Savings amount should be a positive number.")  # MESSAGE
                self.change_save_text_field_colour()

        except TypeError:
            self.update_warning_display("Please type in savings amount as a numeric value.")  # MESSAGE
            self.change_save_text_field_colour()

        except Exception:
            self.update_warning_display("Savings algorithm not working. Contact the customer service for help.")  # MESSAGE

    def text_changed_save(self, text: str):
        try:
            text = text.replace(",", ".")
            self.savings_amount = float(text)
        except ValueError:
            self.savings_amount = 0.0
            self.update_warning_display("Please type in savings amount as a numeric value.")  # MESSAGE
            self.change_save_text_field_colour()
        except TypeError:
            self.savings_amount = 0.0
            self.update_warning_display("Please type in savings amount as a numeric value.")  # MESSAGE
            self.change_save_text_field_colour()

    def create_save_money_button(self):
        btn_save = QPushButton('Save money')
        btn_save.setGeometry(50, 400, 200, 50)
        btn_save.setStatusTip("Press to calculate savings.")
        btn_save.clicked.connect(self.savings_algorithm)
        self.grid.addWidget(btn_save, 3, 2, 1, 1)

    def create_save_text_field(self):
        self.btn_save_amount = LineEditWidget(" Savings amount")
        self.btn_save_amount.setFont(QFont("Helvetica", italic=True))
        self.btn_save_amount.setStyleSheet("color: rgba(0, 0, 0, 40)")
        self.btn_save_amount.setGeometry(50, 400, 200, 50)
        self.btn_save_amount.setStatusTip("Input saving amount based on which savings pie chart will be graphed.")
        self.btn_save_amount.textChanged.connect(self.text_changed_save)
        self.grid.addWidget(self.btn_save_amount, 4, 2, 1, 1)

    def change_save_text_field_colour(self):
        def back_to_original():    # save amount input field returns to normal after 2 seconds
            self.btn_save_amount.setStyleSheet("color: rgba(0, 0, 0, 40)")
        self.btn_save_amount.setStyleSheet("border: 1px solid red; color: rgba(0, 0, 0, 40)")
        threading.Timer(2.0, back_to_original).start()

    def delete_row(self):
        delete_list: list = []
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                delete_list.append(checkbox.text())
        message = self.user.delete_row(delete_list)

        self.update_warning_display(message)  # MESSAGE
        self.expenses = self.user.get_expenses()
        self.savings_expenses = self.expenses
        self.show_savings_sum = 0.0
        self.update_screen()
        self.other_process = True

    def update_screen(self):
        self.create_expenses_piechart()
        self.show_sum = 0
        self.create_upper_label_sum()
        self.create_upper_label_savings()
        self.create_box()
        self.other_process = False

    def text_changed_group(self, text):
        self.last_input = text

    def group_expenses(self):
        grouping_list: list = []
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                grouping_list.append(checkbox.text())
        message, success = self.user.set_grouping(grouping_list, self.last_input)
        self.update_warning_display(message)  # MESSAGE
        if not success and message != "No rows checked.":
            self.change_group_text_field_colour()
        self.expenses = self.user.get_expenses()
        self.savings_expenses = self.expenses
        self.other_process = True
        if len(grouping_list) != 0 and self.last_input != "":
            self.show_savings_sum = 0.0
            self.update_screen()

    def change_group_text_field_colour(self):
        def back_to_original():    # group title input field returns to normal after 2 seconds
            self.btn_group_title.setStyleSheet("color: rgba(0, 0, 0, 40)")
        self.btn_group_title.setStyleSheet("border: 1px solid red; color: rgba(0, 0, 0, 40)")
        threading.Timer(2.0, back_to_original).start()

    def create_group_button(self):
        btn_group = QPushButton('Group')
        btn_group.setGeometry(50, 400, 200, 50)
        btn_group.setStatusTip("Press to group rows.")
        btn_group.clicked.connect(self.group_expenses)
        self.grid.addWidget(btn_group, 3, 3, 1, 1)

    def create_group_text_field(self):
        self.btn_group_title = LineEditWidget(" Group title")
        self.btn_group_title.setFont(QFont("Helvetica", italic=True))
        self.btn_group_title.setStyleSheet("color: rgba(0, 0, 0, 40)")
        self.btn_group_title.setGeometry(50, 400, 200, 50)
        self.btn_group_title.setStatusTip("Input group title that will be set to the new group of merged expenses.")
        self.btn_group_title.textChanged.connect(self.text_changed_group)
        self.grid.addWidget(self.btn_group_title, 4, 3, 1, 1)

    def set_importance(self):
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                message = self.user.set_importance(checkbox.text())
                self.update_warning_display(message)  # MESSAGE
                checkbox.setStyleSheet("color: red")

    def unset_importance(self):
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                message = self.user.unset_importance(checkbox.text())
                self.update_warning_display(message)  # MESSAGE
                checkbox.setStyleSheet("color: black")

    def create_important_button(self):
        self.btn_imp = QPushButton("Set importance")
        self.btn_imp.setGeometry(50, 400, 200, 50)
        self.btn_imp.setStatusTip("Press to set row importance.")
        self.btn_imp.clicked.connect(lambda: self.set_importance())
        self.grid.addWidget(self.btn_imp, 3, 1, 1, 1)

    def create_unimportant_button(self):
        self.btn_unimp = QPushButton("Unset importance")
        self.btn_unimp.setGeometry(50, 400, 200, 50)
        self.btn_unimp.setStatusTip("Press to unset row importance.")
        self.btn_unimp.clicked.connect(lambda: self.unset_importance())
        self.grid.addWidget(self.btn_unimp, 4, 1, 1, 1)

    def create_checkbox_scroll(self):
        scroll = QScrollArea()
        scroll.setStyleSheet("background:rgb(175, 211, 226);")
        scroll.setStatusTip("Window where expenses rows can be modified.")
        self.box.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(800)
        self.scroll_content = QWidget(scroll)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        scroll.setWidget(self.scroll_content)

    def on_stateChanged(self, state):
        for checkbox in self.checkboxes:
            checkbox.setCheckState(state)

    def create_all_checkbox(self):
        self.select_all_box = QCheckBox("Select all")
        self.select_all_box.stateChanged.connect(self.on_stateChanged)
        self.select_all_box.setStatusTip("Select all checkboxes simultaneously.")
        self.box.addWidget(self.select_all_box)

    def checkbox_on_stateChanged(self):
        counter = 0
        counter_savings = 0
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                counter += self.expenses[checkbox.text()][0]
                if len(self.savings_expenses) != 0:
                    counter_savings += (self.expenses[checkbox.text()][0] - self.savings_expenses[checkbox.text()][0])
        self.show_sum = counter
        self.show_savings_sum = abs(counter_savings)
        if self.expenses_total != 0:
            self.b3.setText(" Checked €:   " + str(round(self.show_sum, 2)) + " (" + str(round(abs(self.show_sum / self.expenses_total) * 100, 2)) + "%)")
        else:
            self.b3.setText(" Checked €:   " + str(round(self.show_sum, 2)) + " (" + str(0.0) + "%)")
        self.b4.setText(" Savings €:   " + str(round(self.show_savings_sum, 2)))

    def create_upper_label_sum(self):
        self.b3 = QLabel()
        if self.expenses_total != 0:
            self.b3.setText(" Checked €:   " + str(round(self.show_sum, 2)) + " (" + str(round(abs(self.show_sum / self.expenses_total) * 100, 2)) + "%)")
        else:
            self.b3.setText(" Checked €:   " + str(round(self.show_sum, 2)) + " (" + str(0.0) + "%)")
        self.b3.setStyleSheet("background:#AFD3E2; color:rgb(57, 48, 83);")
        self.b3.setStatusTip("Row sum display.")
        self.grid.addWidget(self.b3, 0, 2)

    def create_upper_label_savings(self):
        self.b4 = QLabel()
        self.b4.setText(" Savings €:   " + str(round(self.show_savings_sum, 2)))
        self.b4.setStyleSheet("background:#AFD3E2; color:rgb(57, 48, 83);")
        self.b4.setStatusTip("Row percent display.")
        self.grid.addWidget(self.b4, 0, 3)

    def create_checkboxes(self):
        checkbox_labels = [checkbox.text() for checkbox in self.checkboxes]

        for key in self.expenses:
            if key not in checkbox_labels:
                new_checkbox = QCheckBox(key)
                self.scroll_layout.addWidget(new_checkbox)
                new_checkbox.stateChanged.connect(self.checkbox_on_stateChanged)
                self.checkboxes.append(new_checkbox)

        for checkbox in self.checkboxes:
            if self.expenses[checkbox.text()][1]:
                checkbox.setStyleSheet("color: red")
            else:
                checkbox.setStyleSheet("color: black")

    def create_load_button(self):
        btn_load = QPushButton('Load file')
        btn_load.setGeometry(50, 400, 200, 50)
        btn_load.setStatusTip("Press to load selected file.")
        return btn_load

    def create_drag_and_drop(self):
        btn_load = self.create_load_button()

        self.lst = ListBoxWidget()
        self.lst.setStyleSheet("background:rgb(175, 211, 226);")
        self.lst.setStatusTip("Drop files to this field.")

        self.grid.addWidget(self.lst, 2, 0, 1, 2)
        self.grid.addWidget(btn_load, 3, 0, 1, 1)

        btn_load.clicked.connect(lambda: self.getSelectedItem())
        btn_load.clicked.connect(lambda: self.create_checkboxes())

    def getSelectedItem(self):
        item = QListWidgetItem(self.lst.currentItem())
        if item.text() != "":
            self.import_file(item.text())
            if self.last_clicked:
                return self.b1.click()
            else:
                return self.b2.click()
        else:
            message = "Drag and drop a file to above field and select it first."
            self.update_warning_display(message)    # MESSAGE

    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menubar.setObjectName("Menubar")
        menuFile = menubar.addMenu("&Other Operations")
        menuFile.setObjectName("Menufile")
        menuFile.setStatusTip("Operations for clearing and deletion.")

        clear_action = QAction("&Clear", self)
        menuFile.addAction(clear_action)

        info_action = QAction("&Info", self)
        menuFile.addAction(info_action)

        delete_action = QAction("&Delete", self)
        menuFile.addAction(delete_action)

        quit_action = QAction("&Quit", self)
        menuFile.addAction(quit_action)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MyMoney Manager"))

        clear_action.setText(_translate("MainWindow", "Clear window"))
        clear_action.setShortcut(_translate("MainWindow", "Ctrl+C"))
        clear_action.setStatusTip(_translate("MainWindow", "Clear the window."))
        clear_action.triggered.connect(self.clear_window)

        info_action.setText(_translate("MainWindow", "Show info"))
        info_action.setShortcut(_translate("MainWindow", "Ctrl+I"))
        info_action.setStatusTip(_translate("MainWindow", "Show information text."))
        info_action.triggered.connect(self.create_info)

        delete_action.setText(_translate("MainWindow", "Delete row"))
        delete_action.setShortcut(_translate("MainWindow", "Ctrl+D"))
        delete_action.setStatusTip(_translate("MainWindow", "Delete row by first checking the expenses box."))
        delete_action.triggered.connect(self.delete_row)

        quit_action.setText(_translate("MainWindow", "Quit "))
        quit_action.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        quit_action.setStatusTip(_translate("MainWindow", "Quit the program."))
        quit_action.triggered.connect(QApplication.quit)

        QtCore.QMetaObject.connectSlotsByName(self)

    def create_status_bar(self):
        statusbar = self.statusBar()
        statusbar.setObjectName("Statusbar")
        statusbar.showMessage("Welcome to the money management app! Please read the above instructions to start with.")

    def import_file(self, path_file: str):
        success, message = self.user.import_file(path_file)
        self.update_warning_display(message)  # MESSAGE
        if success:
            self.file_imported = True
            self.expenses = self.user.get_expenses()
            self.savings_expenses = self.expenses

    def clear_window(self):
        self.file_imported = False
        # Clear all previous data
        self.user.get_expenses().clear()
        self.user.get_income().clear()
        self.income.clear()
        self.expenses.clear()
        # Reset chart view
        empty = QPlainTextEdit()
        empty.setStyleSheet("background:rgb(175, 211, 226);")
        self.grid.addWidget(empty, 1, 0, 1, 2)
        # Reset drag and drop
        self.create_drag_and_drop()
        # Reset Box
        self.create_box()
        # Reset text fields
        self.create_group_text_field()
        self.create_save_text_field()

    def create_box(self):
        self.box = QVBoxLayout()
        self.create_checkbox_scroll()
        self.create_all_checkbox()
        self.checkboxes: list[QCheckBox] = []
        self.create_checkboxes()
        self.grid.addLayout(self.box, 1, 2, 2, 2)

    def create_info(self):
        info = QPlainTextEdit()
        info.setStyleSheet("background:rgb(175, 211, 226);color:rgb(57, 48, 83);")
        info.setStatusTip("Instructions for using MyMoney Manager")
        self.file_imported = False
        info.insertPlainText("1) Drag and drop bank files in csv format to below window to graph a pie chart.\n\n"
                             "2) Switch between income and expenses graphs by clicking above buttons \"Income\" and \"Expenses\".\n\n"
                             "3) Check expenses checkboxes on the right to group expenses rows and set their importance:\n"
                             "  - Rows in red are set as important expenses.\n"
                             "  - The program automatically sets most frequent and sum wise biggest expenses as important.\n"
                             "  - Use unset importance button to set expenses row as unimportant.\n"
                             "  - In order to group, write title of the new group and press \" Group\" button.\n"
                             "  - Expenses row can also be just renamed by checking only one row.\n\n"
                             "4) Click \"Other operations\" from above menu bar in order to do additional operations:\n"
                             "  - Choose \"Clear window\" to clear loaded bank files and graphs.\n"
                             "  - Choose \"Show info\" to display this info text whenever it is needed.\n"
                             "  - Choose \"Delete row\" to delete specific rows from the left.\n"
                             "  - Choose \"Quit\" to exit the program.\n\n"
                             "5) Graph a savings pie chart by writing savings amount and pressing \"Save Money\":\n"
                             "  - The graph will show suggested expenses amounts based on importance settings of expenses rows.\n"
                             "  - Savings amounts will not be applied to important expenses.")
        self.grid.addWidget(info, 1, 0, 1, 2)

    def create_upper_buttons(self):
        self.b1 = QPushButton(self)
        self.b2 = QPushButton(self)

        font_buttons = QtGui.QFont()
        font_buttons.setPointSize(15)
        self.b1.setFont(font_buttons)
        self.b2.setFont(font_buttons)
        self.b1.setText("Income")
        self.b2.setText("Expenses")
        self.b1.setStatusTip("Graph income related diagram.")
        self.b2.setStatusTip("Graph expenses related diagram.")

        self.grid.addWidget(self.b1, 0, 0)
        self.grid.addWidget(self.b2, 0, 1)
        self.b1.clicked.connect(self.create_income_piechart)
        self.b2.clicked.connect(self.create_expenses_piechart)

    # Expenses pie chart
    def create_expenses_piechart(self):
        self.graph_scene_exp = QGraphicsScene()
        self.expenses_total = sum([value[0] for value in self.expenses.values()])
        set_angle = 0
        slices_index = 0
        colours = []
        legend_pos_horizontal = -310
        legend_pos_vertical = -100
        title_pos_horizontal = -55
        title_pos_vertical = -185

        for colour in range(len(self.expenses)):
            number = []
            for rgb in range(3):
                number.append(rand.randrange(0, 255))
            colours.append(QColor(number[0], number[1], number[2]))

        for key, values in self.expenses.items():
            # Creating pie chart slices
            angle = round(float(values[0] * 5760) / self.expenses_total)
            pie_slice = EllipseItem(key, values, self.expenses_total, self.graph_scene_exp)
            pie_slice.setStartAngle(set_angle)
            pie_slice.setSpanAngle(angle)
            pie_slice.setBrush(colours[slices_index])
            pie_slice.setPen(QPen(colours[slices_index]))
            pie_slice.setZValue(1)
            set_angle += angle
            self.graph_scene_exp.addItem(pie_slice)

            # Creating legends
            legend = QLabel()
            pie_slice.add_legend(legend)  # add to ellipseItem in order to change colour
            legend.setText("{} {}€ ({}%)".format(key, str(round(values[0], 2)),
                                                 str(round(abs(values[0] / float(self.expenses_total) * 100), 1))))
            legend.setAutoFillBackground(False)
            legend.setStyleSheet('background-color: transparent')
            font_legend = QtGui.QFont('Times', 13)
            font_legend.setBold(False)
            legend.setFont(font_legend)
            proxy_legend = QGraphicsProxyWidget(pie_slice)
            proxy_legend.setWidget(legend)
            proxy_legend.setZValue(-1)
            proxy_legend.setPos(legend_pos_horizontal, legend_pos_vertical)

            # Creating legend colourboxes
            legend_box = QGraphicsRectItem(legend_pos_horizontal - 20, legend_pos_vertical, 10, 10)
            legend_box.setBrush(colours[slices_index])

            self.graph_scene_exp.addItem(pie_slice)
            self.graph_scene_exp.addItem(legend_box)
            slices_index += 1
            legend_pos_vertical += 20

        # Background colour
        backgroundGradient = QLinearGradient()
        backgroundGradient.setStart(QPointF(0, 0))
        backgroundGradient.setFinalStop(0, 1)
        backgroundGradient.setColorAt(0.0, QColor(175, 201, 182))
        backgroundGradient.setColorAt(1.0, QColor(51, 105, 66))
        self.graph_scene_exp.setBackgroundBrush(backgroundGradient)

        # Set title
        title = QLabel()
        title.setText("Expenses Piechart")
        title.setAutoFillBackground(False)
        title.setStyleSheet('background-color:transparent; color:rgb(0,100,0);')
        font_title = QtGui.QFont('Times', 26)
        font_title.setBold(True)
        title.setFont(font_title)
        proxy_title = QGraphicsProxyWidget()
        proxy_title.setWidget(title)
        proxy_title.setPos(title_pos_horizontal, title_pos_vertical)
        proxy_title.setWindowFrameMargins(0, 20, 0, 0)

        if len(self.expenses) != 0:
            self.graph_scene_exp.addItem(proxy_title)

        # Set expenses total subtitle
        total_subtitle = QLabel()
        total_subtitle.setText("Total Expenses {} €".format(round(self.expenses_total, 2)))
        total_subtitle.setAutoFillBackground(False)
        total_subtitle.setStyleSheet('background-color:transparent; color:rgb(0,100,0);')
        font_subtitle = QtGui.QFont('Times', 26)
        font_subtitle.setBold(True)
        title.setFont(font_subtitle)
        proxy_subtitle = QGraphicsProxyWidget()
        proxy_subtitle.setWidget(total_subtitle)
        proxy_subtitle.setPos(title_pos_horizontal + 20, title_pos_vertical + 25)

        if len(self.expenses) != 0:
            self.graph_scene_exp.addItem(proxy_subtitle)

        graph_view = QGraphicsView()
        graph_view.setScene(self.graph_scene_exp)

        # Status tip and warning display
        if self.file_imported:
            if not self.other_process:
                graph_view.setStatusTip("Expenses pie chart.")
                self.update_warning_display("Expenses pie chart created successfully.")  # MESSAGE
        else:
            if not self.other_process:
                graph_view.setStatusTip("Load files to graph a diagram.")
                self.update_warning_display("Load files before graphing a pie chart.")  # MESSAGE

        self.last_clicked = False
        self.grid.addWidget(graph_view, 1, 0, 1, 2)

    # Income pie chart
    def create_income_piechart(self):
        self.graph_scene_income = QGraphicsScene()
        self.income_total = sum([value[0] for value in self.income.values()])
        set_angle = 0
        slices_index = 0
        colours = []
        legend_pos_horizontal = -310
        legend_pos_vertical = -100
        title_pos_horizontal = -55
        title_pos_vertical = -185

        for colour in range(len(self.income)):
            number = []
            for rgb in range(3):
                number.append(rand.randrange(0, 255))
            colours.append(QColor(number[0], number[1], number[2]))

        for key, values in self.income.items():
            # Creating pie chart slices
            angle = round(float(
                values[0] * 5760) / self.income_total)  # Max span is 5760 -> have to calculate corresponding span angle
            pie_slice = EllipseItem(key, values, self.income_total, self.graph_scene_income)
            pie_slice.setStartAngle(set_angle)
            pie_slice.setSpanAngle(angle)
            pie_slice.setBrush(colours[slices_index])
            pie_slice.setPen(QPen(colours[slices_index]))
            pie_slice.setZValue(1)
            set_angle += angle
            self.graph_scene_income.addItem(pie_slice)

            # Creating legends
            legend = QLabel()
            pie_slice.add_legend(legend)  # add to ellipseItem in order to change colour
            legend.setText("{} {}€ ({}%)".format(key, str(round(values[0], 2)),
                                                 str(round(abs(values[0] / float(self.income_total) * 100), 1))))
            legend.setAutoFillBackground(False)
            legend.setStyleSheet('background-color: transparent')
            font_legend = QtGui.QFont('Times', 13)
            font_legend.setBold(False)
            legend.setFont(font_legend)
            proxy_legend = QGraphicsProxyWidget(pie_slice)
            proxy_legend.setWidget(legend)
            proxy_legend.setZValue(-1)
            proxy_legend.setPos(legend_pos_horizontal, legend_pos_vertical)

            # Creating legend colour boxes
            legend_box = QGraphicsRectItem(legend_pos_horizontal - 20, legend_pos_vertical, 10, 10)
            legend_box.setBrush(colours[slices_index])

            self.graph_scene_income.addItem(pie_slice)
            self.graph_scene_income.addItem(legend_box)
            slices_index += 1
            legend_pos_vertical += 20

        # Background colour
        backgroundGradient = QLinearGradient()
        backgroundGradient.setStart(QPointF(0, 0))
        backgroundGradient.setFinalStop(0, 1)
        backgroundGradient.setColorAt(0.0, QColor(175, 201, 182))
        backgroundGradient.setColorAt(1.0, QColor(51, 105, 66))
        self.graph_scene_income.setBackgroundBrush(backgroundGradient)

        # Set title
        title = QLabel()
        title.setText("Income Pie chart")
        title.setAutoFillBackground(False)
        title.setStyleSheet('background-color:transparent; color:rgb(0,100,0);')
        font_title = QtGui.QFont('Times', 26)
        font_title.setBold(True)
        title.setFont(font_title)
        proxy_title = QGraphicsProxyWidget()
        proxy_title.setWidget(title)
        proxy_title.setPos(title_pos_horizontal, title_pos_vertical)
        proxy_title.setWindowFrameMargins(0, 20, 0, 0)

        if len(self.income) != 0:
            self.graph_scene_income.addItem(proxy_title)

        # Set expenses total subtitle
        total_subtitle = QLabel()
        total_subtitle.setText("Total Income {} €".format(round(self.income_total, 2)))
        total_subtitle.setAutoFillBackground(False)
        total_subtitle.setStyleSheet('background-color:transparent; color:rgb(0,100,0);')
        font_subtitle = QtGui.QFont('Times', 26)
        font_subtitle.setBold(True)
        title.setFont(font_subtitle)
        proxy_subtitle = QGraphicsProxyWidget()
        proxy_subtitle.setWidget(total_subtitle)
        proxy_subtitle.setPos(title_pos_horizontal + 20, title_pos_vertical + 25)

        if len(self.income) != 0:
            self.graph_scene_income.addItem(proxy_subtitle)

        graph_view = QGraphicsView()
        graph_view.setScene(self.graph_scene_income)

        # Statustip and warning display
        if self.file_imported:
            if not self.other_process:
                graph_view.setStatusTip("Income pie chart.")
                self.update_warning_display("Income pie chart created successfully.")  # MESSAGE
        else:
            if not self.other_process:
                graph_view.setStatusTip("Load files to graph a diagram.")
                self.update_warning_display("Load files before graphing a pie chart.")  # MESSAGE

        self.last_clicked = True
        self.grid.addWidget(graph_view, 1, 0, 1, 2)

    # Savings pie chart
    def graph_savings_plot(self):
        self.graph_scene_savings = QGraphicsScene()
        savings_total = sum([value[0] for value in self.savings_expenses.values()])
        set_angle = 0
        slices_index = 0
        colours = []
        legend_pos_horizontal = -310
        legend_pos_vertical = -100
        title_pos_horizontal = -55
        title_pos_vertical = -185

        for colour in range(len(self.savings_expenses)):
            number = []
            for rgb in range(3):
                number.append(rand.randrange(0, 255))
            colours.append(QColor(number[0], number[1], number[2]))

        for key, values in self.savings_expenses.items():
            # Creating pie chart slices
            angle = round(float(
                values[0] * 5760) / savings_total)  # Max span is 5760 -> have to calculate corresponding span angle
            pie_slice = EllipseItem(key, values, savings_total, self.graph_scene_savings)
            pie_slice.setStartAngle(set_angle)
            pie_slice.setSpanAngle(angle)
            pie_slice.setBrush(colours[slices_index])
            pie_slice.setPen(QPen(colours[slices_index]))
            pie_slice.setZValue(1)
            set_angle += angle
            self.graph_scene_savings.addItem(pie_slice)

            # Creating legends
            legend = QLabel()
            pie_slice.add_legend(legend)  # add to ellipseItem in order to change colour
            legend.setText("{} {}€ ({}%)".format(key, str(round(values[0], 2)),
                                                 str(round(abs(values[0] / float(savings_total) * 100), 1))))
            legend.setAutoFillBackground(False)
            legend.setStyleSheet('background-color: transparent')
            font_legend = QtGui.QFont('Times', 13)
            font_legend.setBold(False)
            legend.setFont(font_legend)
            proxy_legend = QGraphicsProxyWidget(pie_slice)
            proxy_legend.setWidget(legend)
            proxy_legend.setZValue(-1)
            proxy_legend.setPos(legend_pos_horizontal, legend_pos_vertical)

            # Creating legend colourboxes
            legend_box = QGraphicsRectItem(legend_pos_horizontal - 20, legend_pos_vertical, 10, 10)
            legend_box.setBrush(colours[slices_index])

            self.graph_scene_savings.addItem(pie_slice)
            self.graph_scene_savings.addItem(legend_box)
            slices_index += 1
            legend_pos_vertical += 20

        # Background colour
        backgroundGradient = QLinearGradient()
        backgroundGradient.setStart(QPointF(0, 0))
        backgroundGradient.setFinalStop(0, 1)
        backgroundGradient.setColorAt(0.0, QColor(175, 100, 182))
        backgroundGradient.setColorAt(1.0, QColor(51, 105, 66))
        self.graph_scene_savings.setBackgroundBrush(backgroundGradient)

        # Set title
        title = QLabel()
        title.setText("Savings Piechart")
        title.setAutoFillBackground(False)
        title.setStyleSheet('background-color:transparent; color:rgb(0,100,0);')
        font_title = QtGui.QFont('Times', 26)
        font_title.setBold(True)
        title.setFont(font_title)
        proxy_title = QGraphicsProxyWidget()
        proxy_title.setWidget(title)
        proxy_title.setPos(title_pos_horizontal, title_pos_vertical)
        proxy_title.setWindowFrameMargins(0, 20, 0, 0)

        if len(self.savings_expenses) != 0:
            self.graph_scene_savings.addItem(proxy_title)

        # Set expenses savings_total subtitle
        total_subtitle = QLabel()
        total_subtitle.setText(
            "Total Expenses {} €\nTotal Savings {} €".format(round(savings_total, 2), self.savings_amount))
        total_subtitle.setAutoFillBackground(False)
        total_subtitle.setStyleSheet('background-color:transparent; color:rgb(0,100,0);')
        font_subtitle = QtGui.QFont('Times', 26)
        font_subtitle.setBold(True)
        title.setFont(font_subtitle)
        proxy_subtitle = QGraphicsProxyWidget()
        proxy_subtitle.setWidget(total_subtitle)
        proxy_subtitle.setPos(title_pos_horizontal + 20, title_pos_vertical + 25)

        if len(self.savings_expenses) != 0:
            self.graph_scene_savings.addItem(proxy_subtitle)

        graph_view = QGraphicsView()
        graph_view.setScene(self.graph_scene_savings)

        # Statustip and warning display
        if self.file_imported:
            if not self.other_process:
                graph_view.setStatusTip("Savings piechart.")
                self.update_warning_display("Savings piechart created successfully.")  # MESSAGE
        else:
            if not self.other_process:
                graph_view.setStatusTip("Load files to graph a diagram.")
                self.update_warning_display("Load files before graphing a pie chart.")  # MESSAGE

        self.last_clicked = False
        self.grid.addWidget(graph_view, 1, 0, 1, 2)
