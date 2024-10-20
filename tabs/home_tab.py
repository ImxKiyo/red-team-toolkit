from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QListWidget, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from modules.domain_info import DomainInfo  # Ensure this import is correct
from modules.ping import ping_website
from tabs.results_tab import ResultsTab
from tabs.domain_info_tab import DomainInfoTab  # Import the DomainInfoTab class


class HomeTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_home_tab()

    def init_home_tab(self):
        layout = QVBoxLayout()

        # Add spacing above the logo for better balance
        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Load and display the logo (smaller size)
        self.logo_label = QLabel(self)
        pixmap = QPixmap("assets/red_team_logo.png")
        self.logo_label.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))  # Adjust logo path if needed
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        # Reduce spacing between logo and input box
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # URL Input box
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL")
        self.url_input.setFixedWidth(200)
        self.url_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.url_input.setStyleSheet("padding: 5px; border-radius: 10px;")

        # Center the input box
        input_layout = QHBoxLayout()
        input_layout.addStretch(1)
        input_layout.addWidget(self.url_input)
        input_layout.addStretch(1)
        layout.addLayout(input_layout)

        # Reduce spacing between input box and full scan button
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Full Scan Button
        self.full_scan_btn = QPushButton("Full Scan", self)
        self.full_scan_btn.clicked.connect(self.full_scan)
        self.full_scan_btn.setFixedWidth(150)
        self.full_scan_btn.setStyleSheet("padding: 10px; border-radius: 10px;")

        # Center Full Scan Button
        full_scan_layout = QHBoxLayout()
        full_scan_layout.addStretch(1)
        full_scan_layout.addWidget(self.full_scan_btn)
        full_scan_layout.addStretch(1)
        layout.addLayout(full_scan_layout)

        # Add some spacing after the full scan button (before the tool buttons)
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Tool buttons
        tools_layout = QHBoxLayout()
        tool_names = [
            "Domain Info And Subdomains",
            "Port Scanner", "SQL Injection Checker",
            "HTML Injection Checker", "Cross-Site Scripting Checker"
        ]
        for tool in tool_names:
            button = QPushButton(tool, self)
            if tool == "Domain Info And Subdomains":
                button.clicked.connect(self.open_domain_info_tab)  # Link to specific method for domain info
            else:
                button.clicked.connect(self.open_tool_tab)
            button.setFixedSize(150, 100)
            button.setStyleSheet("padding: 10px; border-radius: 15px;")
            tools_layout.addWidget(button)

        # Center the buttons horizontally with space between them
        layout.addLayout(tools_layout)

        # Add more space below tool buttons for a balanced layout
        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        layout.addLayout(tools_layout)

        self.setLayout(layout)

    def open_domain_info_tab(self):
        """Opens the Domain Info and Subdomains Tab."""
        domain_info_tab = DomainInfoTab(self.main_window)
        self.main_window.tabs.addTab(domain_info_tab, f"Domain Info & Subdomains")
        self.main_window.tabs.setCurrentWidget(domain_info_tab)

    def open_tool_tab(self):
        sender = self.sender()
        tool_name = sender.text()

        # Create a new tab for the tool
        tool_tab = QWidget()
        tool_layout = QVBoxLayout()

        # Title and input box
        tool_title = QLabel(tool_name, self)
        tool_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tool_layout.addWidget(tool_title)

        # Input box
        input_box = QLineEdit(self)
        input_box.setPlaceholderText(f"Enter data for {tool_name}")
        tool_layout.addWidget(input_box)

        # Results area
        results_label = QLabel("Results", self)
        tool_layout.addWidget(results_label)

        tool_tab.setLayout(tool_layout)
        self.main_window.tabs.addTab(tool_tab, tool_name)
        self.main_window.tabs.setCurrentWidget(tool_tab)

    def full_scan(self):
        url = self.url_input.text()
        print(f"Scanning URL: {url}")  # Debugging output

        # Normalize URL by adding "http://" if it doesn't start with "http"
        if not url.startswith("http"):
            url = "http://" + url

        print(f"Normalized URL: {url}")  # Debugging output

        if not url.startswith("http"):  # Basic validation
            error_tab = QWidget()
            error_layout = QVBoxLayout()

            error_msg = QLabel("Invalid URL, please check and try again.")
            error_layout.addWidget(error_msg)

            back_button = QPushButton("Back to Home", self)
            back_button.clicked.connect(lambda: self.tabs.removeTab(self.tabs.currentIndex()))
            error_layout.addWidget(back_button)

            error_tab.setLayout(error_layout)
            self.tabs.addTab(error_tab, "Error")
            self.tabs.setCurrentWidget(error_tab)
            return

        # Ping the URL to check if it's reachable
        print(f"Pinging URL: {url}")  # Debugging output
        if not ping_website(url):
            error_tab = QWidget()
            error_layout = QVBoxLayout()

            error_msg = QLabel(f"The URL '{url}' is down. Please check and try again.")
            error_layout.addWidget(error_msg)

            back_button = QPushButton("Back to Home", self)
            back_button.clicked.connect(lambda: self.tabs.removeTab(self.tabs.currentIndex()))
            error_layout.addWidget(back_button)

            error_tab.setLayout(error_layout)
            self.tabs.addTab(error_tab, "Error")
            self.tabs.setCurrentWidget(error_tab)
            return

        # Create Full Scan Results Tab
        results_tab = ResultsTab(url, self.main_window)
        self.main_window.tabs.addTab(results_tab, f"Full Scan: {url}")
        self.main_window.tabs.setCurrentWidget(results_tab)

    def show_error(self, message):
        error_tab = QWidget()
        error_layout = QVBoxLayout()
        error_msg = QLabel(message)
        error_layout.addWidget(error_msg)

        back_button = QPushButton("Back to Home", self)
        back_button.clicked.connect(lambda: self.main_window.tabs.removeTab(self.main_window.tabs.currentIndex()))
        error_layout.addWidget(back_button)

        error_tab.setLayout(error_layout)
        self.main_window.tabs.addTab(error_tab, "Error")
        self.main_window.tabs.setCurrentWidget(error_tab)
