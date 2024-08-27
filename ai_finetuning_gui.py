import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QPushButton, QComboBox, 
                             QStackedWidget, QMessageBox, QListWidget,
                             QGraphicsDropShadowEffect, QFrame, QSplitter)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QBrush, QPainter
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QRect, QTimer

class ModernButton(QPushButton):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.darker(color, 120)};
            }}
            QPushButton:pressed {{
                background-color: {self.darker(color, 140)};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)

    def darker(self, color, factor=150):
        c = QColor(color)
        c.setRed(max(0, min(255, c.red() * factor // 100)))
        c.setGreen(max(0, min(255, c.green() * factor // 100)))
        c.setBlue(max(0, min(255, c.blue() * factor // 100)))
        return c.name()

class FineTuningGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.dataset = []
        self.turns = []
        self.saved_system_prompt = ""
        self.unsaved_changes = False
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1A202C;
                color: #E2E8F0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTextEdit, QComboBox, QListWidget {
                border: 2px solid #4A5568;
                border-radius: 5px;
                padding: 5px;
                background-color: #2D3748;
                color: #E2E8F0;
            }
            QLabel {
                color: #81E6D9;
                font-weight: bold;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #4299E1;
                width: 30px;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow_light.png);
                width: 16px;
                height: 16px;
            }
        """)

        main_layout = QHBoxLayout()
        
        # Left panel for input
        left_panel = QVBoxLayout()
        
        # Format selection
        format_layout = QHBoxLayout()
        format_label = QLabel("Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Normal", "Multi-turn"])
        self.format_combo.currentIndexChanged.connect(self.toggle_format)
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        left_panel.addLayout(format_layout)
        
        # Stacked widget for input fields
        self.input_stack = QStackedWidget()
        self.normal_input = self.create_normal_input()
        self.multi_turn_input = self.create_multi_turn_input()
        self.input_stack.addWidget(self.normal_input)
        self.input_stack.addWidget(self.multi_turn_input)
        left_panel.addWidget(self.input_stack)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = ModernButton("Add Conversation", "#4299E1")
        self.add_button.clicked.connect(self.add_conversation)
        button_layout.addWidget(self.add_button)
        
        self.clear_button = ModernButton("Clear Inputs", "#ED8936")
        self.clear_button.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.clear_button)
        
        left_panel.addLayout(button_layout)
        
        # Right panel for dataset display and actions
        right_panel = QVBoxLayout()
        
        # Dataset display
        self.dataset_list = QListWidget()
        self.dataset_list.itemDoubleClicked.connect(self.edit_conversation)
        right_panel.addWidget(QLabel("Current Dataset"))
        right_panel.addWidget(self.dataset_list)
        
        # Dataset actions
        dataset_actions = QHBoxLayout()
        self.save_button = ModernButton("Save Dataset", "#48BB78")
        self.save_button.clicked.connect(self.save_dataset)
        dataset_actions.addWidget(self.save_button)
        
        self.clear_dataset_button = ModernButton("Clear Dataset", "#F56565")
        self.clear_dataset_button.clicked.connect(self.clear_dataset)
        dataset_actions.addWidget(self.clear_dataset_button)
        
        right_panel.addLayout(dataset_actions)
        
        # Conversation counter
        self.conversation_counter = QLabel("Conversations: 0")
        self.conversation_counter.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(self.conversation_counter)
        
        # Add panels to main layout
        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        main_layout.addWidget(splitter)
        
        self.setLayout(main_layout)
        self.setWindowTitle('AI Fine-tuning GUI')
        self.resize(800, 600)
        self.show()

    def create_normal_input(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.system_input = self.create_labeled_text_edit("System message:")
        layout.addWidget(self.system_input)
        
        self.user_input = self.create_labeled_text_edit("User message:")
        layout.addWidget(self.user_input)
        
        self.assistant_input = self.create_labeled_text_edit("Assistant message:")
        layout.addWidget(self.assistant_input)
        
        widget.setLayout(layout)
        return widget

    def create_multi_turn_input(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.multi_system_input = self.create_labeled_text_edit("System message:")
        layout.addWidget(self.multi_system_input)
        
        self.multi_user_input = self.create_labeled_text_edit("User message:")
        layout.addWidget(self.multi_user_input)
        
        self.multi_assistant_input = self.create_labeled_text_edit("Assistant message:")
        layout.addWidget(self.multi_assistant_input)
        
        self.weight_input = self.create_labeled_text_edit("Weight (0 or 1):")
        layout.addWidget(self.weight_input)
        
        self.add_turn_button = ModernButton("Add Turn", "#9F7AEA")
        self.add_turn_button.clicked.connect(self.add_turn)
        layout.addWidget(self.add_turn_button)
        
        widget.setLayout(layout)
        return widget

    def create_labeled_text_edit(self, label):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(label))
        text_edit = QTextEdit()
        text_edit.setMaximumHeight(100)
        layout.addWidget(text_edit)
        widget.setLayout(layout)
        return widget

    def toggle_format(self):
        self.input_stack.setCurrentIndex(self.format_combo.currentIndex())

    def add_turn(self):
        turn = {
            "user": self.create_labeled_text_edit("User message:"),
            "assistant": self.create_labeled_text_edit("Assistant message:"),
            "weight": self.create_labeled_text_edit("Weight (0 or 1):")
        }
        self.turns.append(turn)
        layout = self.multi_turn_input.layout()
        for widget in turn.values():
            layout.insertWidget(layout.count() - 1, widget)

    def add_conversation(self):
        try:
            conversation = {"messages": []}
            if self.format_combo.currentIndex() == 0:  # Normal format
                system_msg = self.system_input.findChild(QTextEdit).toPlainText()
                user_msg = self.user_input.findChild(QTextEdit).toPlainText()
                assistant_msg = self.assistant_input.findChild(QTextEdit).toPlainText()
            else:  # Multi-turn format
                system_msg = self.multi_system_input.findChild(QTextEdit).toPlainText()
                user_msg = self.multi_user_input.findChild(QTextEdit).toPlainText()
                assistant_msg = self.multi_assistant_input.findChild(QTextEdit).toPlainText()
                weight = self.validate_weight(self.weight_input.findChild(QTextEdit).toPlainText())
            
            conversation["messages"].append({"role": "system", "content": system_msg})
            conversation["messages"].append({"role": "user", "content": user_msg})
            conversation["messages"].append({"role": "assistant", "content": assistant_msg})
            
            if self.format_combo.currentIndex() == 1:
                conversation["messages"][-1]["weight"] = weight
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
            self.update_conversation_counter()
            self.show_status("Conversation added successfully", 3000)
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
        reply = QMessageBox.question(self, "Edit Conversation", 
                                     "Do you want to remove this conversation?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.dataset[index]
            self.update_dataset_display()
            self.update_conversation_counter()
            self.show_status("Conversation removed", 3000)

    def save_conversation(self, conversation):
        try:
            with open('fine_tuning_dataset.jsonl', 'a') as f:
                f.write(json.dumps(conversation) + '\n')
        except IOError:
            QMessageBox.critical(self, "Error", "Failed to save the conversation.")
            self.unsaved_changes = True

    def save_dataset(self):
        try:
            with open('fine_tuning_dataset.jsonl', 'w') as f: 
                for item in self.dataset:
                    f.write(json.dumps(item) + '\n')
            self.unsaved_changes = False
            self.show_status("Dataset saved successfully", 3000)
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
            self.show_status("Dataset cleared", 3000)

    def clear_inputs(self):
        for widget in [self.system_input, self.user_input, self.assistant_input,
                       self.multi_system_input, self.multi_user_input, self.multi_assistant_input,
                       self.weight_input]:
            widget.findChild(QTextEdit).clear()
        for turn in self.turns:
            for widget in turn.values():
                self.multi_turn_input.layout().removeWidget(widget)
                widget.deleteLater()
        self.turns.clear()
        self.show_status("Inputs cleared", 3000)

    def show_status(self, message, duration):
        status_label = QLabel(message)
        status_label.setStyleSheet("""
            background-color: #4299E1;
            color: white;
            padding: 10px;
            border-radius: 5px;
        """)
        status_label.setAlignment(Qt.AlignCenter)
        
        self.layout().addWidget(status_label)
        
        QTimer.singleShot(duration, lambda: self.layout().removeWidget(status_label))
        QTimer.singleShot(duration, status_label.deleteLater)

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
