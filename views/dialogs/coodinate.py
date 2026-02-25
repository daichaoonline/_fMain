import json
import random
from pathlib import Path
import sys
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QSpinBox, QDoubleSpinBox,
    QDialog, QPushButton, QListWidget,
    QApplication, QGroupBox, QMessageBox)

class Coordinate(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cities = {
            "New York": (40.7128, -74.0060),
            "Los Angeles": (34.0522, -118.2437),
            "Chicago": (41.8781, -87.6298),
            "Houston": (29.7604, -95.3698),
            "Seattle": (47.6062, -122.3321),
            "Phoenix": (33.4484, -112.0740),
            "Denver": (39.7392, -104.9903),
            "Washington DC": (38.9072, -77.0369),
            "San Francisco": (37.7749, -122.4194),
            "Dallas": (32.7767, -96.7970),
            "Miami": (25.7617, -80.1918),
            "New Jersey": (40.0583, -74.4057),
            "Salt Lake City": (40.7608, -111.8910),
            "Tampa": (27.9506, -82.4572),
            "Atlanta": (33.7490, -84.3880),
            "Albuquerque": (35.0844, -106.6504),
            "Boston": (42.3601, -71.0589),
            "Little Rock": (34.7465, -92.2896),
            "Louisville": (38.2527, -85.7585),
            "Santa Monica": (34.0195, -118.4912),
            "Las Vegas": (36.1699, -115.1398),
            "Portland": (45.5200, -122.6829),
            "San Diego": (32.7157, -117.1611)
        }

        self.setWindowTitle("Coordinate Generator")
        self.setFixedSize(600, 300)

        self.data_folder = Path("./assets/list_cities")
        self.data_folder.mkdir(parents=True, exist_ok=True)

        self.init_ui()
        self.load_coordinates_for_city(self.cmbCity.currentText())

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        left_panel = QVBoxLayout()
        city_group = QGroupBox("City Selection")
        city_layout = QVBoxLayout()

        self.cmbCity = QComboBox()
        self.cmbCity.addItems(self.cities.keys())
        self.cmbCity.currentTextChanged.connect(self.on_city_changed)
        city_layout.addWidget(QLabel("Select City:"))
        city_layout.addWidget(self.cmbCity)

        self.lblCity = QLabel("")
        self.lblCity.setStyleSheet("font-weight: bold;")
        city_layout.addWidget(QLabel("Base Coordinates:"))
        city_layout.addWidget(self.lblCity)

        city_group.setLayout(city_layout)
        left_panel.addWidget(city_group)

        settings_group = QGroupBox("Generation Settings")
        settings_layout = QGridLayout()

        self.sbPoints = QSpinBox()
        self.sbPoints.setRange(1, 100)
        self.sbPoints.setValue(10)
        settings_layout.addWidget(QLabel("Number of Points:"), 0, 0)
        settings_layout.addWidget(self.sbPoints, 0, 1)

        self.sbOffset = QDoubleSpinBox()
        self.sbOffset.setRange(0.001, 1.0)
        self.sbOffset.setValue(0.01)
        self.sbOffset.setSingleStep(0.001)
        settings_layout.addWidget(QLabel("Max Offset (Degrees):"), 1, 0)
        settings_layout.addWidget(self.sbOffset, 1, 1)

        self.btnGenerate = QPushButton("Generate Coordinates")
        self.btnGenerate.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        self.btnGenerate.clicked.connect(self.generate_coordinates)
        settings_layout.addWidget(self.btnGenerate, 2, 0, 1, 2)

        settings_group.setLayout(settings_layout)
        left_panel.addWidget(settings_group)
        left_panel.addStretch()

        # Right panel (results)
        right_panel = QVBoxLayout()
        results_group = QGroupBox("Generated Coordinates")
        results_layout = QVBoxLayout()

        self.listCoord = QListWidget()
        self.listCoord.setAlternatingRowColors(True)
        results_layout.addWidget(self.listCoord)

        button_layout = QHBoxLayout()
        self.btnCopy = QPushButton("Copy")
        self.btnCopy.setStyleSheet("QPushButton { background-color: #555555; color: white; }")
        self.btnCopy.clicked.connect(self.copy_all_coordinates)
        button_layout.addWidget(self.btnCopy)
        results_layout.addLayout(button_layout)

        results_group.setLayout(results_layout)
        right_panel.addWidget(results_group)

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)

        self.update_lblCity(self.cmbCity.currentText())

    def on_city_changed(self, city):
        self.load_coordinates_for_city(city)
        self.update_lblCity(city)

    def update_lblCity(self, city):
        lat, lon = self.cities.get(city, (None, None))
        if lat is not None:
            self.lblCity.setText(f"{lat:.6f}, {lon:.6f}")
        else:
            self.lblCity.setText("Unknown")

    def get_coords_filepath(self, city):
        safe_city = city.replace(" ", "_").lower()
        return self.data_folder / f"{safe_city}_coordinates.json"

    def load_coordinates_for_city(self, city):
        path = self.get_coords_filepath(city)
        coords = []
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    coords = data.get("coordinates", [])
            except Exception:
                coords = []

        self.listCoord.clear()
        for c in coords:
            lat = c.get("lat", 0)
            lon = c.get("lon", 0)
            self.listCoord.addItem(f"{lat:.6f}, {lon:.6f}")

    def auto_save_coordinates(self):
        city = self.cmbCity.currentText()
        coords = []
        for i in range(self.listCoord.count()):
            lat_str, lon_str = self.listCoord.item(i).text().split(", ")
            coords.append({"lat": float(lat_str), "lon": float(lon_str)})
        path = self.get_coords_filepath(city)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"coordinates": coords}, f, indent=4)
        except Exception:
            pass

    def generate_coordinates(self):
        city = self.cmbCity.currentText()
        center_lat, center_lon = self.cities[city]
        num_points = self.sbPoints.value()
        max_offset = self.sbOffset.value()

        coordinates = self.generate_nearby_coordinates(center_lat, center_lon, num_points, max_offset)
        self.listCoord.clear()
        for lat, lon in coordinates:
            self.listCoord.addItem(f"{lat:.6f}, {lon:.6f}")
        self.auto_save_coordinates()

    def generate_nearby_coordinates(self, center_lat, center_lon, num_points=10, max_offset=0.01):
        coordinates = []
        for i in range(num_points):
            lat_offset = random.uniform(-max_offset, max_offset)
            lon_offset = random.uniform(-max_offset, max_offset)
            coordinates.append((center_lat + lat_offset, center_lon + lon_offset))
        return coordinates

    def copy_all_coordinates(self):
        reply = QMessageBox.question(self, "Confirm Copy", "Do you want to copy all generated coordinates?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            coords = [self.listCoord.item(i).text() for i in range(self.listCoord.count())]
            text_to_copy = " | ".join(coords)
            QApplication.clipboard().setText(text_to_copy)
            self.accept()
            return text_to_copy
        else:
            return ""