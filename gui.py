import sys
# No hashlib for this simple demo, but real apps need it for secure passwords
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QFont, QPixmap


DEMO_USERNAME = "user"
DEMO_PASSWORD = "password123" # Plain text password for demo

class SciFlowGUI_PyQt(QWidget):
    def __init__(self):
        super().__init__()
        self.logged_in_user = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ScientiFlow - Secure Access") # Title updated
        self.setGeometry(300, 300, 420, 330) # Adjusted height for password field

        # --- Set background image using the provided path ---
        self.image_path = r"C:\Users\gayat\OneDrive\Pictures\Screenshots\Screenshot 2025-05-17 175426.png"
        
        self.background_label = QLabel(self)
        self.update_background_pixmap()
        self.background_label.lower()

        # --- Main Layout Container ---
        container_widget = QWidget(self)
        container_widget.setStyleSheet("QWidget { background-color: transparent; }")

        self.central_widget_layout = QVBoxLayout(container_widget)
        self.central_widget_layout.setContentsMargins(35, 35, 35, 35)
        self.central_widget_layout.setSpacing(18) # Adjusted spacing
        self.central_widget_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Title Label ---
        title_label = QLabel("ScientiFlow")
        title_font = QFont('Segoe UI', 22, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                background-color: rgba(0, 0, 0, 0.4);
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 15px;
            }
        """)
        self.central_widget_layout.addWidget(title_label)

        # --- Username ---
        username_layout = QHBoxLayout()
        self.username_label = QLabel("Username:")
        self.username_label.setFont(QFont('Segoe UI', 11))
        # Black text with a light semi-transparent background for readability
        self.username_label.setStyleSheet("""
            QLabel { 
                color: black; 
                background-color: rgba(255, 255, 255, 0.7); /* Light semi-transparent bg */
                padding: 3px 5px; /* Add some padding */
                border-radius: 3px; /* Rounded corners for the bg */
            }
        """)

        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Enter username") # Placeholder updated
        self.username_entry.setFont(QFont('Segoe UI', 11))
        self.username_entry.setStyleSheet("""
            QLineEdit {
                background-color: rgba(50, 50, 50, 0.85);
                color: #E0E0E0;
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 8px;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border: 1px solid #0078D7;
                background-color: rgba(60, 60, 60, 0.9);
            }
        """)
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_entry)
        self.central_widget_layout.addLayout(username_layout)

        # --- Password Field (Re-added) ---
        password_layout = QHBoxLayout()
        self.password_label = QLabel("Password:")
        self.password_label.setFont(QFont('Segoe UI', 11))
        # Black text with a light semi-transparent background for readability
        self.password_label.setStyleSheet("""
            QLabel { 
                color: black; 
                background-color: rgba(255, 255, 255, 0.7); /* Light semi-transparent bg */
                padding: 3px 5px; /* Add some padding */
                border-radius: 3px; /* Rounded corners for the bg */
            }
        """)

        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Enter password")
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password) # Hides password input
        self.password_entry.setFont(QFont('Segoe UI', 11))
        self.password_entry.setStyleSheet("""
            QLineEdit {
                background-color: rgba(50, 50, 50, 0.85);
                color: #E0E0E0;
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 8px;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border: 1px solid #0078D7;
                background-color: rgba(60, 60, 60, 0.9);
            }
        """)
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_entry)
        self.central_widget_layout.addLayout(password_layout)


        # --- Buttons ---
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.login_button = QPushButton("Login") # Text back to "Login"
        self.login_button.setFont(QFont('Segoe UI', 11, QFont.Weight.Bold))
        self.login_button.setMinimumHeight(40)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                padding: 10px 15px;
            }
            QPushButton:hover { background-color: #005A9E; }
            QPushButton:pressed { background-color: #004C87; }
            QPushButton:disabled { background-color: #5A5A5A; color: #9E9E9E; }
        """)
        self.login_button.clicked.connect(self.handle_login)
        buttons_layout.addWidget(self.login_button)

        self.logout_button = QPushButton("Logout")
        self.logout_button.setFont(QFont('Segoe UI', 11, QFont.Weight.Bold))
        self.logout_button.setMinimumHeight(40)
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F;
                color: white;
                border-radius: 5px;
                padding: 10px 15px;
            }
            QPushButton:hover { background-color: #B71C1C; }
            QPushButton:pressed { background-color: #9A1313; }
            QPushButton:disabled { background-color: #5A5A5A; color: #9E9E9E; }
        """)
        self.logout_button.clicked.connect(self.handle_logout)
        self.logout_button.setEnabled(False)
        buttons_layout.addWidget(self.logout_button)
        self.central_widget_layout.addLayout(buttons_layout)

        # --- Status Label ---
        self.status_label = QLabel("Status: Awaiting login") # Updated status text
        self.status_label.setFont(QFont('Segoe UI', 10))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #D0D0D0;
                background-color: rgba(0, 0, 0, 0.3);
                padding: 5px;
                border-radius: 3px;
                margin-top: 10px;
            }
        """)
        self.central_widget_layout.addWidget(self.status_label)
        
        main_window_layout = QVBoxLayout(self)
        main_window_layout.addWidget(container_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_window_layout)

        self.show()

    def update_background_pixmap(self):
        pixmap = QPixmap(self.image_path)
        if pixmap.isNull():
            print(f"Warning: Could not load background image from {self.image_path}. Check the path.")
            self.setStyleSheet("QWidget { background-color: #2D2D2D; }")
            if hasattr(self, 'background_label'):
                self.background_label.hide()
        else:
            self.setStyleSheet("") 
            if hasattr(self, 'background_label'):
                self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
                self.background_label.setGeometry(0, 0, self.width(), self.height())
                self.background_label.show()

    def resizeEvent(self, event):
        self.update_background_pixmap()
        super().resizeEvent(event)

    def handle_login(self):
        username = self.username_entry.text()
        password = self.password_entry.text() # Get password input

        if not username.strip() or not password.strip():
            QMessageBox.warning(self, "Input Required", "Username and Password cannot be empty.")
            self.status_label.setText("Status: Username/Password required.")
            self.status_label.setStyleSheet("QLabel { color: #FF9800; font-weight: bold; background-color: rgba(0,0,0,0.3); padding:5px; border-radius:3px; }")
            if not password.strip() and username.strip(): # if only password missing
                 self.password_entry.setFocus()
            else: # if username missing or both missing
                 self.username_entry.setFocus()
            return

        # !!! INSECURE PLAIN TEXT PASSWORD CHECK - FOR DEMONSTRATION ONLY !!!
        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            self.logged_in_user = username
            self.status_label.setText(f"Status: Logged in as {self.logged_in_user}")
            self.status_label.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; background-color: rgba(0,0,0,0.3); padding:5px; border-radius:3px; }")
            QMessageBox.information(self, "Login Successful", f"Welcome, {self.logged_in_user}!")

            self.login_button.setEnabled(False)
            self.logout_button.setEnabled(True)
            self.username_entry.setEnabled(False)
            self.password_entry.setEnabled(False) # Disable password field
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
            self.status_label.setText("Status: Invalid credentials.")
            self.status_label.setStyleSheet("QLabel { color: #F44336; font-weight: bold; background-color: rgba(0,0,0,0.3); padding:5px; border-radius:3px; }")
            self.password_entry.clear() # Clear only password on fail
            self.password_entry.setFocus()


    def handle_logout(self):
        if self.logged_in_user:
            QMessageBox.information(self, "Logout Successful", f"{self.logged_in_user} has been logged out.")
        self.logged_in_user = None
        self.status_label.setText("Status: Awaiting login")
        self.status_label.setStyleSheet("QLabel { color: #D0D0D0; background-color: rgba(0,0,0,0.3); padding:5px; border-radius:3px; margin-top: 10px; }")
        
        self.login_button.setEnabled(True)
        self.logout_button.setEnabled(False)
        self.username_entry.setEnabled(True)
        self.password_entry.setEnabled(True) # Enable password field
        self.username_entry.clear()
        self.password_entry.clear() # Clear password field
        self.username_entry.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Ensure PyQt6 is installed: pip install PyQt6
    login_window = SciFlowGUI_PyQt()
    sys.exit(app.exec())
