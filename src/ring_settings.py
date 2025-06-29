import math
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox, QFrame
)
from PySide6.QtCore import Qt


class RingSettings(QWidget):
    def __init__(self, parent=None, index=0, on_delete=None, on_change=None, tr_func=None, on_move_up=None, on_move_down=None):
        super().__init__(parent)
        self.index = index
        self.on_delete = on_delete
        self.on_change = on_change
        self.on_move_up = on_move_up
        self.on_move_down = on_move_down
        self.tr = tr_func or (lambda x: x)
        
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        frame_layout = QVBoxLayout()
        frame_layout.setSpacing(8)
        frame_layout.setContentsMargins(0, 0, 0, 15)
        
        # Header with title and delete button
        header_layout = QHBoxLayout()
        self.title_label = QLabel(f"{self.tr('ring')} {self.index + 1}")
        font = self.title_label.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSizeF() * 1.5)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: #ffffff; margin: 0px; padding: 0px; border: none; background: transparent; font-size: 18px; font-weight: bold;")
        self.title_label.setContentsMargins(0, 0, 0, 0)
        
        # Move up button
        move_up_button = QPushButton("↑")
        move_up_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 2px 4px;
                margin: 0px;
            }
            QPushButton:hover {
                color: #cccccc;
            }
            QPushButton:pressed {
                color: #999999;
            }
        """)
        move_up_button.clicked.connect(self.request_move_up)
        
        # Move down button
        move_down_button = QPushButton("↓")
        move_down_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 2px 4px;
                margin: 0px;
            }
            QPushButton:hover {
                color: #cccccc;
            }
            QPushButton:pressed {
                color: #999999;
            }
        """)
        move_down_button.clicked.connect(self.request_move_down)
        
        delete_button = QPushButton(self.tr('remove'))
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #f85149;
                text-decoration: underline;
                font-size: 12px;
                padding: 2px;
            }
            QPushButton:hover {
                color: #da3633;
            }
            QPushButton:pressed {
                color: #b62324;
            }
        """)
        delete_button.clicked.connect(self.request_delete)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(move_up_button)
        header_layout.addWidget(move_down_button)
        header_layout.addWidget(delete_button)
        frame_layout.addLayout(header_layout)
        
        # RPM settings
        rpm_layout = QHBoxLayout()
        rpm_layout.setSpacing(10)
        self.rpm_label = QLabel(self.tr('rpm_selection'))
        self.rpm_label.setStyleSheet("font-weight: bold; color: #ffffff; background-color: transparent; border: none; margin: 0px; padding: 0px;")
        self.rpm_label.setContentsMargins(0, 0, 0, 0)
        
        self.rpm_combo = QComboBox()
        self.rpm_combo.addItems(["16", "33⅓", "45", "78"])
        self.rpm_combo.setCurrentIndex(1)
        self.rpm_combo.currentIndexChanged.connect(self.settings_changed)
        
        rpm_layout.addWidget(self.rpm_label, 1)
        rpm_layout.addWidget(self.rpm_combo, 1)
        frame_layout.addLayout(rpm_layout)
        
        # Manual RPM input
        manual_layout = QHBoxLayout()
        manual_layout.setSpacing(10)
        self.rpm_manual_check = QCheckBox(self.tr('enter_rpm_manually'))
        self.rpm_manual_check.setStyleSheet("font-weight: 500; color: #cccccc; background-color: transparent; border: none;")
        self.rpm_manual_check.stateChanged.connect(self.toggle_rpm_input)
        self.rpm_manual_check.stateChanged.connect(self.settings_changed)
        
        self.rpm_input = QDoubleSpinBox()
        self.rpm_input.setRange(1, 100)
        self.rpm_input.setValue(33.33)
        self.rpm_input.setDecimals(2)
        self.rpm_input.setEnabled(False)
        self.rpm_input.valueChanged.connect(self.settings_changed)
        
        manual_layout.addWidget(self.rpm_manual_check, 1)
        manual_layout.addWidget(self.rpm_input, 1)
        frame_layout.addLayout(manual_layout)
        
        # Frequency (Hz)
        hz_layout = QHBoxLayout()
        hz_layout.setSpacing(10)
        self.hz_label = QLabel(self.tr('frequency_hz'))
        self.hz_label.setStyleSheet("font-weight: bold; color: #ffffff; background-color: transparent; border: none; margin: 0px; padding: 0px;")
        self.hz_label.setContentsMargins(0, 0, 0, 0)
        
        self.hz_combo = QComboBox()
        self.hz_combo.addItems(["50", "60"])
        self.hz_combo.currentIndexChanged.connect(self.settings_changed)
        
        hz_layout.addWidget(self.hz_label, 1)
        hz_layout.addWidget(self.hz_combo, 1)
        frame_layout.addLayout(hz_layout)
        
        # Ring depth
        depth_layout = QHBoxLayout()
        depth_layout.setSpacing(10)
        self.depth_label = QLabel(self.tr('ring_depth'))
        self.depth_label.setStyleSheet("font-weight: bold; color: #ffffff; background-color: transparent; border: none; margin: 0px; padding: 0px;")
        self.depth_label.setContentsMargins(0, 0, 0, 0)
        
        self.depth_input = QDoubleSpinBox()
        self.depth_input.setRange(1, 100)
        self.depth_input.setValue(8)
        self.depth_input.setDecimals(1)
        self.depth_input.valueChanged.connect(self.settings_changed)
        
        depth_layout.addWidget(self.depth_label, 1)
        depth_layout.addWidget(self.depth_input, 1)
        frame_layout.addLayout(depth_layout)
        
        # Single mode checkbox
        mode_layout = QHBoxLayout()
        mode_layout.setSpacing(10)
        self.mode_label = QLabel(self.tr('mode_options'))
        self.mode_label.setStyleSheet("font-weight: bold; color: #ffffff; background-color: transparent; border: none; margin: 0px; padding: 0px;")
        self.mode_label.setContentsMargins(0, 0, 0, 0)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([self.tr('single_ring'), self.tr('dual_rings')])
        self.mode_combo.setCurrentIndex(0)
        self.mode_combo.currentIndexChanged.connect(self.settings_changed)
        
        mode_layout.addWidget(self.mode_label, 1)
        mode_layout.addWidget(self.mode_combo, 1)
        frame_layout.addLayout(mode_layout)
        
        # Shape type
        shape_layout = QHBoxLayout()
        shape_layout.setSpacing(10)
        self.shape_label = QLabel(self.tr('shape_type'))
        self.shape_label.setStyleSheet("font-weight: bold; color: #ffffff; background-color: transparent; border: none; margin: 0px; padding: 0px;")
        self.shape_label.setContentsMargins(0, 0, 0, 0)
        
        self.shape_combo = QComboBox()
        self.shape_combo.addItems([self.tr('lines'), self.tr('dots')])
        self.shape_combo.setCurrentIndex(0)
        self.shape_combo.currentIndexChanged.connect(self.settings_changed)
        
        shape_layout.addWidget(self.shape_label, 1)
        shape_layout.addWidget(self.shape_combo, 1)
        frame_layout.addLayout(shape_layout)
        
        # Density type
        density_layout = QHBoxLayout()
        density_layout.setSpacing(10)
        self.density_label = QLabel(self.tr('density'))
        self.density_label.setStyleSheet("font-weight: bold; color: #ffffff; background-color: transparent; border: none; margin: 0px; padding: 0px;")
        self.density_label.setContentsMargins(0, 0, 0, 0)
        
        self.density_combo = QComboBox()
        self.density_combo.addItems([self.tr('double'), self.tr('normal')])
        self.density_combo.setCurrentIndex(0)
        self.density_combo.currentIndexChanged.connect(self.settings_changed)
        
        density_layout.addWidget(self.density_label, 1)
        density_layout.addWidget(self.density_combo, 1)
        frame_layout.addLayout(density_layout)
        
        # Dot size
        dot_size_layout = QHBoxLayout()
        dot_size_layout.setSpacing(10)
        self.dot_size_label = QLabel(self.tr('dot_size'))
        self.dot_size_label.setStyleSheet("font-weight: bold; color: #ffffff; background-color: transparent; border: none; margin: 0px; padding: 0px;")
        self.dot_size_label.setContentsMargins(0, 0, 0, 0)
        
        self.dot_size_combo = QComboBox()
        self.dot_size_combo.addItems(["0.5x", "0.75x", "1x", "1.25x", "1.5x", "2x", "2.5x", "3x"])
        self.dot_size_combo.setCurrentIndex(2)
        self.dot_size_combo.currentIndexChanged.connect(self.settings_changed)
        
        dot_size_layout.addWidget(self.dot_size_label, 1)
        dot_size_layout.addWidget(self.dot_size_combo, 1)
        frame_layout.addLayout(dot_size_layout)
        
        # Information layout with title and content
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        info_layout.setContentsMargins(0, 8, 0, 0)
        
        self.info_title_label = QLabel(self.tr('ring_information'))
        self.info_title_label.setStyleSheet("""
            color: #ffffff;
            font-weight: bold;
            font-size: 13px;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        info_layout.addWidget(self.info_title_label)
        
        self.combined_info_label = QLabel()
        self.combined_info_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 12px; 
            font-weight: normal;
            line-height: 1.3;
            padding: 0px;
            background-color: transparent;
            border: none;
            margin: 0px;
        """)
        self.combined_info_label.setWordWrap(True)
        info_layout.addWidget(self.combined_info_label)
        
        frame_layout.addLayout(info_layout)
        
        # Add separator line with spacing
        frame_layout.addSpacing(20)
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Plain)
        self.separator.setStyleSheet("QFrame { background-color: #808080; border: none; height: 1px; }")
        self.separator.setFixedHeight(1)
        frame_layout.addWidget(self.separator)
        frame_layout.addSpacing(20)
        
        main_layout.addLayout(frame_layout)
        
        self.update_segments_info()
    
    def toggle_rpm_input(self, state):
        is_checked = state == Qt.CheckState.Checked.value
        self.rpm_input.setEnabled(is_checked)
        self.rpm_combo.setEnabled(not is_checked)
        self.update_segments_info()
    
    def get_rpm_value(self):
        if self.rpm_manual_check.isChecked():
            return self.rpm_input.value()
        else:
            rpm_text = self.rpm_combo.currentText()
            if rpm_text == "33⅓":
                return 33.33
            else:
                return float(rpm_text)
    
    def get_hz_value(self):
        return float(self.hz_combo.currentText())
    
    def get_depth_value(self):
        return self.depth_input.value()
    
    def lines_to_rpm(self, num_lines, frequency):
        density_factor = 2 if self.density_combo.currentIndex() == 0 else 1
        rpm = (60 * frequency * density_factor) / num_lines
        return round(rpm, 3)
    
    def calculate_segments_and_line_width(self, radius):
        rpm = self.get_rpm_value()
        hz = self.get_hz_value()
        
        density_factor = 2 if self.density_combo.currentIndex() == 0 else 1
        num_lines_exact = (60 * hz) / rpm * density_factor
        
        num_lines_floor = math.floor(num_lines_exact)
        num_lines_floor_rpm = self.lines_to_rpm(num_lines_floor, hz)
        num_lines_ceil = math.ceil(num_lines_exact)
        num_lines_ceil_rpm = self.lines_to_rpm(num_lines_ceil, hz)
        
        num_lines_rpm = 0
        
        if num_lines_floor == num_lines_ceil or self.mode_combo.currentIndex() == 0:
            if (num_lines_floor == num_lines_ceil):
                num_lines = num_lines_floor
            else:
                num_lines = round(num_lines_exact)
            num_lines_rpm = self.lines_to_rpm(num_lines, hz)
        else:
            num_lines = 0
        
        segment_width = (2 * math.pi * radius) / max(num_lines, 1)
        line_width = segment_width / 2
        
        return (num_lines_exact, num_lines, num_lines_rpm, line_width, 
                num_lines_floor, num_lines_ceil, num_lines_floor_rpm, num_lines_ceil_rpm)
    
    def update_segments_info(self, radius=None):
        if radius is None:
            radius = 100
        
        (num_lines_exact, num_lines, num_lines_rpm, line_width,
         num_lines_floor, num_lines_ceil, num_lines_floor_rpm, num_lines_ceil_rpm) = self.calculate_segments_and_line_width(radius)
        
        if num_lines_floor == num_lines_ceil or self.mode_combo.currentIndex() == 0:
            segments_text = f"{self.tr('number_of_segments')}: {num_lines}"
            details_text = [
                f"{self.tr('ideal')}: {round(num_lines_exact, 3)} {self.tr('lines_text')}",
                f"{self.tr('created')}: {num_lines} ({num_lines_rpm} {self.tr('rpm_text')}) {self.tr('lines_text')}",
            ]
        else:
            segments_text = f"{self.tr('number_of_segments')}: {num_lines_floor}/{num_lines_ceil}"
            details_text = [
                f"{self.tr('ideal')}: {round(num_lines_exact, 3)} {self.tr('lines_text')}",
                f"{self.tr('inner')}: {num_lines_ceil_rpm} {self.tr('rpm_text')} ({num_lines_ceil} {self.tr('lines_text')})",
                f"{self.tr('outer')}: {num_lines_floor_rpm} {self.tr('rpm_text')} ({num_lines_floor} {self.tr('lines_text')})",
            ]
        
        combined_text = [
            segments_text,
            f"{self.tr('line_width')}: {line_width:.2f} mm",
            "\n".join(details_text)
        ]
        
        self.combined_info_label.setText("\n".join(combined_text))
    
    def settings_changed(self):
        self.update_segments_info()
        if self.on_change:
            self.on_change()
    
    def request_delete(self):
        if self.on_delete:
            self.on_delete(self.index)
    
    def request_move_up(self):
        if self.on_move_up:
            self.on_move_up(self.index)
    
    def request_move_down(self):
        if self.on_move_down:
            self.on_move_down(self.index)
    
    def update_language(self, language):
        self.title_label.setText(f"{self.tr('ring')} {self.index + 1}")
        
        self.rpm_label.setText(self.tr('rpm_selection'))
        self.hz_label.setText(self.tr('frequency_hz'))
        self.depth_label.setText(self.tr('ring_depth'))
        self.mode_label.setText(self.tr('mode_options'))
        self.shape_label.setText(self.tr('shape_type'))
        self.density_label.setText(self.tr('density'))
        self.dot_size_label.setText(self.tr('dot_size'))
        self.info_title_label.setText(self.tr('ring_information'))
        
        self.rpm_manual_check.setText(self.tr('enter_rpm_manually'))
        
        current_mode = self.mode_combo.currentIndex()
        current_shape = self.shape_combo.currentIndex()
        current_density = self.density_combo.currentIndex()
        
        self.mode_combo.blockSignals(True)
        self.mode_combo.clear()
        self.mode_combo.addItems([self.tr('single_ring'), self.tr('dual_rings')])
        self.mode_combo.setCurrentIndex(current_mode)
        self.mode_combo.currentIndexChanged.connect(self.settings_changed)
        self.mode_combo.blockSignals(False)
        
        self.shape_combo.blockSignals(True)
        self.shape_combo.clear()
        self.shape_combo.addItems([self.tr('lines'), self.tr('dots')])
        self.shape_combo.setCurrentIndex(current_shape)
        self.shape_combo.currentIndexChanged.connect(self.settings_changed)
        self.shape_combo.blockSignals(False)
        
        self.density_combo.blockSignals(True)
        self.density_combo.clear()
        self.density_combo.addItems([self.tr('double'), self.tr('normal')])
        self.density_combo.setCurrentIndex(current_density)
        self.density_combo.currentIndexChanged.connect(self.settings_changed)
        self.density_combo.blockSignals(False)
        
        self.update_segments_info()
    
    def get_settings(self):
        return {
            'rpm': self.get_rpm_value(),
            'hz': self.get_hz_value(),
            'depth': self.get_depth_value(),
            'single_mode': self.mode_combo.currentIndex() == 0,
            'shape_type': 'lines' if self.shape_combo.currentIndex() == 0 else 'dots',
            'density': 'double' if self.density_combo.currentIndex() == 0 else 'normal',
            'dot_size': float(self.dot_size_combo.currentText().replace('x', ''))
        }