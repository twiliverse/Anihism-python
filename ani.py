import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTextEdit, QComboBox, QDialog, 
                             QProgressBar, QStackedWidget, QGraphicsOpacityEffect, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer, QUrl, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QFontDatabase
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class AnimatedButton(QPushButton):
    def __init__(self, text, hover_color):
        super().__init__(text)
        self.base_color = "#8E44AD"
        self.hover_color = hover_color
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.base_color};
                border: none;
                color: #ECF0F1;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
            }}
        """)

        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(5, 5)
        self.setGraphicsEffect(shadow)

    def enterEvent(self, event):
        self.animate(1.1)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.hover_color};
                border: none;
                color: #ECF0F1;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 10px;
            }}
        """)

    def leaveEvent(self, event):
        self.animate(1.0)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.base_color};
                border: none;
                color: #ECF0F1;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 10px;
            }}
        """)

    def animate(self, scale):
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(100)
        animation.setStartValue(self.geometry())
        center = self.geometry().center()
        new_width = int(self.width() * scale)
        new_height = int(self.height() * scale)
        animation.setEndValue(QRect(int(center.x() - new_width / 2), int(center.y() - new_height / 2), new_width, new_height))
        animation.setEasingCurve(QEasingCurve.OutBack)
        animation.start()
class FadeEffect(QGraphicsOpacityEffect):
    def __init__(self, duration=1000):
        super().__init__()
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

    def start(self):
        self.animation.start()

class ContributionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add to the Beliefs")
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Contribute to the Chaos")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #ECF0F1; font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.contribution_text = QTextEdit()
        self.contribution_text.setPlaceholderText("Share your profound confusion here...")
        self.contribution_text.setStyleSheet("""
            QTextEdit {
                background-color: #34495E;
                color: #ECF0F1;
                border: 2px solid #8E44AD;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.contribution_text)

        button_layout = QHBoxLayout()
        submit_button = AnimatedButton("Submit", "#2ECC71")
        cancel_button = AnimatedButton("Cancel", "#E74C3C")
        submit_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(submit_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
class AnishismGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anishism")
        self.setGeometry(100, 100, 800, 600)
        self.setup_font()
        self.setup_ui()

    def setup_font(self):
        # Load Gotham font (make sure the font file is in the same directory as the script)
        font_id = QFontDatabase.addApplicationFont("Gotham-Bold.otf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.gotham_font = QFont(font_family, 12)
            self.gotham_font_bold = QFont(font_family, 14, QFont.Bold)
        else:
            # Fallback to a sans-serif font if Gotham is not available
            self.gotham_font = QFont("Arial", 12)
            self.gotham_font_bold = QFont("Arial", 14, QFont.Bold)

    def setup_ui(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Set up background gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#2C3E50"))
        gradient.setColorAt(1, QColor("#1B2631"))
        palette = self.palette()
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        self.setup_loading_screen()
        self.setup_acceptance_screen()
        self.setup_main_screen()

        self.central_widget.setCurrentIndex(0)
        self.start_loading()

    def setup_loading_screen(self):
        loading_widget = QWidget()
        layout = QVBoxLayout(loading_widget)
        layout.addStretch()

        loading_label = QLabel("Initiating Anishism...")
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setFont(self.gotham_font_bold)
        loading_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(loading_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #8E44AD;
                border-radius: 5px;
                text-align: center;
                color: #ECF0F1;
                background-color: #34495E;
            }
            QProgressBar::chunk {
                background-color: #9B59B6;
            }
        """)
        layout.addWidget(self.progress_bar)

        layout.addStretch()
        self.central_widget.addWidget(loading_widget)

    def setup_acceptance_screen(self):
        acceptance_widget = QWidget()
        layout = QVBoxLayout(acceptance_widget)
        layout.addStretch()

        question_label = QLabel("Are you ready to embrace the delightful chaos of Anishism?")
        question_label.setAlignment(Qt.AlignCenter)
        question_label.setFont(self.gotham_font_bold)
        question_label.setStyleSheet("color: #ECF0F1;")
        question_label.setWordWrap(True)
        layout.addWidget(question_label)

        button_layout = QHBoxLayout()
        yes_button = AnimatedButton("I accept!", "#2ECC71")  # Green hover color
        no_button = AnimatedButton("I reject ", "#E74C3C")  # Red hover color
        yes_button.clicked.connect(self.accept_anishism)
        no_button.clicked.connect(self.reject_anishism)
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)
        layout.addLayout(button_layout)

        layout.addStretch()
        self.central_widget.addWidget(acceptance_widget)

    def setup_main_screen(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        title = QLabel("Welcome to the Realm of Anishism")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(self.gotham_font_bold)
        title.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(title)

        subtitle = QLabel("Where confusion reigns supreme!")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(self.gotham_font)
        subtitle.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(subtitle)

        principles_label = QLabel("Choose your path of bewilderment:")
        principles_label.setStyleSheet("color: #ECF0F1; font-size: 16px;")
        principles_label.setFont(self.gotham_font)
        layout.addWidget(principles_label)

        self.principles_combo = QComboBox()
        self.principles_combo.addItems([
            "The Holy Muddle",
            "Divine Procrastination",
            "Flexible Worship",
            "Open-Source Doctrine",
            "The Book of Random Edits",
            "The Prosperity Gospel",
            "Reincarnation as an Upgrade",
            "Literal Afterlife Directions",
            "No Need for Huge Temples",
            "Miracles on Demand"
            ])
        self.principles_combo.setStyleSheet("""
            QComboBox {
                background-color: #34495E;
                color: #ECF0F1;
                border: 2px solid #8E44AD;
                border-radius: 5px;
                padding: 5px;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 14px;
                height: 14px;
            }
        """)
        self.principles_combo.setFont(self.gotham_font)
        layout.addWidget(self.principles_combo)

        self.principle_explanation = QTextEdit()
        self.principle_explanation.setReadOnly(True)
        self.principle_explanation.setStyleSheet("""
            QTextEdit {
                background-color: #34495E;
                color: #ECF0F1;
                border: 2px solid #8E44AD;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        self.principle_explanation.setFont(self.gotham_font)
        layout.addWidget(self.principle_explanation)

        button_layout = QHBoxLayout()
        self.explain_button = AnimatedButton("Seek Enlightenment", "#3498DB")
        self.contribute_button = AnimatedButton("Add to the Beliefs", "#F39C12")
        self.procrastinate_button = AnimatedButton("Procrastinate", "#1ABC9C")
        
        self.explain_button.clicked.connect(self.explain_principle)
        self.contribute_button.clicked.connect(self.contribute)
        self.procrastinate_button.clicked.connect(self.procrastinate)
        
        button_layout.addWidget(self.explain_button)
        button_layout.addWidget(self.contribute_button)
        button_layout.addWidget(self.procrastinate_button)
        layout.addLayout(button_layout)

        self.central_widget.addWidget(main_widget)

    def start_loading(self):
        self.progress = 0
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.update_loading)
        self.loading_timer.start(30)

    def update_loading(self):
        self.progress += 1
        self.progress_bar.setValue(self.progress)
        if self.progress >= 100:
            self.loading_timer.stop()
            self.central_widget.setCurrentIndex(1)

    def accept_anishism(self):
        self.central_widget.setCurrentIndex(2)

    def reject_anishism(self):
        self.show_message("F u, now u lost ur free will!", 3000)
        QTimer.singleShot(3000, self.accept_anishism)

    def explain_principle(self):
        principle = self.principles_combo.currentText()
        explanations = {
            "The Holy Muddle": "Embrace the art of saying much while meaning little. Confuse yourself and others with circular logic and paradoxical statements. Remember, clarity is overrated!",
            "Divine Procrastination": "Why do today what you can put off until the heat death of the universe? In Anishism, deadlines are merely suggestions, and 'later' is always the best time.",
            "Flexible Worship": "Express your devotion through interpretive dance, meme creation, or intense staring contests with inanimate objects. The more absurd, the more divine!",
            "Open-Source Doctrine": "Don't like a tenet? Change it! Bored with a ritual? Rewrite it! In Anishism, your personal delusions are just as valid as ancient wisdom.",
            "The Book of Random Edits": "Our sacred text is a collaborative masterpiece of confusion. Add your own contradictory chapter today and watch as others try to make sense of it!",
            "The Prosperity Gospel": "Forget about material wealth! Instead of gold coins or fancy cars, Anishism guarantees you'll receive mild amusement... which is practically the same thing.",
            "Reincarnation as an Upgrade": "Come back to life, but with a twist! In Anishism, reincarnation might turn you into a secondhand stapler or a deflated bouncy castle. It's Ctrl+Z, but with a downgrade.",
            "Literal Afterlife Directions": "No roadmaps to the afterlife here. We give you vague spiritual coordinates like 'Somewhere Over Yonder' and wish you luck finding it!",
            "No Need for Huge Temples": "Why build huge religious monuments when true revelations happen in AnishHub, your hamster's cage, or even your messy backlit keyboard? Holiness is everywhere!",
            "Miracles on Demand": "Every little improvement in your day is a miracle. Your phone didn’t die during a Netflix binge? Divine intervention! Found parking? That’s the universe smiling down on you."
        }
        self.principle_explanation.setText(explanations.get(principle, "Error 404: Wisdom not found (or we forgot where we put it)"))

    def contribute(self):
        dialog = ContributionDialog(self)
        if dialog.exec_():
            contribution = dialog.contribution_text.toPlainText()
            if contribution:
                self.show_message("Processing your insight...", 2000)
                QTimer.singleShot(2000, lambda: self.show_message("You have been carefully ignored!", 3000))

    def procrastinate(self):
        self.show_message("procrastinating...", 2000)
        QTimer.singleShot(2000, lambda: self.show_message("Procrastination successful", 3000))

    def show_message(self, message, duration):
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            background-color: #34495E;
            color: #ECF0F1;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        """)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setFont(self.gotham_font)
        
        self.statusBar().addWidget(message_label, 1)
        QTimer.singleShot(duration, lambda: self.statusBar().removeWidget(message_label))
    def fade_in_widget(self, index):
        self.central_widget.setCurrentIndex(index)
        current_widget = self.central_widget.currentWidget()
        fade_effect = FadeEffect()
        current_widget.setGraphicsEffect(fade_effect)
        fade_effect.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnishismGUI()
    window.show()
    sys.exit(app.exec_())
