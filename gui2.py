import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

class ScientiFlowApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ScientiFlow GUI")
        self.setGeometry(100, 100, 400, 250) # x, y, width, height

        # Central stacked widget to switch between login and main app views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create UI components
        self.login_widget = QWidget()
        self.main_app_widget = QWidget()

        self.init_login_ui()
        self.init_main_app_ui()

        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.main_app_widget)

        # Start with the login screen
        self.show_login_screen()

    def init_login_ui(self):
        layout = QVBoxLayout(self.login_widget)
        layout.setContentsMargins(50, 30, 50, 30) # left, top, right, bottom margins
        layout.setSpacing(15) # spacing between widgets

        title_label = QLabel("ScientiFlow Login")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(35)
        layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(35)
        layout.addWidget(self.password_input)

        # Login button
        login_button = QPushButton("Login")
        login_button.setMinimumHeight(40)
        login_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; }"
                                   "QPushButton:hover { background-color: #45a049; }")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        
        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.login_widget.setLayout(layout)

    def init_main_app_ui(self):
        layout = QVBoxLayout(self.main_app_widget)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(15)

        self.welcome_label = QLabel("Welcome to ScientiFlow!")
        welcome_font = QFont()
        welcome_font.setPointSize(16)
        self.welcome_label.setFont(welcome_font)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.welcome_label)

        # Placeholder for application content (could be more complex)
        app_content_placeholder = QLabel("Application content would appear here.")
        app_content_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(app_content_placeholder, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Logout button
        logout_button = QPushButton("Logout")
        logout_button.setMinimumHeight(40)
        logout_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; border-radius: 5px; }"
                                    "QPushButton:hover { background-color: #da190b; }")
        logout_button.clicked.connect(self.handle_logout)
        
        # Button layout to control size
        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        button_layout.addWidget(logout_button)
        logout_button.setFixedWidth(100) # Fixed width for logout button
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        layout.addLayout(button_layout)
        
        self.main_app_widget.setLayout(layout)

    def handle_login(self):
        # Basic validation (can be expanded)
        username = self.username_input.text()
        # password = self.password_input.text() # Password not used in this demo

        if username: # For demo, just check if username is not empty
            self.welcome_label.setText(f"Welcome, {username}!")
            self.show_main_app_screen()
        else:
            # You could add an error message display here
            print("Login failed: Username cannot be empty.")
            # Simple error handling - maybe show a QMessageBox
            from PyQt6.QtWidgets import QMessageBox
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Login Failed")
            msg_box.setInformativeText("Username cannot be empty.")
            msg_box.setWindowTitle("Error")
            msg_box.exec()


    def handle_logout(self):
        # Clear username and password fields upon logout
        self.username_input.clear()
        self.password_input.clear()
        self.show_login_screen()

    def show_login_screen(self):
        self.stacked_widget.setCurrentWidget(self.login_widget)
        self.setWindowTitle("ScientiFlow GUI - Login")
        self.resize(400, 300) # Resize for login screen

    def show_main_app_screen(self):
        self.stacked_widget.setCurrentWidget(self.main_app_widget)
        self.setWindowTitle("ScientiFlow GUI - Main Application")
        self.resize(500, 400) # Resize for main app screen


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ScientiFlowApp()
    main_window.show()
    sys.exit(app.exec())
