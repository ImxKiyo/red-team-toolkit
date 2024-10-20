# tabs/port_scanner_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem

class PortScannerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_port_scanner_tab()

    def init_port_scanner_tab(self):
        layout = QVBoxLayout()

        title_label = QLabel("Port Scanner", self)
        layout.addWidget(title_label)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL or IP")
        layout.addWidget(self.url_input)

        scan_button = QPushButton("Scan Ports", self)
        scan_button.clicked.connect(self.scan_ports)
        layout.addWidget(scan_button)

        self.results_table = QTableWidget(0, 2, self)
        self.results_table.setHorizontalHeaderLabels(["Port", "Status"])
        layout.addWidget(self.results_table)

        self.setLayout(layout)

    def scan_ports(self):
        url = self.url_input.text()
        # Placeholder for actual port scanning logic
        print(f"Scanning ports for {url}...")
        # Dummy data for demonstration
        results = [(22, "Closed"), (80, "Open"), (443, "Open")]
        self.results_table.setRowCount(len(results))
        for row, (port, status) in enumerate(results):
            self.results_table.setItem(row, 0, QTableWidgetItem(str(port)))
            self.results_table.setItem(row, 1, QTableWidgetItem(status))
