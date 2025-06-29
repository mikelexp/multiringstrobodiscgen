import sys
import os
import tempfile
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QSpinBox, QDoubleSpinBox, QFileDialog, QComboBox, 
    QMessageBox, QTabWidget, QApplication, QInputDialog, QListWidget, 
    QListWidgetItem, QTextEdit
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QResizeEvent, QGuiApplication

# For PDF export (only import when needed to avoid dependency issues)
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    from reportlab.lib.pagesizes import A4, LETTER, LEGAL, A3
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

from .config_manager import ConfigManager
from .translations import TRANSLATIONS
from .ring_settings import RingSettings
from .svg_generator import SVGGenerator


# Constants for sizes
PREVIEW_PANEL_MARGIN_WIDTH = 20
PREVIEW_PANEL_MARGIN_HEIGHT = 20


class StroboscopeMultiRingsGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.config_manager = ConfigManager()
        self.current_language = self.config_manager.get('language', 'en')
        
        self.setWindowTitle(self.tr('app_title'))
        self.setMinimumSize(1000, 700)
        self.svg_content = ""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_svg_file = None
        
        self.ring_widgets = []
        self.svg_generator = SVGGenerator()
        
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.generate_disc)
        
        self.apply_font_scaling()
        self.setup_ui()
        self.add_ring()
        self.load_presets_list()
        
    def tr(self, key):
        return TRANSLATIONS.get(self.current_language, TRANSLATIONS['en']).get(key, key)
    
    def apply_font_scaling(self):
        self.scale_factor = 1.15
        
        font = QApplication.font()
        font_size = font.pointSize()
        if font_size > 0:
            font.setPointSize(int(font_size * self.scale_factor))
            QApplication.setFont(font)
    
    def is_dark_theme(self):
        palette = QGuiApplication.palette()
        background_color = palette.color(palette.ColorRole.Window)
        brightness = (background_color.red() * 299 + background_color.green() * 587 + background_color.blue() * 114) / 1000
        return brightness < 128
    
    def apply_font_to_widget(self, widget, size_increase=0):
        font = widget.font()
        current_size = font.pointSize()
        if current_size > 0 and size_increase > 0:
            font.setPointSize(current_size + size_increase)
            widget.setFont(font)
    
    def schedule_preview_update(self):
        self.update_timer.start(300)
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        central_widget.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QPushButton {
                background-color: #569cd6;
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
            }
            QLabel {
                color: #ffffff;
                font-size: 13px;
            }
            QTabWidget {
                border: none;
                background-color: transparent;
            }
            QTabWidget::pane {
                border: 1px solid #404040;
                border-radius: 8px;
                background-color: rgba(40, 40, 40, 0.95);
                margin-top: -1px;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 12px 20px;
                margin-right: 2px;
                font-weight: 600;
                color: #cccccc;
            }
            QTabBar::tab:selected {
                background-color: #569cd6;
                color: #ffffff;
                border-color: #569cd6;
            }
            QTabBar::tab:hover:!selected {
                background-color: #404040;
                color: #ffffff;
            }
        """)
        
        main_layout = QHBoxLayout(central_widget)
        
        controls_panel = QWidget()
        controls_panel.setStyleSheet("QWidget { background-color: #252525; }")
        controls_layout = QVBoxLayout(controls_panel)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tab_widget = QTabWidget()
        controls_layout.addWidget(self.tab_widget)
        
        # TAB 1: Rings Configuration
        rings_tab = QWidget()
        rings_tab_layout = QVBoxLayout(rings_tab)
        rings_tab_layout.setContentsMargins(15, 15, 15, 15)
        rings_tab_layout.setSpacing(10)
        
        self.add_ring_button = QPushButton(f"+ {self.tr('add_ring')}")
        self.apply_font_to_widget(self.add_ring_button, 1)
        self.add_ring_button.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                border: 2px solid #238636;
                padding: 6px 14px;
                font-size: 14px;
                color: #ffffff;
                min-height: 27px;
                max-height: 27px;
            }
            QPushButton:hover {
                background-color: #2ea043;
                border-color: #2ea043;
            }
            QPushButton:pressed {
                background-color: #1a7f37;
                border-color: #1a7f37;
            }
        """)
        self.add_ring_button.clicked.connect(self.add_ring)
        rings_tab_layout.addWidget(self.add_ring_button)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.rings_container = QWidget()
        self.rings_layout = QVBoxLayout(self.rings_container)
        self.rings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.rings_layout.setContentsMargins(5, 5, 15, 5)
        self.rings_layout.setSpacing(8)
        
        scroll_area.setWidget(self.rings_container)
        rings_tab_layout.addWidget(scroll_area, 1)
        
        self.tab_widget.addTab(rings_tab, self.tr('rings_tab'))
        
        # TAB 2: Config
        params_tab = QWidget()
        params_layout = QVBoxLayout(params_tab)
        params_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        params_layout.setSpacing(15)
        params_layout.setContentsMargins(20, 20, 20, 20)
        
        # Language selector
        language_layout = QHBoxLayout()
        self.language_label = QLabel(self.tr('language'))
        self.language_combo = QComboBox()
        self.language_combo.addItems([self.tr('english'), self.tr('spanish')])
        self.language_combo.setCurrentIndex(0 if self.current_language == 'en' else 1)
        self.language_combo.currentIndexChanged.connect(self.change_language)
        language_layout.addWidget(self.language_label)
        language_layout.addWidget(self.language_combo)
        params_layout.addLayout(language_layout)
        
        self.measurements_title = QLabel(self.tr('measurements_mm'))
        self.measurements_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin: 0px; padding: 0px; border: none; background: transparent;")
        self.measurements_title.setContentsMargins(0, 0, 0, 0)
        params_layout.addWidget(self.measurements_title)
        
        # Diameter
        diameter_layout = QHBoxLayout()
        self.diameter_label = QLabel(self.tr('total_diameter'))
        self.diameter_input = QSpinBox()
        self.diameter_input.setRange(10, 320)
        self.diameter_input.setValue(200)
        self.diameter_input.valueChanged.connect(self.schedule_preview_update)
        diameter_layout.addWidget(self.diameter_label)
        diameter_layout.addWidget(self.diameter_input)
        params_layout.addLayout(diameter_layout)
        
        # Spindle diameter
        spindle_diameter_layout = QHBoxLayout()
        self.spindle_diameter_label = QLabel(self.tr('spindle_diameter'))
        self.spindle_diameter_input = QDoubleSpinBox()
        self.spindle_diameter_input.setRange(0, 20)
        self.spindle_diameter_input.setValue(7)
        self.spindle_diameter_input.setDecimals(2)
        self.spindle_diameter_input.setSingleStep(0.1)
        self.spindle_diameter_input.valueChanged.connect(self.schedule_preview_update)
        spindle_diameter_layout.addWidget(self.spindle_diameter_label)
        spindle_diameter_layout.addWidget(self.spindle_diameter_input)
        params_layout.addLayout(spindle_diameter_layout)
        
        # Outer circle width
        outer_circle_width_layout = QHBoxLayout()
        self.outer_circle_width_label = QLabel(self.tr('outer_circle_width'))
        self.outer_circle_width_input = QDoubleSpinBox()
        self.outer_circle_width_input.setRange(0, 10)
        self.outer_circle_width_input.setValue(1)
        self.outer_circle_width_input.setSingleStep(0.1)
        self.outer_circle_width_input.setDecimals(2)
        self.outer_circle_width_input.valueChanged.connect(self.schedule_preview_update)
        outer_circle_width_layout.addWidget(self.outer_circle_width_label)
        outer_circle_width_layout.addWidget(self.outer_circle_width_input)
        params_layout.addLayout(outer_circle_width_layout)
        
        # Ring separation
        ring_separation_layout = QHBoxLayout()
        self.ring_separation_label = QLabel(self.tr('ring_separation'))
        self.ring_separation_input = QDoubleSpinBox()
        self.ring_separation_input.setRange(0, 10)
        self.ring_separation_input.setValue(1)
        self.ring_separation_input.setDecimals(2)
        self.ring_separation_input.valueChanged.connect(self.schedule_preview_update)
        ring_separation_layout.addWidget(self.ring_separation_label)
        ring_separation_layout.addWidget(self.ring_separation_input)
        params_layout.addLayout(ring_separation_layout)
        
        # Text positioning section
        self.disc_text_title = QLabel(self.tr('disc_text'))
        self.disc_text_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin: 15px 0px 10px 0px; padding: 0px; border: none; background: transparent;")
        self.disc_text_title.setContentsMargins(0, 0, 0, 0)
        params_layout.addWidget(self.disc_text_title)
        
        # Top text
        top_text_layout = QVBoxLayout()
        self.top_text_label = QLabel(self.tr('text_top'))
        self.top_text_input = QTextEdit()
        self.top_text_input.setMaximumHeight(120)  # Double height (60 -> 120)
        self.top_text_input.textChanged.connect(self.schedule_preview_update)
        self.top_text_input.setTabChangesFocus(True)  # Tab moves to next widget instead of inserting tab
        top_text_layout.addWidget(self.top_text_label)
        top_text_layout.addWidget(self.top_text_input)
        params_layout.addLayout(top_text_layout)
        
        # Bottom text
        bottom_text_layout = QVBoxLayout()
        self.bottom_text_label = QLabel(self.tr('text_bottom'))
        self.bottom_text_input = QTextEdit()
        self.bottom_text_input.setMaximumHeight(120)  # Double height (60 -> 120)
        self.bottom_text_input.textChanged.connect(self.schedule_preview_update)
        self.bottom_text_input.setTabChangesFocus(True)  # Tab moves to next widget instead of inserting tab
        bottom_text_layout.addWidget(self.bottom_text_label)
        bottom_text_layout.addWidget(self.bottom_text_input)
        params_layout.addLayout(bottom_text_layout)
        
        params_layout.addStretch()
        
        self.tab_widget.addTab(params_tab, self.tr('config_tab'))
        
        # TAB 3: Export Options
        export_tab = QWidget()
        export_tab_layout = QVBoxLayout(export_tab)
        export_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        export_tab_layout.setSpacing(15)
        export_tab_layout.setContentsMargins(20, 20, 20, 20)
        
        # Export format
        export_format_layout = QHBoxLayout()
        self.export_format_label = QLabel(self.tr('export_format'))
        self.format_combo = QComboBox()
        if PDF_AVAILABLE:
            self.format_combo.addItems(["SVG", "PDF"])
        else:
            self.format_combo.addItems(["SVG"])
        self.format_combo.setCurrentIndex(0)
        
        export_format_layout.addWidget(self.export_format_label)
        export_format_layout.addWidget(self.format_combo)
        export_tab_layout.addLayout(export_format_layout)
        
        # Paper format selection (for PDF export)
        self.page_size_layout = QHBoxLayout()
        self.page_size_label = QLabel(self.tr('page_size'))
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4", "Letter", "Legal", "A3"])
        self.page_size_combo.setCurrentIndex(0)
        self.page_size_combo.setEnabled(False)
        self.page_size_combo.setStyleSheet("QComboBox:disabled { color: gray; }")
        
        self.page_size_layout.addWidget(self.page_size_label)
        self.page_size_layout.addWidget(self.page_size_combo)
        export_tab_layout.addLayout(self.page_size_layout)
        
        self.format_combo.currentTextChanged.connect(lambda text: self.page_size_combo.setEnabled(text == "PDF" and PDF_AVAILABLE))
        
        self.export_button = QPushButton(self.tr('export'))
        self.apply_font_to_widget(self.export_button, 1)
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #8957e5;
                border: 2px solid #8957e5;
                padding: 6px 14px;
                font-size: 14px;
                color: #ffffff;
                min-height: 27px;
                max-height: 27px;
            }
            QPushButton:hover {
                background-color: #a475f9;
                border-color: #a475f9;
            }
            QPushButton:pressed {
                background-color: #7c3aed;
                border-color: #7c3aed;
            }
        """)
        self.export_button.clicked.connect(self.export_file)
        self.export_button.setEnabled(False)
        export_tab_layout.addWidget(self.export_button)
        export_tab_layout.addStretch()
        self.tab_widget.addTab(export_tab, self.tr('export_tab'))
        
        # TAB 4: Presets
        presets_tab = QWidget()
        presets_tab_layout = QVBoxLayout(presets_tab)
        presets_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        presets_tab_layout.setSpacing(15)
        presets_tab_layout.setContentsMargins(20, 20, 20, 20)
        
        # Save as new preset button
        self.save_preset_button = QPushButton(self.tr('save_as_new_preset'))
        self.apply_font_to_widget(self.save_preset_button, 1)
        self.save_preset_button.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                border: 2px solid #238636;
                padding: 6px 14px;
                font-size: 14px;
                color: #ffffff;
                min-height: 27px;
                max-height: 27px;
            }
            QPushButton:hover {
                background-color: #2ea043;
                border-color: #2ea043;
            }
            QPushButton:pressed {
                background-color: #1a7f37;
                border-color: #1a7f37;
            }
        """)
        self.save_preset_button.clicked.connect(self.save_new_preset)
        presets_tab_layout.addWidget(self.save_preset_button)
        
        # Presets list
        self.presets_list = QListWidget()
        self.presets_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 4px;
                color: #ffffff;
                padding: 5px;
            }
            QListWidget::item {
                background-color: transparent;
                padding: 8px;
                border-bottom: 1px solid #404040;
            }
            QListWidget::item:selected {
                background-color: #569cd6;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
        """)
        presets_tab_layout.addWidget(self.presets_list, 1)
        
        self.tab_widget.addTab(presets_tab, self.tr('presets_tab'))
        
        self.tab_widget.setCurrentIndex(0)
        
        controls_panel.setFixedWidth(400)
        main_layout.addWidget(controls_panel)
        
        # Preview panel
        self.preview_panel = QWidget()
        self.preview_panel.setStyleSheet("background-color: white;")
        preview_layout = QVBoxLayout(self.preview_panel)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.svg_widget = QSvgWidget()
        self.svg_widget.setMinimumSize(QSize(300, 300))
        preview_layout.addWidget(self.svg_widget, 1, Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addWidget(self.preview_panel, 1)
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.adjust_svg_size()
    
    def adjust_svg_size(self):
        if hasattr(self, 'svg_widget') and hasattr(self, 'preview_panel'):
            available_width = self.preview_panel.width() - PREVIEW_PANEL_MARGIN_WIDTH
            available_height = self.preview_panel.height() - PREVIEW_PANEL_MARGIN_HEIGHT
            
            size = min(available_width, available_height)
            self.svg_widget.setFixedSize(QSize(size, size))
    
    def add_ring(self):
        index = len(self.ring_widgets)
        ring_widget = RingSettings(
            parent=self.rings_container,
            index=index,
            on_delete=self.delete_ring,
            on_change=self.schedule_preview_update,
            tr_func=self.tr,
            on_move_up=self.move_ring_up,
            on_move_down=self.move_ring_down
        )
        self.ring_widgets.append(ring_widget)
        self.rings_layout.addWidget(ring_widget)
        
        self.schedule_preview_update()
    
    def delete_ring(self, index):
        if len(self.ring_widgets) <= 1:
            QMessageBox.warning(self, self.tr('warning'), self.tr('at_least_one_ring'))
            return
            
        if index < len(self.ring_widgets):
            widget = self.ring_widgets.pop(index)
            self.rings_layout.removeWidget(widget)
            widget.deleteLater()
            
        self.update_ring_indices()
        self.schedule_preview_update()
    
    def move_ring_up(self, index):
        if index > 0 and index < len(self.ring_widgets):
            # Swap rings in the list
            self.ring_widgets[index], self.ring_widgets[index - 1] = self.ring_widgets[index - 1], self.ring_widgets[index]
            
            # Remove both widgets from layout
            self.rings_layout.removeWidget(self.ring_widgets[index])
            self.rings_layout.removeWidget(self.ring_widgets[index - 1])
            
            # Re-add them in new order
            self.rings_layout.insertWidget(index - 1, self.ring_widgets[index - 1])
            self.rings_layout.insertWidget(index, self.ring_widgets[index])
            
            # Update indices and titles
            self.update_ring_indices()
            self.schedule_preview_update()
    
    def move_ring_down(self, index):
        if index >= 0 and index < len(self.ring_widgets) - 1:
            # Swap rings in the list
            self.ring_widgets[index], self.ring_widgets[index + 1] = self.ring_widgets[index + 1], self.ring_widgets[index]
            
            # Remove both widgets from layout
            self.rings_layout.removeWidget(self.ring_widgets[index])
            self.rings_layout.removeWidget(self.ring_widgets[index + 1])
            
            # Re-add them in new order
            self.rings_layout.insertWidget(index, self.ring_widgets[index])
            self.rings_layout.insertWidget(index + 1, self.ring_widgets[index + 1])
            
            # Update indices and titles
            self.update_ring_indices()
            self.schedule_preview_update()
    
    def update_ring_indices(self):
        for i, widget in enumerate(self.ring_widgets):
            widget.index = i
            widget.title_label.setText(f"{widget.tr('ring')} {i + 1}")
    
    def generate_disc(self):
        if not self.ring_widgets:
            QMessageBox.warning(self, self.tr('warning'), self.tr('add_at_least_one_ring'))
            return
        
        diameter = self.diameter_input.value()
        spindle_diameter = self.spindle_diameter_input.value()
        outer_circle_width = self.outer_circle_width_input.value()
        ring_separation = self.ring_separation_input.value()
        
        # Get text positioning values
        disc_text = {
            'top': self.top_text_input.toPlainText(),
            'bottom': self.bottom_text_input.toPlainText()
        }
        
        svg_file = self.svg_generator.generate_disc(
            diameter, spindle_diameter, outer_circle_width, 
            ring_separation, self.ring_widgets, disc_text
        )
        
        self.temp_svg_file = type('TempFile', (), {'name': svg_file})()
        self.svg_widget.load(svg_file)
        self.adjust_svg_size()
        self.export_button.setEnabled(True)
    
    def export_file(self):
        try:
            if not self.temp_svg_file:
                QMessageBox.warning(self, self.tr('error'), self.tr('no_disc_to_export'))
                return
        
            if self.format_combo.currentText() == "SVG":
                file_filter = "SVG Files (*.svg)"
                default_ext = ".svg"
            elif self.format_combo.currentText() == "PDF" and PDF_AVAILABLE:
                file_filter = "PDF Files (*.pdf)"
                default_ext = ".pdf"
            else:
                file_filter = "SVG Files (*.svg)"
                default_ext = ".svg"
        
            file_path, _ = QFileDialog.getSaveFileName(
                self, self.tr('export_disc'), "", file_filter
            )
        
            if not file_path:
                return
        
            if not file_path.endswith(default_ext):
                file_path += default_ext
        
            if os.path.exists(file_path):
                reply = QMessageBox.question(
                    self, self.tr('warning'), f"'{file_path}' {self.tr('file_exists_overwrite')}",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return
        
            if self.format_combo.currentText() == "SVG":
                with open(self.temp_svg_file.name, 'r') as src, open(file_path, 'w') as dst:
                    dst.write(src.read())
            elif self.format_combo.currentText() == "PDF" and PDF_AVAILABLE:
                drawing = svg2rlg(self.temp_svg_file.name)
                
                disc_diameter_mm = self.diameter_input.value()
                disc_diameter_pt = disc_diameter_mm * 2.83465
                
                paper_format = self.page_size_combo.currentText()
                if paper_format == "A4":
                    pagesize = A4
                elif paper_format == "Letter":
                    pagesize = LETTER
                elif paper_format == "Legal":
                    pagesize = LEGAL
                elif paper_format == "A3":
                    pagesize = A3
                else:
                    pagesize = A4
                
                page_width, page_height = pagesize
                
                x_offset = (page_width - disc_diameter_pt) / 2
                y_offset = (page_height - disc_diameter_pt) / 2
                
                from reportlab.graphics.shapes import Drawing, Group
                
                new_drawing = Drawing(page_width, page_height)
                
                group = Group(drawing)
                scale_factor = disc_diameter_pt / drawing.width
                group.scale(scale_factor, scale_factor)
                group.translate(x_offset, y_offset)
                
                new_drawing.add(group)
                
                renderPDF.drawToFile(new_drawing, file_path, pagesize=pagesize)
            else:
                # Fallback to SVG if PDF not available
                with open(self.temp_svg_file.name, 'r') as src, open(file_path, 'w') as dst:
                    dst.write(src.read())
        
        except Exception as e:
            QMessageBox.critical(self, self.tr('error'), f"{self.tr('error_saving_file')} {e}")
    
    def change_language(self, index):
        new_language = 'en' if index == 0 else 'es'
        if new_language != self.current_language:
            self.current_language = new_language
            self.config_manager.set('language', new_language)
            self.update_ui_language()
    
    def update_ui_language(self):
        self.setWindowTitle(self.tr('app_title'))
        
        self.tab_widget.setTabText(0, self.tr('rings_tab'))
        self.tab_widget.setTabText(1, self.tr('config_tab'))
        self.tab_widget.setTabText(2, self.tr('export_tab'))
        self.tab_widget.setTabText(3, self.tr('presets_tab'))
        
        self.add_ring_button.setText(f"+ {self.tr('add_ring')}")
        
        if hasattr(self, 'measurements_title'):
            self.measurements_title.setText(self.tr('measurements_mm'))
        if hasattr(self, 'diameter_label'):
            self.diameter_label.setText(self.tr('total_diameter'))
        if hasattr(self, 'spindle_diameter_label'):
            self.spindle_diameter_label.setText(self.tr('spindle_diameter'))
        if hasattr(self, 'outer_circle_width_label'):
            self.outer_circle_width_label.setText(self.tr('outer_circle_width'))
        if hasattr(self, 'ring_separation_label'):
            self.ring_separation_label.setText(self.tr('ring_separation'))
        if hasattr(self, 'language_label'):
            self.language_label.setText(self.tr('language'))
        
        # Text positioning labels
        if hasattr(self, 'disc_text_title'):
            self.disc_text_title.setText(self.tr('disc_text'))
        if hasattr(self, 'top_text_label'):
            self.top_text_label.setText(self.tr('text_top'))
        if hasattr(self, 'bottom_text_label'):
            self.bottom_text_label.setText(self.tr('text_bottom'))
        
        if hasattr(self, 'export_format_label'):
            self.export_format_label.setText(self.tr('export_format'))
        if hasattr(self, 'page_size_label'):
            self.page_size_label.setText(self.tr('page_size'))
        if hasattr(self, 'export_button'):
            self.export_button.setText(self.tr('export'))
        
        if hasattr(self, 'save_preset_button'):
            self.save_preset_button.setText(self.tr('save_as_new_preset'))
        
        # Update presets list to refresh tooltips
        if hasattr(self, 'presets_list'):
            self.load_presets_list()
        
        if hasattr(self, 'language_combo'):
            current_index = self.language_combo.currentIndex()
            self.language_combo.blockSignals(True)
            self.language_combo.clear()
            self.language_combo.addItems([self.tr('english'), self.tr('spanish')])
            self.language_combo.setCurrentIndex(current_index)
            self.language_combo.currentIndexChanged.connect(self.change_language)
            self.language_combo.blockSignals(False)
        
        for i, ring_widget in enumerate(self.ring_widgets):
            ring_widget.update_language(self.current_language)
        
        self.schedule_preview_update()

    def get_current_settings(self):
        return {
            'rings': [ring.get_settings() for ring in self.ring_widgets],
            'diameter': self.diameter_input.value(),
            'spindle_diameter': self.spindle_diameter_input.value(),
            'outer_circle_width': self.outer_circle_width_input.value(),
            'ring_separation': self.ring_separation_input.value(),
            'text_top': self.top_text_input.toPlainText(),
            'text_bottom': self.bottom_text_input.toPlainText()
        }
    
    def load_preset_data(self, preset_data):
        # Clear all rings without validation
        for widget in self.ring_widgets:
            self.rings_layout.removeWidget(widget)
            widget.deleteLater()
        self.ring_widgets.clear()
        
        self.diameter_input.setValue(preset_data.get('diameter', 200))
        self.spindle_diameter_input.setValue(preset_data.get('spindle_diameter', 7.0))
        self.outer_circle_width_input.setValue(preset_data.get('outer_circle_width', 1.0))
        self.ring_separation_input.setValue(preset_data.get('ring_separation', 1.0))
        
        # Load text positioning values
        self.top_text_input.setPlainText(preset_data.get('text_top', ''))
        self.bottom_text_input.setPlainText(preset_data.get('text_bottom', ''))
        
        for ring_data in preset_data.get('rings', []):
            self.add_ring()
            ring_widget = self.ring_widgets[-1]
            
            # Set RPM value - check if it matches dropdown options first
            rpm_value = ring_data.get('rpm', 33.33)
            rpm_dropdown_values = {16: 0, 33.33: 1, 45: 2, 78: 3}  # value: index mapping
            
            if rpm_value in rpm_dropdown_values:
                # Use dropdown selection
                ring_widget.rpm_manual_check.setChecked(False)
                ring_widget.rpm_combo.setCurrentIndex(rpm_dropdown_values[rpm_value])
            else:
                # Use manual input
                ring_widget.rpm_manual_check.setChecked(True)
                ring_widget.rpm_input.setValue(rpm_value)
            ring_widget.hz_combo.setCurrentText(str(int(ring_data.get('hz', 50))))
            ring_widget.depth_input.setValue(ring_data.get('depth', 8))
            ring_widget.mode_combo.setCurrentIndex(0 if ring_data.get('single_mode', True) else 1)
            ring_widget.shape_combo.setCurrentIndex(0 if ring_data.get('shape_type', 'lines') == 'lines' else 1)
            ring_widget.density_combo.setCurrentIndex(0 if ring_data.get('density', 'double') == 'double' else 1)
            
            dot_size_str = f"{ring_data.get('dot_size', 1)}x"
            dot_size_index = ring_widget.dot_size_combo.findText(dot_size_str)
            if dot_size_index >= 0:
                ring_widget.dot_size_combo.setCurrentIndex(dot_size_index)
        
        self.schedule_preview_update()
    
    def save_new_preset(self):
        name, ok = QInputDialog.getText(self, self.tr('preset_name'), self.tr('preset_name_dialog'))
        if ok and name.strip():
            name = name.strip()
            presets = self.config_manager.get('presets', {})
            presets[name] = self.get_current_settings()
            self.config_manager.set('presets', presets)
            self.load_presets_list()
    
    def load_presets_list(self):
        self.presets_list.clear()
        presets = self.config_manager.get('presets', {})
        
        for preset_name in presets.keys():
            item = QListWidgetItem(preset_name)
            self.presets_list.addItem(item)
            
            widget = QWidget()
            main_layout = QVBoxLayout(widget)
            main_layout.setContentsMargins(8, 8, 8, 8)
            main_layout.setSpacing(5)
            
            name_label = QLabel(preset_name)
            name_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 13px;")
            main_layout.addWidget(name_label)
            
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(3)
            buttons_layout.addStretch()
            
            load_button = QPushButton("⭳")
            load_button.setToolTip(self.tr('load'))
            load_button.setStyleSheet("""
                QPushButton {
                    background-color: #569cd6;
                    color: white;
                    border: none;
                    padding: 4px;
                    border-radius: 2px;
                    font-size: 10px;
                    min-width: 15px;
                    min-height: 15px;
                    max-width: 15px;
                    max-height: 15px;
                }
                QPushButton:hover {
                    background-color: #6aa4d8;
                }
            """)
            load_button.clicked.connect(lambda checked, name=preset_name: self.load_preset(name))
            buttons_layout.addWidget(load_button)
            
            save_button = QPushButton("💾")
            save_button.setToolTip(self.tr('save'))
            save_button.setStyleSheet("""
                QPushButton {
                    background-color: #569cd6;
                    color: white;
                    border: none;
                    padding: 4px;
                    border-radius: 2px;
                    font-size: 10px;
                    min-width: 15px;
                    min-height: 15px;
                    max-width: 15px;
                    max-height: 15px;
                }
                QPushButton:hover {
                    background-color: #6aa4d8;
                }
            """)
            save_button.clicked.connect(lambda checked, name=preset_name: self.save_preset(name))
            buttons_layout.addWidget(save_button)
            
            rename_button = QPushButton("✏️")
            rename_button.setToolTip(self.tr('rename'))
            rename_button.setStyleSheet("""
                QPushButton {
                    background-color: #569cd6;
                    color: white;
                    border: none;
                    padding: 4px;
                    border-radius: 2px;
                    font-size: 10px;
                    min-width: 15px;
                    min-height: 15px;
                    max-width: 15px;
                    max-height: 15px;
                }
                QPushButton:hover {
                    background-color: #6aa4d8;
                }
            """)
            rename_button.clicked.connect(lambda checked, name=preset_name: self.rename_preset(name))
            buttons_layout.addWidget(rename_button)
            
            delete_button = QPushButton("🗑️")
            delete_button.setToolTip(self.tr('delete'))
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 4px;
                    border-radius: 2px;
                    font-size: 10px;
                    min-width: 15px;
                    min-height: 15px;
                    max-width: 15px;
                    max-height: 15px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            delete_button.clicked.connect(lambda checked, name=preset_name: self.delete_preset(name))
            buttons_layout.addWidget(delete_button)
            
            main_layout.addLayout(buttons_layout)
            
            self.presets_list.setItemWidget(item, widget)
            item.setSizeHint(QSize(widget.sizeHint().width(), 85))
    
    def load_preset(self, name):
        presets = self.config_manager.get('presets', {})
        if name in presets:
            self.load_preset_data(presets[name])
    
    def save_preset(self, name):
        presets = self.config_manager.get('presets', {})
        presets[name] = self.get_current_settings()
        self.config_manager.set('presets', presets)
    
    def rename_preset(self, name):
        new_name, ok = QInputDialog.getText(self, self.tr('rename'), self.tr('enter_new_name'), text=name)
        if ok and new_name.strip() and new_name.strip() != name:
            new_name = new_name.strip()
            presets = self.config_manager.get('presets', {})
            if name in presets:
                presets[new_name] = presets.pop(name)
                self.config_manager.set('presets', presets)
                self.load_presets_list()
    
    def delete_preset(self, name):
        reply = QMessageBox.question(
            self, self.tr('delete'), self.tr('confirm_delete'),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            presets = self.config_manager.get('presets', {})
            if name in presets:
                del presets[name]
                self.config_manager.set('presets', presets)
                self.load_presets_list()

    def closeEvent(self, event):
        self.temp_dir.cleanup()