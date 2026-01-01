import sys
import os
import json
import shutil
import subprocess
import threading
import random
import time
from datetime import datetime
import tempfile
import wave
import pyaudio
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea, QFrame, QListWidget,
    QDialog, QFileDialog, QMessageBox, QMenu
)
from PyQt6.QtGui import QPixmap, QFont, QColor, QPalette, QIcon, QAction
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QEasingCurve, QPropertyAnimation, QPoint, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


# ------------------------
# Sleeker Space Palette
# ------------------------
COLORS = {
    "bg": "#0c101a",
    "chat_bg": "#101622",
    "self_bubble": "#182030",
    "peer_bubble": "#1c1828",
    "input_bg": "#141926",
    "button": "#5a7af5",
    "button_hover": "#6d8df7",
    "text": "#e6ebf5",
    "timestamp": "#8a95aa",
    "border": "#252c3d",
}

# ------------------------
# Paths
# ------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_DIR = os.path.join(SCRIPT_DIR, "backgrounds")
ICONS_DIR = os.path.join(SCRIPT_DIR, "icons")
os.makedirs(BACKGROUND_DIR, exist_ok=True)


# ------------------------
# Helper: user downloads folder
# ------------------------
def get_user_download_dir(username):
    home = os.path.expanduser("~")
    download_dir = os.path.join(home, "Downloads", "SecureMessenger", username)
    os.makedirs(download_dir, exist_ok=True)
    return download_dir


# ------------------------
# History Manager
# ------------------------
class HistoryManager:
    def __init__(self, username):
        self.username = username
        self.history_file = os.path.join(get_user_download_dir(username), "history.json")
        self.messages = self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_message(self, msg_data):
        self.messages.append(msg_data)
        with open(self.history_file, 'w') as f:
            json.dump(self.messages, f, indent=2)





def generate_rsa_keys(user): pass
def load_private_path(user): return b"dummy_private"
def load_public_key(user): return b"dummy_public"
def encrypt_message(aes_key, msg): return msg[::-1]
def decrypt_message(aes_key, cipher): return cipher[::-1]
def sign_message(private_key, msg): return "signature"
def verify_signature(public_key, msg, sig): return True
def generate_aes_key(): return b"dummy_aes_key"


def open_file(filepath):
    try:
        if sys.platform == "win32":
            os.startfile(filepath)
        elif sys.platform == "darwin":
            subprocess.run(["open", filepath])
        else:
            subprocess.run(["xdg-open", filepath])
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Could not open file:\n{e}")


def get_file_icon(filename):
    ext = filename.split('.')[-1].lower() if '.' in filename else ""
    if ext in ("mp3", "wav", "ogg", "m4a", "aac"):
        return "🎵"
    elif ext in ("jpg", "jpeg", "png", "gif", "bmp", "webp"):
        return "🖼️"
    elif ext in ("pdf",):
        return "📄"
    elif ext in ("txt", "log"):
        return "📝"
    elif ext in ("doc", "docx"):
        return "📘"
    elif ext in ("xlsx", "xls"):
        return "📊"
    else:
        return "📎"



def get_current_time():
    return datetime.now().strftime("%H:%M")



def get_audio_duration(filepath):
    try:
        with wave.open(filepath, 'r') as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return f"{duration:.1f}s"
    except:
        return "?.?s"


class WaveformWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        self.setStyleSheet("background: transparent;")
        self.bars = []
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(1)
        for _ in range(18):
            bar = QFrame()
            bar.setFixedWidth(3)
            bar.setStyleSheet("background: #5a7af5; border-radius: 1px;")
            bar.setVisible(False)
            self.bars.append(bar)
            layout.addWidget(bar)

    def start_animation(self):
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate)
        self.animation_timer.start(120)
        for bar in self.bars:
            bar.setVisible(True)

    def stop_animation(self):
        if hasattr(self, 'animation_timer'):
            self.animation_timer.stop()
        for bar in self.bars:
            bar.setVisible(False)

    def _animate(self):
        for bar in self.bars:
            height = random.randint(4, 22)
            bar.setFixedHeight(height)


