import sys
import os
import shutil
import json
from pathlib import Path
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect, QUrl, QTimer
from PySide6.QtGui import QColor, QDesktopServices, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QTextEdit,
    QFileDialog, QLabel, QFrame, QGraphicsDropShadowEffect, 
    QDialog, QStackedWidget, QProgressBar
)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

CONFIG_FILE = Path("config.json")
DEFAULT_MAP = {
    "Export": [".obj", ".fbx"],
    "Max": [".max", ".3ds"],
    "Textures": [".jpg", ".png", ".mtl"]
}

MODERN_STYLE = """
QMainWindow, QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #090d16, stop:0.5 #111827, stop:1 #0f172a);
}
QFrame#mainPanel, QFrame#dialogPanel {
    background-color: rgba(30, 41, 59, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
}
QFrame#titleBar {
    background-color: rgba(0, 0, 0, 0.35);
    border-top-left-radius: 16px;
    border-top-right-radius: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
QLabel#titleText {
    color: #f8fafc;
    font-weight: bold;
    font-size: 13px;
}
QPushButton#minBtn, QPushButton#closeBtn {
    border-radius: 6px;
    border: none;
    color: transparent;
    font-size: 11px;
    font-weight: bold;
    padding-bottom: 2px;
}
QPushButton#minBtn { background-color: #facc15; }
QPushButton#minBtn:hover { background-color: #fde047; color: #713f12; }
QPushButton#closeBtn { background-color: #f43f5e; }
QPushButton#closeBtn:hover { background-color: #fb7185; color: #881337; }
QFrame#sidebar {
    background-color: rgba(15, 23, 42, 0.65);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom-left-radius: 16px;
}
QPushButton.navBtn {
    background: transparent;
    border: none;
    border-radius: 10px;
    color: #94a3b8;
    font-weight: bold;
    font-size: 13px;
    text-align: left;
    padding: 12px 14px;
}
QPushButton.navBtn:hover {
    background-color: rgba(255, 255, 255, 0.08);
    color: #f8fafc;
}
QPushButton.navBtn[active="true"] {
    background-color: rgba(99, 102, 241, 0.25);
    color: #818cf8;
    border-left: 3px solid #6366f1;
}
QLineEdit, QTextEdit {
    background-color: rgba(9, 13, 22, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    padding: 8px 12px;
    color: #f8fafc;
    font-size: 13px;
    selection-background-color: #6366f1;
}
QLineEdit:focus {
    border: 1px solid rgba(129, 140, 248, 0.9);
    background-color: rgba(9, 13, 22, 0.95);
}
QLabel {
    color: #e2e8f0;
    font-weight: 600;
    font-size: 13px;
    background: transparent;
}
QPushButton {
    outline: none;
    border-radius: 10px;
    font-size: 13px;
    font-weight: bold;
    color: white;
}
QPushButton#browseBtn, QPushButton#openFolderBtn, QPushButton#clearLogBtn {
    background-color: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.22);
}
QPushButton#browseBtn:hover, QPushButton#openFolderBtn:hover, QPushButton#clearLogBtn:hover {
    background-color: rgba(255, 255, 255, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.55);
}
QPushButton#browseBtn:pressed, QPushButton#openFolderBtn:pressed {
    background-color: rgba(255, 255, 255, 0.08);
}
QPushButton#sortBtn, QPushButton#saveConfigBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #4f46e5);
    border: 1px solid rgba(129, 140, 248, 0.4);
}
QPushButton#sortBtn:hover, QPushButton#saveConfigBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #6366f1);
    border: 1px solid rgba(255, 255, 255, 0.85);
}
QPushButton#sortBtn:pressed, QPushButton#saveConfigBtn:pressed {
    background: #1d4ed8;
}
QPushButton#undoBtn, QPushButton#resetConfigBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dc2626, stop:1 #e11d48);
    border: 1px solid rgba(251, 113, 133, 0.4);
}
QPushButton#undoBtn:hover, QPushButton#resetConfigBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ef4444, stop:1 #f43f5e);
    border: 1px solid rgba(255, 255, 255, 0.85);
}
QPushButton#undoBtn:pressed, QPushButton#resetConfigBtn:pressed {
    background: #b91c1c;
}
QProgressBar {
    background-color: rgba(9, 13, 22, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    text-align: center;
    color: #f8fafc;
    font-size: 11px;
    font-weight: bold;
    max-height: 14px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #6366f1);
    border-radius: 5px;
}
"""

class CollapsibleSidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.min_width = 50
        self.max_width = 160
        self.setFixedWidth(self.min_width)

        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(260)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.animation_max = QPropertyAnimation(self, b"maximumWidth")
        self.animation_max.setDuration(260)
        self.animation_max.setEasingCurve(QEasingCurve.InOutCubic)

        self.collapse_timer = QTimer(self)
        self.collapse_timer.setSingleShot(True)
        self.collapse_timer.setInterval(220)
        self.collapse_timer.timeout.connect(self._do_collapse)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.collapse_timer.stop()
        self.expand()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.collapse_timer.start()

    def expand(self):
        self.animation.stop()
        self.animation_max.stop()
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(self.max_width)
        self.animation_max.setStartValue(self.width())
        self.animation_max.setEndValue(self.max_width)
        self.animation.start()
        self.animation_max.start()

    def _do_collapse(self):
        self.animation.stop()
        self.animation_max.stop()
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(self.min_width)
        self.animation_max.setStartValue(self.width())
        self.animation_max.setEndValue(self.min_width)
        self.animation.start()
        self.animation_max.start()


class CustomMessageBox(QDialog):
    def __init__(self, parent, title: str, text: str, is_error: bool = False):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(440)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        panel = QFrame()
        panel.setObjectName("dialogPanel")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 220))
        shadow.setOffset(0, 8)
        panel.setGraphicsEffect(shadow)

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(28, 24, 28, 24)
        panel_layout.setSpacing(14)

        icon_str = "❌" if is_error else "✨"
        title_lbl = QLabel(f"{icon_str}  {title}")
        title_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        panel_layout.addWidget(title_lbl)

        msg_lbl = QLabel(text)
        msg_lbl.setStyleSheet("color: #e2e8f0; font-size: 14px; font-weight: normal; line-height: 1.4;")
        msg_lbl.setWordWrap(True)
        panel_layout.addWidget(msg_lbl)

        panel_layout.addSpacing(6)

        ok_btn = QPushButton("OK")
        ok_btn.setObjectName("sortBtn" if not is_error else "undoBtn")
        ok_btn.setFixedSize(120, 40)
        ok_btn.clicked.connect(self.accept)
        panel_layout.addWidget(ok_btn, alignment=Qt.AlignRight)

        layout.addWidget(panel)
        self.adjustSize()


class TitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setObjectName("titleBar")
        self.setFixedHeight(38)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)

        title_label = QLabel("Сортировщик файлов")
        title_label.setObjectName("titleText")
        layout.addWidget(title_label)

        layout.addStretch()

        self.min_btn = QPushButton("−")
        self.min_btn.setObjectName("minBtn")
        self.min_btn.setFixedSize(14, 14)
        self.min_btn.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(self.min_btn)

        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(14, 14)
        self.close_btn.clicked.connect(self.parent_window.close)
        layout.addWidget(self.close_btn)

        self._drag_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent_window.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()


class ProjectSorterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(720, 560)
        self.setAcceptDrops(True)

        icon_path = resource_path("icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet(MODERN_STYLE)
        self.sort_map = self.load_or_create_config()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.main_panel = QFrame()
        self.main_panel.setObjectName("mainPanel")
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 6)
        self.main_panel.setGraphicsEffect(shadow)

        panel_layout = QVBoxLayout(self.main_panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        panel_layout.addWidget(self.title_bar)

        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        sidebar = CollapsibleSidebar()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(8)

        self.btn_nav_sorter = QPushButton("📁  Сортировка")
        self.btn_nav_sorter.setProperty("class", "navBtn")
        self.btn_nav_sorter.setProperty("active", "true")
        self.btn_nav_sorter.clicked.connect(lambda: self.switch_tab(0))

        self.btn_nav_settings = QPushButton("⚙️  Настройки")
        self.btn_nav_settings.setProperty("class", "navBtn")
        self.btn_nav_settings.setProperty("active", "false")
        self.btn_nav_settings.clicked.connect(lambda: self.switch_tab(1))

        sidebar_layout.addWidget(self.btn_nav_sorter)
        sidebar_layout.addWidget(self.btn_nav_settings)
        sidebar_layout.addStretch()

        body_layout.addWidget(sidebar)

        self.pages = QStackedWidget()
        self.pages.addWidget(self.create_sorter_page())
        self.pages.addWidget(self.create_settings_page())
        
        body_layout.addWidget(self.pages)
        panel_layout.addLayout(body_layout)
        
        status_bar = QFrame()
        status_bar.setStyleSheet("background: rgba(0,0,0,0.25); border-bottom-left-radius: 16px; border-bottom-right-radius: 16px;")
        status_bar.setFixedHeight(26)
        sb_layout = QHBoxLayout(status_bar)
        sb_layout.setContentsMargins(15, 0, 15, 0)
        self.status_lbl = QLabel(f"Config: {CONFIG_FILE.resolve()}")
        self.status_lbl.setStyleSheet("font-size: 11px; color: #64748b; font-weight: normal;")
        sb_layout.addWidget(self.status_lbl)
        panel_layout.addWidget(status_bar)

        main_layout.addWidget(self.main_panel)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if Path(url.toLocalFile()).is_dir():
                    event.acceptProposedAction()
                    return

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            folder_path = Path(url.toLocalFile())
            if folder_path.is_dir():
                self.path_input.setText(str(folder_path))
                self.switch_tab(0)
                break

    def create_sorter_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)

        folder_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Путь к рабочей директории...")
        self.path_input.setFixedHeight(38)
        
        browse_btn = QPushButton("Обзор")
        browse_btn.setObjectName("browseBtn")
        browse_btn.setFixedSize(80, 38)
        browse_btn.clicked.connect(self.select_folder)

        open_folder_btn = QPushButton("📂")
        open_folder_btn.setObjectName("openFolderBtn")
        open_folder_btn.setFixedSize(45, 38)
        open_folder_btn.clicked.connect(self.open_in_explorer)
        
        folder_layout.addWidget(self.path_input)
        folder_layout.addWidget(browse_btn)
        folder_layout.addWidget(open_folder_btn)
        layout.addLayout(folder_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        self.sort_btn = QPushButton("Сортировать")
        self.sort_btn.setObjectName("sortBtn")
        self.sort_btn.setFixedHeight(42)
        self.sort_btn.clicked.connect(self.run_sorting)
        
        self.undo_btn = QPushButton("Отменить")
        self.undo_btn.setObjectName("undoBtn")
        self.undo_btn.setFixedHeight(42)
        self.undo_btn.clicked.connect(self.undo_sorting)

        buttons_layout.addWidget(self.sort_btn, 2)
        buttons_layout.addWidget(self.undo_btn, 1)
        layout.addLayout(buttons_layout)

        log_header = QHBoxLayout()
        log_header.addWidget(QLabel("Журнал:"))
        log_header.addStretch()
        clear_btn = QPushButton("Очистить")
        clear_btn.setObjectName("clearLogBtn")
        clear_btn.setFixedSize(75, 24)
        clear_btn.setStyleSheet("font-size: 11px; padding: 2px;")
        clear_btn.clicked.connect(lambda: self.log_area.clear())
        log_header.addWidget(clear_btn)
        layout.addLayout(log_header)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

        return page

    def create_settings_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)

        layout.addWidget(QLabel("Добавление правила:"))

        form_layout = QHBoxLayout()
        self.folder_name_input = QLineEdit()
        self.folder_name_input.setPlaceholderText("Имя папки")
        self.folder_name_input.setFixedHeight(36)

        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText("Расширения (.zip, .rar)")
        self.ext_input.setFixedHeight(36)

        form_layout.addWidget(self.folder_name_input, 1)
        form_layout.addWidget(self.ext_input, 2)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        save_btn.setObjectName("saveConfigBtn")
        save_btn.setFixedHeight(38)
        save_btn.clicked.connect(self.add_rule_and_save)

        reset_btn = QPushButton("Сбросить")
        reset_btn.setObjectName("resetConfigBtn")
        reset_btn.setFixedHeight(38)
        reset_btn.clicked.connect(self.reset_config)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(reset_btn)
        layout.addLayout(btn_layout)

        layout.addWidget(QLabel("Активная конфигурация:"))
        self.config_display = QTextEdit()
        self.config_display.setReadOnly(True)
        layout.addWidget(self.config_display)

        self.update_config_display()
        return page

    def switch_tab(self, index: int):
        self.pages.setCurrentIndex(index)
        is_sorter = (index == 0)
        self.btn_nav_sorter.setProperty("active", "true" if is_sorter else "false")
        self.btn_nav_settings.setProperty("active", "false" if is_sorter else "true")
        self.btn_nav_sorter.style().unpolish(self.btn_nav_sorter)
        self.btn_nav_sorter.style().polish(self.btn_nav_sorter)
        self.btn_nav_settings.style().unpolish(self.btn_nav_settings)
        self.btn_nav_settings.style().polish(self.btn_nav_settings)

    def load_or_create_config(self) -> dict:
        if not CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump(DEFAULT_MAP, f, indent=4, ensure_ascii=False)
            except Exception:
                return DEFAULT_MAP.copy()

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_MAP.copy()

    def update_config_display(self):
        text_lines = []
        for folder, exts in self.sort_map.items():
            text_lines.append(f"<b>{folder}/</b> : <font color='#818cf8'>{', '.join(exts)}</font>")
        self.config_display.setHtml("<br>".join(text_lines))

    def add_rule_and_save(self):
        folder = self.folder_name_input.text().strip()
        exts_str = self.ext_input.text().strip()
        if not folder or not exts_str:
            self.show_message("Ошибка", "Заполните оба поля", is_error=True)
            return

        exts = [e.strip().lower() for e in exts_str.split(",") if e.strip()]
        exts = [e if e.startswith(".") else f".{e}" for e in exts]

        self.sort_map[folder] = exts
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.sort_map, f, indent=4, ensure_ascii=False)

        self.folder_name_input.clear()
        self.ext_input.clear()
        self.update_config_display()
        self.show_message("Успешно", f"Правило для папки {folder} сохранено")

    def reset_config(self):
        self.sort_map = DEFAULT_MAP.copy()
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.sort_map, f, indent=4, ensure_ascii=False)
        self.update_config_display()
        self.show_message("Успешно", "Конфигурация сброшена по умолчанию")

    def show_message(self, title: str, text: str, is_error: bool = False):
        dlg = CustomMessageBox(self, title, text, is_error)
        dlg.exec()

    def log(self, html_message: str):
        self.log_area.insertHtml(html_message + "<br>")
        self.log_area.ensureCursorVisible()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите директорию")
        if folder:
            self.path_input.setText(folder)

    def open_in_explorer(self):
        target_dir = self.get_valid_target_dir()
        if target_dir:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(target_dir)))

    def get_valid_target_dir(self):
        folder_path_str = self.path_input.text().strip()
        if not folder_path_str:
            self.show_message("Ошибка", "Укажите путь к директории", is_error=True)
            return None

        target_dir = Path(folder_path_str)
        if not target_dir.exists() or not target_dir.is_dir():
            self.show_message("Ошибка", "Указанной директории не существует", is_error=True)
            return None
            
        return target_dir

    def run_sorting(self):
        target_dir = self.get_valid_target_dir()
        if not target_dir:
            return

        self.log_area.clear()
        self.progress_bar.setValue(0)
        self.log(f"<b>Директория:</b> {target_dir}")

        extension_to_folder = {}
        for folder_name, extensions in self.sort_map.items():
            for ext in extensions:
                extension_to_folder[ext.lower()] = folder_name

        created_folders = {}
        for folder_name in self.sort_map.keys():
            subfolder_path = target_dir / folder_name
            subfolder_path.mkdir(exist_ok=True)
            created_folders[folder_name] = subfolder_path

        files_to_move = [f for f in target_dir.iterdir() if f.is_file() and f.suffix.lower() in extension_to_folder]
        total_files = len(files_to_move)

        if total_files == 0:
            self.log("<i>Файлов для сортировки не обнаружено.</i>")
            self.show_message("Информация", "В директории нет файлов, соответствующих фильтрам")
            return

        self.log("<i>Обработка...</i>")
        moved_count = 0

        for i, item in enumerate(files_to_move, 1):
            ext = item.suffix.lower()
            dest_folder_name = extension_to_folder[ext]
            dest_folder_path = created_folders[dest_folder_name]
            destination_file = dest_folder_path / item.name

            counter = 1
            while destination_file.exists():
                destination_file = dest_folder_path / f"{item.stem}_{counter}{item.suffix}"
                counter += 1

            try:
                shutil.move(str(item), str(destination_file))
                self.log(f"&nbsp;&nbsp;&nbsp;&nbsp;-> <font color='#818cf8'>{item.name}</font> -> <b>{dest_folder_name}/{destination_file.name}</b>")
                moved_count += 1
            except Exception as e:
                self.log(f"&nbsp;&nbsp;&nbsp;&nbsp;[!] Ошибка перемещения {item.name}: {e}")

            self.progress_bar.setValue(int((i / total_files) * 100))
            QApplication.processEvents()

        self.log(f"<b>Готово.</b> Перемещено файлов: <b>{moved_count}</b>")
        self.show_message("Завершено", f"Обработано файлов: {moved_count}")

    def undo_sorting(self):
        target_dir = self.get_valid_target_dir()
        if not target_dir:
            return

        self.log_area.clear()
        self.progress_bar.setValue(0)
        self.log(f"<b>Отмена операции в:</b> {target_dir}")

        files_to_restore = []
        for folder_name in self.sort_map.keys():
            subfolder_path = target_dir / folder_name
            if subfolder_path.exists() and subfolder_path.is_dir():
                files_to_restore.extend([f for f in subfolder_path.iterdir() if f.is_file()])

        total_files = len(files_to_restore)
        if total_files == 0:
            self.log("<i>Целевые директории пусты или отсутствуют.</i>")
            self.show_message("Информация", "Нет файлов для возврата")
            return

        restored_count = 0
        for i, item in enumerate(files_to_restore, 1):
            destination_file = target_dir / item.name
            counter = 1
            while destination_file.exists():
                destination_file = target_dir / f"{item.stem}_returned_{counter}{item.suffix}"
                counter += 1

            try:
                shutil.move(str(item), str(destination_file))
                self.log(f"&nbsp;&nbsp;&nbsp;&nbsp;<- <font color='#38bdf8'>{item.name}</font> из <b>{item.parent.name}/</b>")
                restored_count += 1
            except Exception as e:
                self.log(f"&nbsp;&nbsp;&nbsp;&nbsp;[!] Ошибка возврата: {e}")

            self.progress_bar.setValue(int((i / total_files) * 100))
            QApplication.processEvents()

        for folder_name in self.sort_map.keys():
            subfolder_path = target_dir / folder_name
            if subfolder_path.exists():
                try:
                    subfolder_path.rmdir()
                    self.log(f"&nbsp;&nbsp;&nbsp;&nbsp;[-] Пустая директория удалена: {folder_name}/")
                except OSError:
                    self.log(f"&nbsp;&nbsp;&nbsp;&nbsp;[!] Директория не пуста, пропущено: {folder_name}/")

        self.log(f"<b>Операция отменена.</b> Возвращено файлов: <b>{restored_count}</b>")
        self.show_message("Завершено", f"Возвращено файлов: {restored_count}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectSorterApp()
    window.show()
    sys.exit(app.exec())