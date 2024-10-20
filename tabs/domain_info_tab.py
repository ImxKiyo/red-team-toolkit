from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QListWidget, QLineEdit, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from modules.domain_info import DomainInfo  # Ensure the correct path for your module


class DomainInfoTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.url_input = None
        self.layout = None
        self.init_domain_info_tab()

    def init_domain_info_tab(self):
        """Initialize the tab with input field and layout for domain information."""
        self.layout = QVBoxLayout()

        # Heading for the tab
        heading_label = QLabel("Domain and Subdomain Information", self)
        heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading_label.setStyleSheet("font-size: 24px; font-weight: bold; color: rgb(215, 38, 61);")
        self.layout.addWidget(heading_label)

        # Input box for domain entry
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter domain and press Enter (e.g., example.com)")
        self.url_input.setStyleSheet("font-size: 16px;")
        self.url_input.setFixedWidth(400)  # Medium size input box
        self.url_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.url_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Connect Enter key press to trigger results display
        self.url_input.returnPressed.connect(self.on_enter_pressed)

        # Spacer to center content when there are no results
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(self.spacer)

        # Placeholder for dynamic content (domain info and subdomains)
        self.setLayout(self.layout)

    def on_enter_pressed(self):
        """Handle the Enter key press to display domain info and subdomains."""
        url = self.url_input.text().strip()
        if url:
            self.clear_previous_results()
            self.url = url
            self.display_domain_info(self.layout)
            self.display_subdomains(self.layout)

    def clear_previous_results(self):
        """Clear previous domain information and subdomains from the layout."""
        while self.layout.count() > 2:  # Keep the heading and input box
            widget = self.layout.takeAt(2).widget()
            if widget:
                widget.deleteLater()

    def display_domain_info(self, layout):
        """Fetch and display domain information in a table."""
        domain_info_container = QVBoxLayout()
        domain_info_label = QLabel("Domain Information", self)
        domain_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        domain_info_label.setStyleSheet("font-size: 18px; font-weight: bold; color: rgb(215, 38, 61);")
        domain_info_container.addWidget(domain_info_label)

        try:
            # Use DomainInfo to fetch domain information
            domain_info = DomainInfo(self.url)
            dom_info = domain_info.find_dom_info()

            if "Error" in dom_info:
                # Handle error case
                error_msg = QLabel(f"Failed to fetch domain information: {dom_info['Error']}", self)
                domain_info_container.addWidget(error_msg)
                layout.addLayout(domain_info_container)
                return  # Exit early if there's an error

            if isinstance(dom_info, dict):
                # Add IP address to domain information
                ip_address = domain_info.dom_to_ip()  # Always attempt to resolve IP
                dom_info["IP Address"] = ip_address if isinstance(ip_address, str) else "Could not resolve IP"

                # Domain Information Table
                domain_info_table = QTableWidget(len(dom_info), 2, self)
                domain_info_table.setHorizontalHeaderLabels(["Type", "Information"])

                for i, (key, value) in enumerate(dom_info.items()):
                    domain_info_table.setItem(i, 0, QTableWidgetItem(key))
                    domain_info_table.setItem(i, 1, QTableWidgetItem(str(value)))

                domain_info_table.horizontalHeader().setStretchLastSection(True)
                domain_info_table.resizeColumnsToContents()  # Make sure table fits
                domain_info_container.addWidget(domain_info_table)
            else:
                raise ValueError("Domain information must be a dictionary.")

        except Exception as e:
            print(f"Error fetching domain info: {e}")  # Debugging output
            error_msg = QLabel(f"Failed to fetch domain information: {str(e)}", self)
            domain_info_container.addWidget(error_msg)

        layout.addLayout(domain_info_container)

    def display_subdomains(self, layout):
        """Fetch and display subdomains in a list."""
        subdomain_container = QVBoxLayout()
        subdomain_label = QLabel("Subdomains", self)
        subdomain_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subdomain_label.setStyleSheet("font-size: 18px; font-weight: bold; color: rgb(215, 38, 61);")
        subdomain_container.addWidget(subdomain_label)

        try:
            # Use DomainInfo to fetch subdomains
            domain_info = DomainInfo(self.url)  # Ensure self.url is correctly passed
            subdomains = domain_info.subdom()  # Use subdom() method to fetch subdomains

            if isinstance(subdomains, set) and subdomains:  # Check for non-empty set
                subdomain_list = QListWidget(self)
                subdomain_list.addItems(list(subdomains))  # Convert set to list for QListWidget
                subdomain_container.addWidget(subdomain_list)
            else:
                raise ValueError("Subdomains must be a non-empty set.")

        except Exception as e:
            print(f"Error fetching subdomains: {e}")  # Debugging output
            error_msg = QLabel(f"Failed to fetch subdomains: {str(e)}", self)
            subdomain_container.addWidget(error_msg)

        layout.addLayout(subdomain_container)