class StatusIndicator(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Secure end-to-end encryption")
        self.setFont(QFont("Segoe UI", 8))
        self.setStyleSheet(f"color: {COLORS['timestamp']}; padding: 2px;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(20)

    def show_encrypting(self):
        self.setText("🔒 Encrypting...")
        self.setStyleSheet(f"color: #FFD700; padding: 2px;")
        QTimer.singleShot(800, self.show_sending)

    def show_sending(self):
        self.setText("✉️ Sending...")
        self.setStyleSheet(f"color: #5a7af5; padding: 2px;")
        QTimer.singleShot(600, self.show_secure)

    def show_secure(self):
        self.setText("Secure")
        self.setStyleSheet(f"color: {COLORS['timestamp']}; padding: 2px;")

    def show_verifying(self):
        self.setText("🔍 Verifying...")
        self.setStyleSheet(f"color: #FFA500; padding: 2px;")
        QTimer.singleShot(600, self.show_verified)

    def show_verified(self):
        self.setText("✅ Verified!")
        self.setStyleSheet(f"color: #4CAF50; padding: 2px;")
        QTimer.singleShot(1200, self.show_secure)

    def show_error(self, error_msg):
        self.setText("❌ Error")
        self.setStyleSheet(f"color: #f44336; padding: 2px;")
        QTimer.singleShot(1500, self.show_secure)



class MessageBubble(QFrame):
    def __init__(self, text, is_self, timestamp, msg_id=""):
        super().__init__()
        self.is_self = is_self
        self.msg_id = msg_id
        self.reactions = []
        layout = QVBoxLayout()
        layout.setContentsMargins(14, 10, 14, 8)
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text_label.setFont(QFont("Segoe UI", 11))
        text_label.setStyleSheet(f"color: {COLORS['text']};")
        time_label = QLabel(timestamp)
        time_label.setFont(QFont("Segoe UI", 8))
        time_label.setStyleSheet(f"color: {COLORS['timestamp']};")
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(text_label)
        layout.addWidget(time_label)
        self.reactions_layout = QHBoxLayout()
        self.reactions_layout.setSpacing(6)
        layout.addLayout(self.reactions_layout)
        self.setLayout(layout)
        radius = "18px"
        corner_cut = "4px"
        if is_self:
            self.setStyleSheet(f"""
            background-color: {COLORS['self_bubble']};
            border-radius: {radius};
            border-bottom-right-radius: {corner_cut};
            padding: 0px;
            """)
        else:
            self.setStyleSheet(f"""
            background-color: {COLORS['peer_bubble']};
            border-radius: {radius};
            border-bottom-left-radius: {corner_cut};
            padding: 0px;
            """)

    def add_reaction(self, emoji, username):
        for r in self.reactions:
            if r['user'] == username and r['emoji'] == emoji:
                return
        self.reactions.append({'emoji': emoji, 'user': username})
        self._update_reactions_display()
        self._animate_reaction(emoji)

    def _update_reactions_display(self):
        while self.reactions_layout.count():
            child = self.reactions_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        emoji_count = {}
        for r in self.reactions:
            emoji_count[r['emoji']] = emoji_count.get(r['emoji'], 0) + 1
        for emoji, count in emoji_count.items():
            label_text = f"{emoji} {count}" if count > 1 else emoji
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 9))
            label.setStyleSheet(f"color: #a0c0ff; background: rgba(90, 122, 245, 0.15); padding: 1px 5px; border-radius: 6px;")
            self.reactions_layout.addWidget(label)
        self.reactions_layout.addStretch()

    def _animate_reaction(self, emoji):
        reaction = QLabel(emoji)
        reaction.setStyleSheet("font-size: 20px; background: transparent;")
        reaction.setParent(self.window())
        reaction.move(self.mapToGlobal(QPoint(15, -5)).x(), self.mapToGlobal(QPoint(15, -5)).y())
        reaction.show()
        anim1 = QPropertyAnimation(reaction, b"pos")
        anim1.setDuration(700)
        anim1.setStartValue(reaction.pos())
        anim1.setEndValue(QPoint(reaction.x(), reaction.y() - 80))
        anim1.setEasingCurve(QEasingCurve.Type.OutQuad)
        anim2 = QPropertyAnimation(reaction, b"windowOpacity")
        anim2.setDuration(700)
        anim2.setStartValue(1.0)
        anim2.setEndValue(0.0)
        anim1.start()
        anim2.start()
        QTimer.singleShot(700, reaction.deleteLater)


