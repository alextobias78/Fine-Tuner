import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QPushButton, QComboBox, 
                             QGroupBox, QMessageBox, QScrollArea, QListWidget,
                             QStatusBar, QGraphicsDropShadowEffect, QFrame)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QBrush, QPainter
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QRect

class FineTuningGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.dataset = []
        self.turns = []
        self.saved_system_prompt = ""
        self.unsaved_changes = False
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setStyleSheet("""
            QWidget {
                background-color: #1A202C;
                color: #E2E8F0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                border: 2px solid #2D3748;
                border-radius: 12px;
                margin-top: 1ex;
                background-color: #2D3748;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #81E6D9;
                font-weight: bold;
            }
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4299E1, stop:1 #3182CE);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3182CE, stop:1 #2B6CB0);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2B6CB0, stop:1 #2C5282);
            }
            QTextEdit, QComboBox, QListWidget {
                border: 2px solid #4A5568;
                border-radius: 8px;
                padding: 8px;
                background-color: #2D3748;
                color: #E2E8F0;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #4299E1;
                width: 30px;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow_light.png);
                width: 16px;
                height: 16px;
            }
            QScrollBar:vertical {
                border: none;
                background: #4A5568;
                width: 12px;
                margin: 0px 0px 0px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #718096;
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QStatusBar {
                background-color: #2D3748;
                color: #E2E8F0;
            }
        """)
        
        # Custom frame with gradient background
        class GradientFrame(QFrame):
            def paintEvent(self, event):
                painter = QPainter(self)
                gradient = QLinearGradient(0, 0, self.width(), self.height())
                gradient.setColorAt(0, QColor("#1A202C"))
                gradient.setColorAt(1, QColor("#2D3748"))
                painter.fillRect(self.rect(), QBrush(gradient))

        self.setAutoFillBackground(True)
        gradient_frame = GradientFrame(self)
        gradient_frame.setGeometry(self.rect())
        
        # Add glow effect to buttons
        for button in self.findChildren(QPushButton):
            glow = QGraphicsDropShadowEffect(self)
            glow.setBlurRadius(15)
            glow.setColor(QColor(66, 153, 225, 150))
            glow.setOffset(0, 0)
            button.setGraphicsEffect(glow)

        # Format selection
        format_group = QGroupBox("Format")
        format_layout = QVBoxLayout()
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Normal", "Multi-turn"])
        self.format_combo.currentIndexChanged.connect(self.toggle_format)
        format_layout.addWidget(self.format_combo)
        format_group.setLayout(format_layout)
        main_layout.addWidget(format_group)

        # Scrollable input area
        input_scroll = QScrollArea()
        input_scroll.setWidgetResizable(True)
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)

        # Input fields
        input_group = QGroupBox("Conversation Input")
        
        self.system_input = self.create_labeled_text_edit("System message:")
        input_layout.addWidget(self.system_input)

        system_prompt_layout = QHBoxLayout()
        self.save_system_prompt_button = QPushButton("Save System Prompt")
        self.save_system_prompt_button.clicked.connect(self.save_system_prompt)
        system_prompt_layout.addWidget(self.save_system_prompt_button)
        self.clear_system_prompt_button = QPushButton("Clear Saved Prompt")
        self.clear_system_prompt_button.clicked.connect(self.clear_system_prompt)
        system_prompt_layout.addWidget(self.clear_system_prompt_button)
        input_layout.addLayout(system_prompt_layout)

        self.user_input = self.create_labeled_text_edit("User message:")
        input_layout.addWidget(self.user_input)

        self.assistant_input = self.create_labeled_text_edit("Assistant message:")
        input_layout.addWidget(self.assistant_input)

        self.weight_input = self.create_labeled_text_edit("Weight (0 or 1):")
        self.weight_input.setVisible(False)
        input_layout.addWidget(self.weight_input)

        self.add_turn_button = QPushButton("Add Turn")
        self.add_turn_button.clicked.connect(self.add_turn)
        self.add_turn_button.setVisible(False)
        input_layout.addWidget(self.add_turn_button)

        input_group.setLayout(input_layout)
        input_scroll.setWidget(input_group)
        main_layout.addWidget(input_scroll)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        self.add_button = QPushButton("Add Conversation")
        self.add_button.clicked.connect(self.add_conversation)
        button_layout.addWidget(self.add_button)

        self.save_button = QPushButton("Save Dataset")
        self.save_button.clicked.connect(self.save_dataset)
        button_layout.addWidget(self.save_button)

        self.clear_dataset_button = QPushButton("Clear Dataset")
        self.clear_dataset_button.clicked.connect(self.clear_dataset)
        button_layout.addWidget(self.clear_dataset_button)
        button_layout.addStretch(1)

        main_layout.addLayout(button_layout)

        # Dataset display
        display_group = QGroupBox("Current Dataset")
        display_layout = QVBoxLayout()
        self.dataset_list = QListWidget()
        self.dataset_list.setMaximumHeight(150)
        self.dataset_list.itemDoubleClicked.connect(self.edit_conversation)
        display_layout.addWidget(self.dataset_list)
        display_group.setLayout(display_layout)

        main_layout.addWidget(display_group)

        # Add status bar
        self.status_bar = QStatusBar()
        main_layout.addWidget(self.status_bar)

        # Add conversation counter
        self.conversation_counter = QLabel("Conversations: 0")
        self.conversation_counter.setStyleSheet("color: #81E6D9; font-weight: bold; font-size: 16px;")
        main_layout.addWidget(self.conversation_counter)

        self.setLayout(main_layout)
        self.setWindowTitle('AI Fine-tuning GUI')
        self.resize(600, 800)
        self.show()

    def create_labeled_text_edit(self, label):
        group = QGroupBox(label)
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setMaximumHeight(100)
        layout.addWidget(text_edit)
        group.setLayout(layout)
        
        # Add animation to the text edit
        self.add_focus_animation(text_edit)
        
        return group

    def add_focus_animation(self, widget):
        def on_focus_in():
            animation = QPropertyAnimation(widget, b"minimumHeight")
            animation.setDuration(200)
            animation.setStartValue(widget.height())
            animation.setEndValue(widget.height() + 20)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            animation.start()

        def on_focus_out():
            animation = QPropertyAnimation(widget, b"minimumHeight")
            animation.setDuration(200)
            animation.setStartValue(widget.height())
            animation.setEndValue(widget.height() - 20)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            animation.start()

        widget.focusInEvent = lambda e: on_focus_in()
        widget.focusOutEvent = lambda e: on_focus_out()

    def toggle_format(self):
        is_multi_turn = self.format_combo.currentText() == "Multi-turn"
        self.weight_input.setVisible(is_multi_turn)
        self.add_turn_button.setVisible(is_multi_turn)

    def add_turn(self):
        turn = {
            "user": self.create_labeled_text_edit("User message:"),
            "assistant": self.create_labeled_text_edit("Assistant message:"),
            "weight": self.create_labeled_text_edit("Weight (0 or 1):")
        }
        self.turns.append(turn)
        for widget in turn.values():
            self.layout().insertWidget(self.layout().count() - 2, widget)

    def save_system_prompt(self):
        self.saved_system_prompt = self.system_input.findChild(QTextEdit).toPlainText()
        QMessageBox.information(self, "Success", "System prompt saved successfully.")

    def clear_system_prompt(self):
        self.saved_system_prompt = ""
        self.system_input.findChild(QTextEdit).clear()
        QMessageBox.information(self, "Success", "Saved system prompt cleared.")

    def add_conversation(self):
        try:
            conversation = {"messages": []}
            system_msg = self.saved_system_prompt or self.system_input.findChild(QTextEdit).toPlainText()
            conversation["messages"].append({"role": "system", "content": system_msg})

            if self.format_combo.currentText() == "Normal":
                user_msg = self.user_input.findChild(QTextEdit).toPlainText()
                assistant_msg = self.assistant_input.findChild(QTextEdit).toPlainText()
                conversation["messages"].extend([
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": assistant_msg}
                ])
            else:
                user_msg = self.user_input.findChild(QTextEdit).toPlainText()
                assistant_msg = self.assistant_input.findChild(QTextEdit).toPlainText()
                weight = self.validate_weight(self.weight_input.findChild(QTextEdit).toPlainText())
                conversation["messages"].extend([
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": assistant_msg, "weight": weight}
                ])
                for turn in self.turns:
                    user_msg = turn["user"].findChild(QTextEdit).toPlainText()
                    assistant_msg = turn["assistant"].findChild(QTextEdit).toPlainText()
                    weight = self.validate_weight(turn["weight"].findChild(QTextEdit).toPlainText())
                    conversation["messages"].extend([
                        {"role": "user", "content": user_msg},
                        {"role": "assistant", "content": assistant_msg, "weight": weight}
                    ])

            self.dataset.append(conversation)
            self.save_conversation(conversation)
            self.update_dataset_display()
            self.clear_inputs()
            self.status_bar.showMessage("Conversation added and saved successfully", 3000)
            self.update_conversation_counter()
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))

    def validate_weight(self, weight_str):
        try:
            weight = int(weight_str)
            if weight not in [0, 1]:
                raise ValueError("Weight must be 0 or 1")
            return weight
        except ValueError:
            raise ValueError("Invalid weight. Please enter 0 or 1.")

    def update_dataset_display(self):
        self.dataset_list.clear()
        for i, conversation in enumerate(self.dataset):
            self.dataset_list.addItem(f"Conversation {i+1}")

    def edit_conversation(self, item):
        index = self.dataset_list.row(item)
        conversation = self.dataset[index]
        # Implement editing logic here
        # For simplicity, we'll just remove the conversation
        reply = QMessageBox.question(self, "Edit Conversation", 
                                     "Do you want to remove this conversation?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.dataset[index]
            self.update_dataset_display()

    def save_conversation(self, conversation):
        try:
            with open('fine_tuning_dataset.jsonl', 'a') as f:
                f.write(json.dumps(conversation) + '\n')
        except IOError:
            QMessageBox.critical(self, "Error", "Failed to save the conversation.")
            self.unsaved_changes = True

    def save_dataset(self):
        if not self.unsaved_changes:
            self.status_bar.showMessage("No new changes to save", 3000)
            return

        try:
            with open('fine_tuning_dataset.jsonl', 'w') as f:
                for item in self.dataset:
                    f.write(json.dumps(item) + '\n')
            self.unsaved_changes = False
            self.status_bar.showMessage("Dataset saved successfully", 3000)
        except IOError:
            QMessageBox.critical(self, "Error", "Failed to save the dataset.")

    def update_conversation_counter(self):
        self.conversation_counter.setText(f"Conversations: {len(self.dataset)}")

    def clear_dataset(self):
        reply = QMessageBox.question(self, "Clear Dataset", 
                                     "Are you sure you want to clear the entire dataset?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.dataset.clear()
            self.update_dataset_display()
            self.update_conversation_counter()
            open('fine_tuning_dataset.jsonl', 'w').close()  # Clear the file
            self.status_bar.showMessage("Dataset cleared", 3000)

    def clear_inputs(self):
        if not self.saved_system_prompt:
            self.system_input.findChild(QTextEdit).clear()
        self.user_input.findChild(QTextEdit).clear()
        self.assistant_input.findChild(QTextEdit).clear()
        self.weight_input.findChild(QTextEdit).clear()
        for turn in self.turns:
            for widget in turn.values():
                self.layout().removeWidget(widget)
                widget.deleteLater()
        self.turns.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(26, 32, 44))
    dark_palette.setColor(QPalette.WindowText, QColor(226, 232, 240))
    dark_palette.setColor(QPalette.Base, QColor(45, 55, 72))
    dark_palette.setColor(QPalette.AlternateBase, QColor(74, 85, 104))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(26, 32, 44))
    dark_palette.setColor(QPalette.ToolTipText, QColor(226, 232, 240))
    dark_palette.setColor(QPalette.Text, QColor(226, 232, 240))
    dark_palette.setColor(QPalette.Button, QColor(66, 153, 225))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(129, 230, 217))
    dark_palette.setColor(QPalette.Highlight, QColor(66, 153, 225))
    dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(dark_palette)
    
    # Set app icon
    app.setWindowIcon(QIcon('app_icon_dark.png'))
    
    ex = FineTuningGUI()
    sys.exit(app.exec_())
