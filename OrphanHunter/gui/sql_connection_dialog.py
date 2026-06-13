"""SQL connection configuration dialog."""
from pathlib import Path
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QSpinBox, QPushButton, QLabel, QMessageBox,
    QGroupBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from OrphanHunter.analyzer.live_db_connector import ConfigParser


class SQLConnectionDialog(QDialog):
    """Dialog for configuring SQL database connection."""
    
    def __init__(self, config, parent=None):
        """Initialize SQL connection dialog.
        
        Args:
            config: Config object
            parent: Parent widget
        """
        super().__init__(parent)
        self.config = config
        self.credentials = {
            'host': '',
            'user': '',
            'password': '',
            'database': '',
            'port': 3306
        }
        
        self.init_ui()
        self.load_existing_credentials()
    
    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("Configure SQL Connection")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Info section
        info_label = QLabel(
            "Configure your MySQL/MariaDB connection credentials.\n"
            "These will be saved and used for all database operations."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Auto-detect section
        detect_group = QGroupBox("Auto-Detect from config.php")
        detect_layout = QVBoxLayout()
        
        detect_btn_layout = QHBoxLayout()
        self.detect_btn = QPushButton("Auto-Detect Credentials")
        self.detect_btn.clicked.connect(self.auto_detect_credentials)
        detect_btn_layout.addWidget(self.detect_btn)
        detect_btn_layout.addStretch()
        detect_layout.addLayout(detect_btn_layout)
        
        self.detect_status = QLabel("")
        self.detect_status.setWordWrap(True)
        detect_layout.addWidget(self.detect_status)
        
        detect_group.setLayout(detect_layout)
        layout.addWidget(detect_group)
        
        # Credentials form
        cred_group = QGroupBox("Database Credentials")
        form_layout = QFormLayout()
        
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("localhost or IP address")
        form_layout.addRow("Host:", self.host_input)
        
        self.port_input = QSpinBox()
        self.port_input.setMinimum(1)
        self.port_input.setMaximum(65535)
        self.port_input.setValue(3306)
        form_layout.addRow("Port:", self.port_input)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Database username")
        form_layout.addRow("Username:", self.user_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Database password (optional)")
        form_layout.addRow("Password:", self.password_input)
        
        self.database_input = QLineEdit()
        self.database_input.setPlaceholderText("Database name")
        form_layout.addRow("Database:", self.database_input)
        
        cred_group.setLayout(form_layout)
        layout.addWidget(cred_group)
        
        # Security warning
        warning = QLabel(
            "⚠️ Note: Credentials are stored in plaintext in the config file. "
            "Ensure your config file has appropriate permissions."
        )
        warning.setWordWrap(True)
        warning_font = QFont()
        warning_font.setPointSize(8)
        warning.setFont(warning_font)
        warning.setStyleSheet("color: #ff6600;")
        layout.addWidget(warning)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.test_btn = QPushButton("Test Connection")
        self.test_btn.clicked.connect(self.test_connection)
        button_layout.addWidget(self.test_btn)
        
        button_layout.addStretch()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_credentials)
        button_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_existing_credentials(self):
        """Load existing credentials from config."""
        sql_creds = self.config.get('sql_credentials', {})
        
        if sql_creds:
            self.host_input.setText(sql_creds.get('host', ''))
            self.port_input.setValue(sql_creds.get('port', 3306))
            self.user_input.setText(sql_creds.get('user', ''))
            self.password_input.setText(sql_creds.get('password', ''))
            self.database_input.setText(sql_creds.get('database', ''))
    
    def auto_detect_credentials(self):
        """Auto-detect credentials from config.php."""
        config_php_path = self.config.get('config_php_path', '')
        
        if not config_php_path or not Path(config_php_path).exists():
            self.detect_status.setText(
                "❌ No config.php path set. Please configure it in the Configuration tab first."
            )
            self.detect_status.setStyleSheet("color: red;")
            return
        
        try:
            parser = ConfigParser()
            credentials = parser.parse_config(Path(config_php_path))
            valid, message = parser.validate_credentials()
            
            if valid:
                # Fill in the form
                if credentials['host']:
                    self.host_input.setText(credentials['host'])
                if credentials['user']:
                    self.user_input.setText(credentials['user'])
                if credentials['password']:
                    self.password_input.setText(credentials['password'])
                if credentials['database']:
                    self.database_input.setText(credentials['database'])
                if credentials['port']:
                    self.port_input.setValue(credentials['port'])
                
                self.detect_status.setText(
                    f"✓ Credentials detected from {Path(config_php_path).name}. "
                    "Please review and test before saving."
                )
                self.detect_status.setStyleSheet("color: green;")
            else:
                self.detect_status.setText(f"❌ {message}")
                self.detect_status.setStyleSheet("color: red;")
        
        except Exception as e:
            self.detect_status.setText(f"❌ Error parsing config.php: {e}")
            self.detect_status.setStyleSheet("color: red;")
    
    def test_connection(self):
        """Test database connection with current credentials."""
        # Gather credentials from form
        test_creds = {
            'host': self.host_input.text().strip(),
            'port': self.port_input.value(),
            'user': self.user_input.text().strip(),
            'password': self.password_input.text(),
            'database': self.database_input.text().strip()
        }
        
        # Validate
        if not test_creds['host']:
            QMessageBox.warning(self, "Missing Host", "Please enter a database host.")
            return
        if not test_creds['user']:
            QMessageBox.warning(self, "Missing Username", "Please enter a database username.")
            return
        if not test_creds['database']:
            QMessageBox.warning(self, "Missing Database", "Please enter a database name.")
            return
        
        # Try to connect
        try:
            from OrphanHunter.analyzer.live_db_connector import LiveDatabaseConnector
            
            connector = LiveDatabaseConnector()
            success, message = connector.connect(test_creds)
            
            if success:
                # Get table count
                tables = connector.get_tables()
                connector.disconnect()
                
                QMessageBox.information(
                    self, 
                    "Connection Successful", 
                    f"✓ Connected successfully!\n\n"
                    f"Database: {test_creds['database']}\n"
                    f"Tables found: {len(tables)}\n\n"
                    f"You can now save these credentials."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Connection Failed",
                    f"Failed to connect to database:\n\n{message}"
                )
        
        except ImportError:
            QMessageBox.warning(
                self,
                "Missing Package",
                "mysql-connector-python is not installed.\n\n"
                "Install it with: pip install mysql-connector-python"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Connection Error",
                f"An error occurred:\n\n{e}"
            )
    
    def save_credentials(self):
        """Save credentials to config."""
        # Gather credentials
        creds = {
            'host': self.host_input.text().strip(),
            'port': self.port_input.value(),
            'user': self.user_input.text().strip(),
            'password': self.password_input.text(),
            'database': self.database_input.text().strip()
        }
        
        # Validate
        if not creds['host'] or not creds['user'] or not creds['database']:
            QMessageBox.warning(
                self,
                "Incomplete Credentials",
                "Please fill in at least Host, Username, and Database fields."
            )
            return
        
        # Save to config
        self.config.set('sql_credentials', creds)
        self.config.save()
        
        QMessageBox.information(
            self,
            "Credentials Saved",
            "SQL credentials have been saved successfully!\n\n"
            "They will be used for all database connections."
        )
        
        self.accept()
    
    def get_credentials(self) -> dict:
        """Get the configured credentials.
        
        Returns:
            Dictionary with credentials
        """
        return {
            'host': self.host_input.text().strip(),
            'port': self.port_input.value(),
            'user': self.user_input.text().strip(),
            'password': self.password_input.text(),
            'database': self.database_input.text().strip()
        }


