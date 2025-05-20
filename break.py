from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSystemTrayIcon, QMenu, QLineEdit, QHBoxLayout
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QTimer
import sys
import ctypes
import os
import threading

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class BreakPauseApp(QWidget):
    """
    Esta aplicación ayuda a gestionar pausas activas para evitar fatiga frente al computador.
    - Mantiene el sistema activo evitando suspensión y bloqueo.
    - Se minimiza en la bandeja del sistema en lugar de cerrarse al presionar el icono de cerrar.
    """
    
    def __init__(self):
        
        super().__init__()
        self.running = False 
        print
        self.setWindowIcon(QIcon(resource_path("icon_break.ico")))
        self.initUI()
        self.initTrayIcon()


    def initUI(self):
        self.setWindowTitle("Break!")
        self.setGeometry(100, 100, 200, 100)  
        self.style("background-color: #582263; border-radius: 10px;")

        layout = QVBoxLayout()

        self.status_label = QLabel("Inactivo")
        self.style_widget(self.status_label, "color: red; font-size: 10px; font-weight: bold; background-color: #25002c; border-radius: 10px; padding: 10px;")
        self.status_label.setFixedHeight(40)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.start_button = QPushButton("Iniciar")
        self.style_widget(self.start_button, """
            QPushButton {
                background-color: #8806a1; color: white; border-radius: 10px; padding: 10px;
            }
            QPushButton:hover { background-color: #7c0094; }
            QPushButton:pressed { background-color: #605D5D; }
        """)
        self.start_button.clicked.connect(self.start)
        layout.addWidget(self.start_button)

        container = QWidget()
        layout_input = QHBoxLayout(container)
        layout_input.setContentsMargins(0, 0, 0, 0)
        layout_input.setSpacing(2)

        self.timer_input = QLineEdit()
        self.timer_input.setPlaceholderText("Temporizador en minutos")
        self.timer_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_input.setFixedHeight(40)
        self.timer_input.setToolTip("Temporizador en minutos, ingrese los minutos en los cuales el temporizador estará activo.")
        style = "background-color: #8806a1; color: white; border-radius: 10px; padding: 10px; font-size: 12px;"
        self.timer_input.setStyleSheet("QLineEdit {" + style + "}")

        self.start_timer_button = QPushButton("▶")
        self.start_timer_button.setFixedSize(40, 40)
        self.start_timer_button.setStyleSheet("QPushButton {" + style + "} QPushButton:hover {background-color: #75008d;}")
        self.start_timer_button.clicked.connect(self.start_timer)

        layout_input.addWidget(self.timer_input)
        layout_input.addWidget(self.start_timer_button)
        layout.addWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.stop_button = QPushButton("Detener")
        self.style_widget(self.stop_button, """
            QPushButton {
                background-color: #e74c3c; color: white; border-radius: 10px; padding: 10px;
            }
            QPushButton:hover { background-color: #ec7063; }
            QPushButton:pressed { background-color: #c0392b; }
        """)
        self.stop_button.clicked.connect(self.stop)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def start_timer(self):
        try:
            minutes = int(self.timer_input.text())
            self.remaining_time = minutes * 60
            self.timer.start(1000)
            self.start()
        except ValueError:
            self.timer_input.setPlaceholderText("Ingrese un número válido")

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_input.setText(f"{minutes:02}:{seconds:02} min")
        else:
            self.stop()
            self.timer_input.setText("Temporizador en minutos")

    def stop_timer(self):
        self.timer.stop()
        self.remaining_time = 0
        self.timer_input.clear()
        self.timer_input.setPlaceholderText("Temporizador en minutos")

    def initTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(QIcon(resource_path("icon_break.ico")), self)
        tray_menu = QMenu()
        restore_action = QAction("Restaurar", self)
        restore_action.triggered.connect(self.showNormal)
        tray_menu.addAction(restore_action)
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.quitApp)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def quitApp(self):
        self.tray_icon.hide()
        QApplication.quit()

    def generate_event(self):
        self.running = True
        while self.running:
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

    def start(self):
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self.generate_event, daemon=True)
            thread.start()
            self.status_label.setText("Activo")
            self.style_widget(self.status_label, "color: #19001e; font-size: 10px; font-weight: bold; background-color: #00CCBE; border-radius: 10px; padding: 10px;")

    def stop(self):
        self.running = False
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        self.status_label.setText("Inactivo")
        self.stop_timer()
        self.style_widget(self.status_label, "color: red; font-size: 10px; font-weight: bold; background-color: #25002c; border-radius: 10px; padding: 10px;")

    def style(self, parametros):
        self.setStyleSheet(f"{parametros}")
    
    def style_widget(self, widget, parametros):
        widget.setStyleSheet(f"{parametros}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BreakPauseApp()
    window.show()
    sys.exit(app.exec())