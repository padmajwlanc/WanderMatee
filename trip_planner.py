from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QDateEdit, QTimeEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog, QLabel
)
from PyQt6.QtCore import QDate, QTime
import winsound  # For playing alarm tones on Windows
import threading  # For running the alarm in the background

class TripPlannerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.trips = []  # List to store trips
        self.alarm_tone = None  # Selected alarm tone file path
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Add Trip Form
        add_trip_section = QWidget()
        add_trip_layout = QHBoxLayout()

        # Destination Input
        self.destination_input = QLineEdit()
        self.destination_input.setPlaceholderText("Destination")
        self.destination_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        add_trip_layout.addWidget(self.destination_input)

        # Start Date Input
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)  # Enable calendar popup
        self.start_date_input.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        add_trip_layout.addWidget(self.start_date_input)

        # Start Time Input
        self.start_time_input = QTimeEdit()
        self.start_time_input.setTime(QTime.currentTime())
        self.start_time_input.setStyleSheet("""
            QTimeEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        add_trip_layout.addWidget(self.start_time_input)

        # End Date Input
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)  # Enable calendar popup
        self.end_date_input.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        add_trip_layout.addWidget(self.end_date_input)

        # End Time Input
        self.end_time_input = QTimeEdit()
        self.end_time_input.setTime(QTime.currentTime())
        self.end_time_input.setStyleSheet("""
            QTimeEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        add_trip_layout.addWidget(self.end_time_input)

        # Add Trip Button
        add_trip_button = QPushButton("Add Trip")
        add_trip_button.setStyleSheet("""
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
        add_trip_button.clicked.connect(self.add_trip)
        add_trip_layout.addWidget(add_trip_button)

        add_trip_section.setLayout(add_trip_layout)
        layout.addWidget(add_trip_section)

        # Alarm Tone Selection
        alarm_tone_section = QWidget()
        alarm_tone_layout = QHBoxLayout()

        self.alarm_tone_label = QLabel("Alarm Tone:")
        self.alarm_tone_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.select_alarm_tone_button = QPushButton("Select Alarm Tone")
        self.select_alarm_tone_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.select_alarm_tone_button.clicked.connect(self.select_alarm_tone)
        alarm_tone_layout.addWidget(self.alarm_tone_label)
        alarm_tone_layout.addWidget(self.select_alarm_tone_button)

        alarm_tone_section.setLayout(alarm_tone_layout)
        layout.addWidget(alarm_tone_section)

        # Trip List
        self.trip_table = QTableWidget()
        self.trip_table.setColumnCount(6)
        self.trip_table.setHorizontalHeaderLabels(["Destination", "Start Date", "Start Time", "End Date", "End Time", "Remind Me"])
        self.trip_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.trip_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #3897f0;
                color: white;
                padding: 8px;
            }
        """)
        layout.addWidget(self.trip_table)

        self.setLayout(layout)

    def add_trip(self):
        # Get trip details
        destination = self.destination_input.text()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        start_time = self.start_time_input.time().toString("HH:mm")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        end_time = self.end_time_input.time().toString("HH:mm")

        if not destination:
            QMessageBox.warning(self, "Error", "Please enter a destination.")
            return

        # Add trip to the list
        self.trips.append((destination, start_date, start_time, end_date, end_time))

        # Update the trip table
        self.update_trip_table()

        # Clear the input fields
        self.destination_input.clear()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_time_input.setTime(QTime.currentTime())
        self.end_date_input.setDate(QDate.currentDate())
        self.end_time_input.setTime(QTime.currentTime())

    def update_trip_table(self):
        self.trip_table.setRowCount(len(self.trips))
        for i, trip in enumerate(self.trips):
            self.trip_table.setItem(i, 0, QTableWidgetItem(trip[0]))
            self.trip_table.setItem(i, 1, QTableWidgetItem(trip[1]))
            self.trip_table.setItem(i, 2, QTableWidgetItem(trip[2]))
            self.trip_table.setItem(i, 3, QTableWidgetItem(trip[3]))
            self.trip_table.setItem(i, 4, QTableWidgetItem(trip[4]))

            # Add "Remind Me" button
            remind_button = QPushButton("Remind Me")
            remind_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            remind_button.clicked.connect(lambda _, idx=i: self.set_reminder(idx))
            self.trip_table.setCellWidget(i, 5, remind_button)

    def set_reminder(self, trip_index):
        # Get the trip's start time
        start_date = self.trips[trip_index][1]
        start_time = self.trips[trip_index][2]

        # Combine date and time into a single datetime string
        from datetime import datetime
        alarm_time = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")

        # Calculate the time difference in seconds
        current_time = datetime.now()
        time_difference = (alarm_time - current_time).total_seconds()

        if time_difference <= 0:
            QMessageBox.warning(self, "Error", "The selected time has already passed.")
            return

        # Set a timer to trigger the alarm
        timer = threading.Timer(time_difference, self.trigger_alarm)
        timer.start()

        QMessageBox.information(self, "Reminder Set", f"Reminder set for {start_date} {start_time}.")

    def trigger_alarm(self):
        # Play the selected alarm tone
        if self.alarm_tone:
            winsound.PlaySound(self.alarm_tone, winsound.SND_FILENAME)  # Play the selected .wav file
        else:
            winsound.Beep(500, 1000)  # Default beep

    def select_alarm_tone(self):
        # Open a file dialog to select an alarm tone
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Audio Files (*.wav)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            # Get the selected file path
            self.alarm_tone = file_dialog.selectedFiles()[0]
            QMessageBox.information(self, "Alarm Tone Selected", f"Alarm tone set to: {self.alarm_tone}")