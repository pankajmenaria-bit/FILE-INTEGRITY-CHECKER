import sys
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class FileIntegrityChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.file_path = None
        self.stored_hash = None

    def initUI(self):
        self.setWindowTitle("File Integrity Checker")
        self.setGeometry(100, 100, 400, 250)

        # Set red background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#ff4d4d"))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # File selection button
        self.select_file_btn = QPushButton("📂 Select File", self)
        self.select_file_btn.clicked.connect(self.select_file)
        self.select_file_btn.setStyleSheet("""
            background-color: #e60000;
            color: white;
            font-size: 15px;
            border-radius: 5px;
            padding: 10px;
        """)
        layout.addWidget(self.select_file_btn)

        # Display selected file
        self.file_label = QLabel("📁 No file selected", self)
        self.file_label.setStyleSheet("""
            color: white;
            font-size: 13px;
        """)
        layout.addWidget(self.file_label)

        # Compute hash button
        self.compute_hash_btn = QPushButton("🔐 Compute Hash", self)
        self.compute_hash_btn.clicked.connect(self.compute_hash)
        self.compute_hash_btn.setEnabled(False)
        self.compute_hash_btn.setStyleSheet("""
            background-color: #cc0000;
            color: white;
            font-size: 15px;
            border-radius: 5px;
            padding: 10px;
        """)
        layout.addWidget(self.compute_hash_btn)

        # Check Integrity button
        self.check_integrity_btn = QPushButton("🛡 Check Integrity", self)
        self.check_integrity_btn.clicked.connect(self.check_integrity)
        self.check_integrity_btn.setEnabled(False)
        self.check_integrity_btn.setStyleSheet("""
            background-color: #990000;
            color: white;
            font-size: 15px;
            border-radius: 5px;
            padding: 10px;
        """)
        layout.addWidget(self.check_integrity_btn)

        self.setLayout(layout)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"📁 File: {file_path}")
            self.compute_hash_btn.setEnabled(True)

    def compute_hash(self):
        if not self.file_path:
            return

        self.stored_hash = self.calculate_hash(self.file_path)
        if self.stored_hash:
            QMessageBox.information(
                self,
                "✅ Hash Computed",
                f"SHA-256 Hash:\n{self.stored_hash}"
            )
            self.check_integrity_btn.setEnabled(True)

    def check_integrity(self):
        if not self.file_path or not self.stored_hash:
            return

        current_hash = self.calculate_hash(self.file_path)
        if current_hash == self.stored_hash:
            QMessageBox.information(
                self,
                "✅ Integrity Check",
                "🎉 File is intact. No changes detected."
            )
        else:
            QMessageBox.warning(
                self,
                "⚠️ Integrity Check",
                "❌ Warning! File has been modified!"
            )

    @staticmethod
    def calculate_hash(file_path):
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            QMessageBox.critical(None, "❌ Error", "File not found!")
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileIntegrityChecker()
    window.show()
    sys.exit(app.exec_())
