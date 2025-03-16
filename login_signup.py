import sys
import smtplib
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from dashboard import Dashboard  

class LoginSignupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WanderMate - Login/Signup")
        self.showMaximized()  
        self.users = {}  
        self.init_ui()

    def init_ui(self):
  
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("background.jpg").scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        self.background.setGeometry(0, 0, self.width(), self.height())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_container = QWidget()
        form_container.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            padding: 20px;
        """)
        form_layout = QVBoxLayout()

        title = QLabel("WanderMate")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: yellow;
            margin-bottom: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(title)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            margin-bottom: 10px;
            color: yellow;
            background-color: rgba(255, 255, 255, 0.1);
        """)
        form_layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            margin-bottom: 20px;
            color: yellow;
            background-color: rgba(255, 255, 255, 0.1);
        """)
        form_layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            margin-bottom: 10px;
        """)
        self.login_button.clicked.connect(self.login)
        form_layout.addWidget(self.login_button)

        self.signup_button = QPushButton("Signup")
        self.signup_button.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            background-color: #2196F3;
            color: white;
        """)
        self.signup_button.clicked.connect(self.signup)
        form_layout.addWidget(self.signup_button)

        form_container.setLayout(form_layout)
        main_layout.addWidget(form_container)
        self.central_widget.setLayout(main_layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        if email not in self.users:
            QMessageBox.warning(self, "Error", "User does not exist. Please sign up.")
            return

        if not self.users[email]["verified"]:
            QMessageBox.warning(self, "Error", "Please verify your email before logging in.")
            return

        if self.users[email]["password"] != password:
            QMessageBox.warning(self, "Error", "Incorrect password.")
            return

        QMessageBox.information(self, "Login", f"Logged in as {email}")

        
        self.dashboard = Dashboard(email)  
        self.dashboard.show()
        self.close()  

    def signup(self):
        email = self.email_input.text()
        password = self.password_input.text()
        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        # Check if the user already exists
        if email in self.users:
            QMessageBox.warning(self, "Error", "User already exists. Please log in.")
            return

        self.users[email] = {"password": password, "verified": False}

        # Send verification email using Mailtrap
        try:
            self.send_verification_email(email)
            QMessageBox.information(self, "Signup", "Verification email sent! Please check your inbox.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send email: {str(e)}")

    def send_verification_email(self, email):
        # Mailtrap SMTP settings
        smtp_server = "sandbox.smtp.mailtrap.io"
        smtp_port = 465
        smtp_username = "25b3cd22d3de3a"  
        smtp_password = "fb5d8bdd48dbae"  

        # Email content
        subject = "Verify Your WanderMate Account"
        body = "Click the link to verify your account: http://wanderMate.com/verify"

        # Create the email
        message = f"Subject: {subject}\n\n{body}"

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail("noreply@wanderMate.com", email, message)
        self.users[email]["verified"] = True 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginSignupWindow()
    window.show()
    sys.exit(app.exec())