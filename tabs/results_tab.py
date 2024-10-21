from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QListWidget
from PyQt6.QtCore import Qt
from modules.domain_info import DomainInfo  # Adjust this import based on your project structure


class ResultsTab(QWidget):
    def __init__(self, url, main_window):
        super().__init__()
        self.url = url
        self.main_window = main_window
        self.init_results_tab()

    def init_results_tab(self):
        layout = QVBoxLayout()

        # Display domain information and subdomains
        self.display_domain_info(layout)
        self.display_subdomains(layout)

        self.setLayout(layout)

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

            print(f"Type of dom_info: {type(dom_info)}")  # Debugging
            print(f"Content of dom_info: {dom_info}")  # Debugging

            if isinstance(dom_info, dict) and "Error" in dom_info:
                # Handle error case
                error_msg = QLabel(f"Failed to fetch domain information: {dom_info['Error']}", self)
                domain_info_container.addWidget(error_msg)
                return  # Exit early if there's an error
            else:
                print(f"Unexpected type for dom_info: {type(dom_info)}")

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
                subdomain_list.itemClicked.connect(self.open_subdomain_tab)  # Connect item click to method
                subdomain_container.addWidget(subdomain_list)
            else:
                raise ValueError("Subdomains must be a non-empty set.")

        except Exception as e:
            print(f"Error fetching subdomains: {e}")  # Debugging output
            error_msg = QLabel(f"Failed to fetch subdomains: {str(e)}", self)
            subdomain_container.addWidget(error_msg)

        layout.addLayout(subdomain_container)

    def open_subdomain_tab(self, item):
        """Handle clicking on a subdomain to perform a scan."""
        subdomain = item.text()
        self.full_scan_for_subdomain(subdomain)

    def full_scan_for_subdomain(self, subdomain):
        """Perform a full scan for the provided subdomain."""
        # Implement the logic for scanning the subdomain.
        print(f"Scanning subdomain: {subdomain}")  # Add functionality as needed