class FileBubble(QFrame):
    def __init__(self, filename, is_self, timestamp, filepath, duration="", main_window=None):
        super().__init__()
        self.is_self = is_self
        self.filepath = filepath
        self.main_window = main_window
        self.is_playing = False
        layout = QVBoxLayout()
        layout.setContentsMargins(14, 10, 14, 8)
        icon = get_file_icon(filename)
        display_name = f"{icon} {filename}"
        if duration:
            display_name += f" ({duration})"
        header = QLabel(display_name)
        header.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        header.setWordWrap(True)
        header.setStyleSheet(f"color: {COLORS['text']};")
        time_label = QLabel(timestamp)
        time_label.setFont(QFont("Segoe UI", 8))
        time_label.setStyleSheet(f"color: {COLORS['timestamp']};")
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(header)
        layout.addWidget(time_label)

        self.audio_layout = QHBoxLayout()
        self.audio_layout.setContentsMargins(0, 0, 0, 0)
        self.play_btn = QPushButton("▶")
        self.play_btn.setFixedSize(30, 30)
        self.play_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['button']};
            color: white;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['button_hover']};
        }}
        """)
        self.play_btn.clicked.connect(self.toggle_play)

        self.waveform_bars = []
        waveform_frame = QFrame()
        waveform_frame.setFixedHeight(20)
        waveform_layout = QHBoxLayout(waveform_frame)
        waveform_layout.setContentsMargins(5, 0, 5, 0)
        waveform_layout.setSpacing(1)
        for _ in range(15):
            bar = QFrame()
            bar.setFixedWidth(2)
            bar.setStyleSheet("background: #5a7af5; border-radius: 1px;")
            bar.setVisible(False)
            self.waveform_bars.append(bar)
            waveform_layout.addWidget(bar)
        self.waveform_frame = waveform_frame

        self.audio_layout.addWidget(self.play_btn)
        self.audio_layout.addWidget(self.waveform_frame)
        self.audio_layout.addStretch()

        if filepath.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a', '.aac')):
            layout.addLayout(self.audio_layout)
            self.is_audio = True
        else:
            self.is_audio = False

        btn_text = "📥 Open"
        self.button = QPushButton(btn_text)
        self.button.setFixedWidth(70)
        self.button.clicked.connect(self.on_click)
        self.button.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['button']};
            color: white;
            border-radius: 12px;
            padding: 3px;
            font-size: 9px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['button_hover']};
        }}
        """)
        if is_self:
            layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignRight)
        else:
            layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignLeft)

        if is_self:
            self.setStyleSheet(f"""
            background-color: {COLORS['self_bubble']};
            border-radius: 16px;
            border-bottom-right-radius: 4px;
            padding: 0px;
            """)
        else:
            self.setStyleSheet(f"""
            background-color: {COLORS['peer_bubble']};
            border-radius: 16px;
            border-bottom-left-radius: 4px;
            padding: 0px;
            """)

        self.setLayout(layout)

    def toggle_play(self):
        if not self.main_window:
            return
        if self.is_playing:
            self.main_window.stop_audio()
        else:
            self.main_window.play_audio(self.filepath, self)

    def start_waveform(self):
        self.is_playing = True
        self.play_btn.setText("⏸")
        for bar in self.waveform_bars:
            bar.setVisible(True)
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate_waveform)
        self.animation_timer.start(150)

    def stop_waveform(self):
        self.is_playing = False
        self.play_btn.setText("▶")
        if hasattr(self, 'animation_timer'):
            self.animation_timer.stop()
        for bar in self.waveform_bars:
            bar.setVisible(False)

    def _animate_waveform(self):
        for bar in self.waveform_bars:
            height = random.randint(4, 16)
            bar.setFixedHeight(height)

    def on_click(self):
        if self.filepath and os.path.exists(self.filepath):
            open_file(self.filepath)
        else:
            QMessageBox.critical(None, "Error", "File not found.")


class SmoothDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowOpacity(0.0)
        self.setStyleSheet(f"""
        QDialog {{
            background-color: {COLORS['chat_bg']};
            border-radius: 10px;
        }}
        """)
        self.main_layout = QVBoxLayout(self)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(180)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def showEvent(self, event):
        super().showEvent(event)
        self.anim.start()



class AudioRecorder(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.recording = True

    def run(self):
        try:
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            CHUNK = 1024
            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
            frames = []
            while self.recording:
                data = stream.read(CHUNK)
                frames.append(data)
            stream.stop_stream()
            stream.close()
            audio.terminate()
            wf = wave.open(self.filepath, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            self.finished.emit(self.filepath)
        except Exception as e:
            self.error.emit(str(e))

    def stop_recording(self):
        self.recording = False


class StarryBackground(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stars = []
        self.init_stars()
        self.timer = QTimer()
        self.timer.timeout.connect(self.twinkle)
        self.timer.start(900)
        self.setStyleSheet("background: transparent;")

    def init_stars(self):
        for _ in range(50):
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            size = random.uniform(0.6, 1.8)
            opacity = random.uniform(0.3, 0.9)
            self.stars.append({"x": x, "y": y, "size": size, "opacity": opacity})

    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QColor
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for star in self.stars:
            alpha = int(255 * star["opacity"])
            color = QColor(220, 230, 255, alpha)
            painter.setPen(color)
            painter.setBrush(color)
            painter.drawEllipse(
                int(star["x"]), int(star["y"]),
                int(star["size"]), int(star["size"])
            )

    def twinkle(self):
        for star in self.stars:
            if random.random() < 0.25:
                star["opacity"] = random.uniform(0.2, 0.9)
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.stars = []
        self.init_stars()

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(360, 180)
        self.setStyleSheet(f"""
        QDialog {{
            background-color: {COLORS['chat_bg']};
            color: {COLORS['text']};
        }}
        """)
        layout = QVBoxLayout(self)
        title = QLabel("Secure Messenger")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        desc = QLabel("Secure messaging with end-to-end encryption.\nMade with PyQt6.")
        desc.setFont(QFont("Segoe UI", 10))
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['button']};
            color: white;
            border-radius: 10px;
            padding: 5px;
        }}
        """)
        layout.addWidget(close_btn)


class SecureMessenger(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.peer = "userB" if username == "userA" else "userA"
        self.setWindowTitle(f"Secure Messenger – {self.username}")
        self.resize(700, 720)

        icon_path = os.path.join(ICONS_DIR, "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Crypto setup
        generate_rsa_keys(self.username)
        generate_rsa_keys(self.peer)
        self.private_key = load_private_path(self.username)
        self.peer_public = load_public_key(self.peer)
        self.aes_key = generate_aes_key()

        # Paths
        self.download_dir = get_user_download_dir(self.username)
        self.peer_dir = get_user_download_dir(self.peer)
        self.received_files = {}  # ✅ ONLY files from peer
        self.recorder = None
        self.recording = False
        self.msg_id_counter = 0

        # Audio playback
        self.current_audio_player = None
        self.current_audio_output = None
        self.current_audio_bubble = None

        # History
        self.history = HistoryManager(self.username)

        # UI setup
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Background
        self.bg_label = QLabel(self)
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.stackUnder(central)
        self.starry_bg = None
        self.load_background()

        # Chat area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(10)
        self._update_chat_margins()  # ✅ Safe: method defined before use
        self.scroll_area.setWidget(self.chat_widget)
        main_layout.addWidget(self.scroll_area)

        # Input area
        input_frame = QFrame()
        input_frame.setStyleSheet(f"""
        QFrame {{
            background-color: {COLORS['input_bg']};
            border-radius: 24px;
            padding: 6px;
            margin: 10px 14px 14px 14px;
            border: 1px solid {COLORS['border']};
        }}
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 0, 10, 0)
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Message...")
        self.entry.setFont(QFont("Segoe UI", 11))
        self.entry.setStyleSheet(f"color: {COLORS['text']}; background: transparent; border: none;")
        self.entry.returnPressed.connect(self.animate_send)
        input_layout.addWidget(self.entry)

        file_btn = QPushButton("📎")
        file_btn.setFixedSize(38, 38)
        file_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['input_bg']};
            border-radius: 19px;
            font-size: 16px;
            color: #a0c0ff;
        }}
        QPushButton:hover {{
            background-color: #3a4a6b;
        }}
        """)
        file_btn.clicked.connect(self.send_file)
        input_layout.addWidget(file_btn)

        self.record_btn = QPushButton("🎤")
        self.record_btn.setFixedSize(38, 38)
        self.record_btn.setStyleSheet(self.record_button_style(False))
        self.record_btn.clicked.connect(self.toggle_recording)
        input_layout.addWidget(self.record_btn)

        self.send_btn = QPushButton("➤")
        self.send_btn.setFixedSize(38, 38)
        self.send_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['button']};
            border-radius: 19px;
            font-size: 16px;
            color: white;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['button_hover']};
        }}
        """)
        self.send_btn.clicked.connect(self.animate_send)
        input_layout.addWidget(self.send_btn)

        main_layout.addWidget(input_frame)

        # Waveform
        self.waveform = WaveformWidget()
        self.waveform.setVisible(False)
        main_layout.addWidget(self.waveform, alignment=Qt.AlignmentFlag.AlignCenter)

        # Bottom bar
        bottom_layout = QHBoxLayout()
        self.status_indicator = StatusIndicator()
        files_btn = QPushButton("📁")
        files_btn.setFixedSize(28, 28)
        files_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['input_bg']};
            border-radius: 14px;
            font-size: 14px;
            color: #a0c0ff;
        }}
        QPushButton:hover {{
            background-color: {COLORS['button']};
        }}
        """)
        files_btn.clicked.connect(self.open_files_window)
        bottom_layout.addWidget(self.status_indicator)
        bottom_layout.addStretch()
        bottom_layout.addWidget(files_btn)
        main_layout.addLayout(bottom_layout)

        # Menu & history
        self.create_menu()
        self.load_history()
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.poll_messages)
        self.poll_timer.start(1000)

    def _update_chat_margins(self):
        width = self.width()
        margin = max(6, min(12, int(width * 0.02)))
        self.chat_layout.setContentsMargins(margin, 12, margin, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        if self.starry_bg:
            self.starry_bg.setGeometry(0, 0, self.width(), self.height())
        self._update_chat_margins()

    def create_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
        QMenuBar {{
            background-color: {COLORS['input_bg']};
            color: {COLORS['text']};
            border: none;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 4px 8px;
        }}
        QMenuBar::item:selected {{
            background: {COLORS['button']};
            border-radius: 4px;
        }}
        """)
        file_menu = menubar.addMenu("File")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        file_menu.addAction(about_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def load_background(self):
        valid_ext = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
        bg_files = [f for f in os.listdir(BACKGROUND_DIR) if f.lower().endswith(valid_ext)]
        if bg_files:
            path = os.path.join(BACKGROUND_DIR, random.choice(bg_files))
            self.bg_pixmap = QPixmap(path)
            self.update_background()
            self.bg_label.show()
            if self.starry_bg:
                self.starry_bg.hide()
        else:
            self.bg_pixmap = None
            self.bg_label.hide()
            if not self.starry_bg:
                self.starry_bg = StarryBackground(self)
                self.starry_bg.setGeometry(0, 0, self.width(), self.height())
                self.starry_bg.lower()
            else:
                self.starry_bg.show()
                self.starry_bg.setGeometry(0, 0, self.width(), self.height())

    def update_background(self):
        if hasattr(self, 'bg_pixmap') and self.bg_pixmap and not self.bg_pixmap.isNull():
            scaled = self.bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self.bg_label.setPixmap(scaled)
            self.bg_label.setGeometry(0, 0, self.width(), self.height())

    def record_button_style(self, active=False):
        color = "#ff6b8a" if active else "#3a4a6b"
        text_color = "white" if active else "#b0c0ff"
        return f"""
        QPushButton {{
            background-color: {color};
            border-radius: 19px;
            font-size: 16px;
            color: {text_color};
        }}
        QPushButton:hover {{
            background-color: {"#ff4d75" if active else "#455a80"};
        }}
        """

    def animate_send(self):
        self.send_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['button_hover']};
            border-radius: 19px;
            font-size: 16px;
            color: white;
            font-weight: bold;
        }}
        """)
        QTimer.singleShot(80, lambda: self.send_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {COLORS['button']};
            border-radius: 19px;
            font-size: 16px;
            color: white;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['button_hover']};
        }}
        """))
        self.send_message()

    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.record_btn.setText("⏹")
            self.record_btn.setStyleSheet(self.record_button_style(True))
            self.waveform.setVisible(True)
            self.waveform.start_animation()
            filepath = os.path.join(tempfile.gettempdir(), f"voice_msg_{int(time.time())}.wav")
            self.recorder = AudioRecorder(filepath)
            self.recorder.finished.connect(self.on_recording_finished)
            self.recorder.error.connect(self.on_recording_error)
            self.recorder.start()
        else:
            if self.recorder:
                self.recorder.stop_recording()
            self.recording = False

    def on_recording_finished(self, filepath):
        self.record_btn.setText("🎤")
        self.record_btn.setStyleSheet(self.record_button_style(False))
        self.waveform.stop_animation()
        self.waveform.setVisible(False)
        duration = get_audio_duration(filepath)
        filename = os.path.basename(filepath)
        notif_file = os.path.join(self.peer_dir, f"file_{self.username}_{int(time.time())}.json")
        with open(notif_file, "w") as f:
            json.dump({
                "from": self.username,
                "file": filename,
                "path": filepath,
                "time": get_current_time()
            }, f)
        self.add_message(FileBubble(filename, True, get_current_time(), filepath, duration, main_window=self), is_file=True)

    def on_recording_error(self, error_msg):
        self.recording = False
        self.record_btn.setText("🎤")
        self.record_btn.setStyleSheet(self.record_button_style(False))
        self.waveform.stop_animation()
        self.waveform.setVisible(False)
        self.status_indicator.show_error("Recording failed")

    def send_message(self):
        msg = self.entry.text().strip()
        if not msg: return
        self.status_indicator.show_encrypting()
        QTimer.singleShot(300, lambda: self._finish_send_message(msg))

    def _finish_send_message(self, msg):
        cipher = encrypt_message(self.aes_key, msg)
        sig = sign_message(self.private_key, msg)
        timestamp = get_current_time()
        payload = {"from": self.username, "cipher": cipher, "signature": sig, "time": timestamp}
        msg_file = os.path.join(self.peer_dir, f"msg_{self.username}_{int(time.time())}.json")
        with open(msg_file, "w") as f:
            json.dump(payload, f)
        self.entry.clear()
        msg_id = f"msg_{self.msg_id_counter}"
        self.msg_id_counter += 1
        self.history.save_message({
            "id": msg_id,
            "text": msg,
            "from": self.username,
            "time": timestamp
        })
        self.add_message(MessageBubble(msg, True, timestamp, msg_id), msg_id=msg_id)

    def send_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if not path: return
        filename = os.path.basename(path)
        duration = get_audio_duration(path) if path.lower().endswith(('.wav', '.mp3')) else ""
        notif_file = os.path.join(self.peer_dir, f"file_{self.username}_{int(time.time())}.json")
        with open(notif_file, "w") as f:
            json.dump({
                "from": self.username,
                "file": filename,
                "path": path,
                "time": get_current_time()
            }, f)
        self.add_message(FileBubble(filename, True, get_current_time(), path, duration, main_window=self), is_file=True)
        #  DO NOT add to received_files — this is a SENT file

    def add_message(self, bubble, msg_id=None, is_file=False):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        if bubble.is_self:
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addStretch()
        self.chat_layout.addWidget(container)
        if msg_id and not is_file:
            setattr(bubble, 'msg_id', msg_id)
            bubble.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            bubble.customContextMenuRequested.connect(lambda pos: self.show_reaction_menu(bubble, pos))
        if is_file and hasattr(bubble, 'main_window'):
            bubble.main_window = self
        bubble.setWindowOpacity(0.0)
        anim = QPropertyAnimation(bubble, b"windowOpacity")
        anim.setDuration(250)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def show_reaction_menu(self, bubble, pos):
        menu = QMenu(self)
        emojis = ["❤️", "😂", "✨", "👍", "😊", "😇", "😞"]
        for emoji in emojis:
            action = QAction(emoji, self)
            action.triggered.connect(lambda checked, e=emoji: self.react_to_message(bubble, e))
            menu.addAction(action)
        menu.exec(bubble.mapToGlobal(pos))

    def react_to_message(self, bubble, emoji):
        if hasattr(bubble, 'msg_id'):
            bubble.add_reaction(emoji, self.username)

    def load_history(self):
        for msg in self.history.messages:
            is_self = msg["from"] == self.username
            bubble = MessageBubble(msg["text"], is_self, msg["time"], msg.get("id", ""))
            self.add_message(bubble, msg_id=msg.get("id", ""))

    def poll_messages(self):
        try:
            for filename in os.listdir(self.download_dir):
                if not filename.endswith(".json"): continue
                filepath = os.path.join(self.download_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    timestamp = data.get("time", get_current_time())
                    if "file" in data:
                        # ✅ Only process files FROM PEER
                        if data["from"] == self.peer:
                            src = data["path"]
                            dest_file = data["file"]
                            dest_path = os.path.join(self.download_dir, dest_file)
                            try:
                                shutil.copy2(src, dest_path)
                            except:
                                self.add_message(MessageBubble("❌ File receive failed", False, timestamp), is_file=True)
                            else:
                                duration = get_audio_duration(dest_path) if dest_file.lower().endswith(('.wav', '.mp3')) else ""
                                bubble = FileBubble(dest_file, False, timestamp, dest_path, duration, main_window=self)
                                self.add_message(bubble, is_file=True)
                                # ONLY add peer-sent files to received_files
                                self.received_files[dest_file] = dest_path
                        # else: ignore files you sent — they appear in peer's folder
                    elif "cipher" in data:
                        self.status_indicator.show_verifying()
                        QTimer.singleShot(400, lambda d=data, t=timestamp: self._process_message(d, t))
                except:
                    pass
                finally:
                    try:
                        os.remove(filepath)
                    except:
                        pass
        except:
            pass

    def _process_message(self, data, timestamp):
        try:
            plaintext = decrypt_message(self.aes_key, data["cipher"])
            if verify_signature(load_public_key(data["from"]), plaintext, data["signature"]):
                msg_id = f"msg_{self.msg_id_counter}"
                self.msg_id_counter += 1
                self.history.save_message({
                    "id": msg_id,
                    "text": plaintext,
                    "from": data["from"],
                    "time": timestamp
                })
                bubble = MessageBubble(plaintext, False, timestamp, msg_id)
                self.add_message(bubble, msg_id=msg_id)
            else:
                self.add_message(MessageBubble("❌ Invalid signature!", False, timestamp))
                self.status_indicator.show_error("Invalid signature")
        except:
            self.add_message(MessageBubble("❌ Decryption failed!", False, timestamp))
            self.status_indicator.show_error("Decryption failed")

    def open_files_window(self):
        if not self.received_files:
            QMessageBox.information(self, "No Files", "No files received yet.")
            return
        dialog = SmoothDialog(self)
        dialog.setWindowTitle("Received Files")
        dialog.resize(340, 240)
        list_widget = QListWidget()
        list_widget.setFont(QFont("Segoe UI", 10))
        list_widget.setStyleSheet(f"color: {COLORS['text']}; background: {COLORS['chat_bg']}; border: none;")
        for fname in sorted(self.received_files):
            icon = get_file_icon(fname)
            duration = ""
            path = self.received_files.get(fname)
            if path and fname.lower().endswith(('.wav', '.mp3')):
                duration = " (" + get_audio_duration(path) + ")"
            list_widget.addItem(f"{icon} {fname}{duration}")
        dialog.main_layout.addWidget(list_widget)

        def on_double_click(item):
            parts = item.text().split(" ", 1)
            if len(parts) < 2: return
            fname = parts[1].split(" (")[0]
            path = self.received_files.get(fname)
            if path and os.path.exists(path):
                open_file(path)
            else:
                QMessageBox.critical(dialog, "Error", "File not found.")
        list_widget.itemDoubleClicked.connect(on_double_click)
        dialog.exec()

    # Audio playback
    def play_audio(self, filepath, bubble):
        self.stop_audio()
        self.current_audio_player = QMediaPlayer()
        self.current_audio_output = QAudioOutput()
        self.current_audio_player.setAudioOutput(self.current_audio_output)
        self.current_audio_player.setSource(QUrl.fromLocalFile(filepath))
        self.current_audio_player.playbackStateChanged.connect(
            lambda: self.on_playback_state_changed(bubble)
        )
        self.current_audio_player.errorOccurred.connect(
            lambda error, error_str: self.on_audio_error(error_str)
        )
        self.current_audio_player.play()
        self.current_audio_bubble = bubble
        bubble.start_waveform()

    def stop_audio(self):
        if self.current_audio_player:
            self.current_audio_player.stop()
            self.current_audio_player.deleteLater()
            self.current_audio_player = None
            self.current_audio_output = None
        if self.current_audio_bubble:
            self.current_audio_bubble.stop_waveform()
            self.current_audio_bubble = None

    def on_playback_state_changed(self, bubble):
        if self.current_audio_player and self.current_audio_player.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
            bubble.stop_waveform()

    def on_audio_error(self, error_str):
        QMessageBox.critical(self, "Audio Error", f"Failed to play audio:\n{error_str}")
        self.stop_audio()

    def closeEvent(self, event):
        if self.recording and self.recorder:
            self.recorder.stop_recording()
        self.stop_audio()
        event.accept()


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("userA", "userB"):
        print("Usage: python interface.py userA   OR   userB")
        sys.exit(1)
    app = QApplication(sys.argv)
    icon_path = os.path.join(ICONS_DIR, "app_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor(COLORS["bg"]))
    palette.setColor(QPalette.ColorRole.Base, QColor(COLORS["chat_bg"]))
    palette.setColor(QPalette.ColorRole.Text, QColor(COLORS["text"]))
    app.setPalette(palette)
    window = SecureMessenger(sys.argv[1])
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()