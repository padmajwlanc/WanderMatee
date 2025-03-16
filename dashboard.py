from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QTextEdit, QTabWidget, QDialog, QGridLayout, QFileDialog
)
from PyQt6.QtGui import QPixmap, QColor, QFont
from PyQt6.QtCore import Qt
from trip_planner import TripPlannerTab  # Add a dot before the module name  # Ensure the import statement is correct

class Dashboard(QMainWindow):
    def __init__(self, email):
        super().__init__()
        self.email = email
        self.setWindowTitle(f"WanderMate - Dashboard ({email})")
        self.setGeometry(100, 100, 1200, 800)
        self.theme = "light"  # Default theme
        self.init_ui()

    def init_ui(self):
        # Create a tabbed interface
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add the Profile Tab
        self.tabs.addTab(self.create_profile_tab(), "Profile")

        # Add the Trip Planner Tab
        self.tabs.addTab(TripPlannerTab(), "Trip Planner")  # Add the TripPlannerTab

    def create_profile_tab(self):
        profile_tab = QWidget()
        layout = QVBoxLayout()

        # Profile Section
        profile_section = QWidget()
        profile_layout = QHBoxLayout()

        # Profile picture (circular with border)
        self.profile_picture = QLabel()
        self.profile_picture.setPixmap(QPixmap("profile_placeholder.jpg").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.profile_picture.setStyleSheet("""
            QLabel {
                border: 3px solid #ddd;
                border-radius: 50px;
                padding: 5px;
            }
        """)
        profile_layout.addWidget(self.profile_picture, alignment=Qt.AlignmentFlag.AlignCenter)

        # Update Profile Picture Button
        update_picture_button = QPushButton("Update Profile Picture")
        update_picture_button.setStyleSheet("""
            QPushButton {
                background-color: #3897f0;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2684f0;
            }
        """)
        update_picture_button.clicked.connect(self.update_profile_picture)
        profile_layout.addWidget(update_picture_button, alignment=Qt.AlignmentFlag.AlignCenter)

        profile_section.setLayout(profile_layout)
        layout.addWidget(profile_section)

        # Stats Section
        stats_section = QWidget()
        stats_layout = QHBoxLayout()

        # Number of Connections Made
        self.connections_label = QLabel("Connections: 0")
        self.connections_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        stats_layout.addWidget(self.connections_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # History
        self.history_label = QLabel("History: No trips yet")
        self.history_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        stats_layout.addWidget(self.history_label, alignment=Qt.AlignmentFlag.AlignCenter)

        stats_section.setLayout(stats_layout)
        layout.addWidget(stats_section)

        # Edit Profile Section
        edit_section = QWidget()
        edit_layout = QVBoxLayout()

        # Enter Username
        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        edit_layout.addWidget(self.username_label)
        edit_layout.addWidget(self.username_input)

        # Enter Phone Number
        self.phone_label = QLabel("Phone Number:")
        self.phone_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        self.phone_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        edit_layout.addWidget(self.phone_label)
        edit_layout.addWidget(self.phone_input)

        # Edit Profile Button
        edit_profile_button = QPushButton("Edit Profile")
        edit_profile_button.setStyleSheet("""
            QPushButton {
                background-color: #3897f0;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2684f0;
            }
        """)
        edit_profile_button.clicked.connect(self.edit_profile)
        edit_layout.addWidget(edit_profile_button)

        edit_section.setLayout(edit_layout)
        layout.addWidget(edit_section)

        # Change Theme Button
        change_theme_button = QPushButton("Change Theme")
        change_theme_button.setStyleSheet("""
            QPushButton {
                background-color: #3897f0;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2684f0;
            }
        """)
        change_theme_button.clicked.connect(self.show_color_palette)
        layout.addWidget(change_theme_button)

        profile_tab.setLayout(layout)
        return profile_tab

    def edit_profile(self):
        # Get the updated username and phone number
        new_username = self.username_input.text()
        new_phone = self.phone_input.text()

        # Update the labels
        self.username_label.setText(f"Username: {new_username}")
        self.phone_label.setText(f"Phone Number: {new_phone}")

        # Show a confirmation message
        QMessageBox.information(self, "Profile Updated", "Your profile has been updated.")

    def show_color_palette(self):
        # Create a dialog for the color palette
        color_dialog = QDialog(self)
        color_dialog.setWindowTitle("Choose a Theme Color")
        color_dialog.setFixedSize(300, 200)

        # Create a grid layout for the color buttons
        grid_layout = QGridLayout()

        # Define a list of colors
        colors = [
            ("Light", "#FFFFFF"),  # White
            ("Dark", "#333333"),   # Dark Gray
            ("Blue", "#0078D7"),   # Blue
            ("Green", "#4CAF50"),  # Green
            ("Red", "#F44336"),    # Red
            ("Purple", "#9C27B0"), # Purple
        ]

        # Add buttons for each color
        for i, (name, color) in enumerate(colors):
            button = QPushButton(name)
            button.setStyleSheet(f"background-color: {color}; color: white;")
            button.clicked.connect(lambda _, c=color: self.change_theme(c))
            grid_layout.addWidget(button, i // 2, i % 2)

        color_dialog.setLayout(grid_layout)
        color_dialog.exec()

    def change_theme(self, color):
        # Update the application's stylesheet based on the selected color
        self.setStyleSheet(f"""
            background-color: {color};
            color: {'white' if color != "#FFFFFF" else 'black'};
        """)

    def update_profile_picture(self):
        # Open a file dialog to select an image
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            # Get the selected file path
            file_path = file_dialog.selectedFiles()[0]

            # Load the image and set it as the profile picture
            pixmap = QPixmap(file_path)
            self.profile_picture.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    window = Dashboard("test@example.com")
    window.show()
    app.exec()