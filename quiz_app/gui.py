from PyQt5.QtWidgets import (
    QComboBox,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QButtonGroup,
    QMessageBox,
    QSizePolicy,
    QSpacerItem,
)
from PyQt5.QtCore import Qt
import json
import os
from db import QuizDB


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Game")
        self.setMinimumSize(600, 450)  # 150% larger
        self.db = QuizDB()
        self.all_questions = self.db.load_questions()
        self.difficulty = None
        self.questions = []
        self.current = 0
        self.score = 0
        self.attempts = 0
        self.high_score = self.db.get_high_score()
        self.init_ui()
        self.show_difficulty_selection()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_difficulty_selection(self):
        self.clear_layout()
        title = QLabel("<h1 style='color:#2d89ef;'>Quiz Game</h1>")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)
        desc = QLabel("<p style='font-size:16px;'>Select difficulty to begin:</p>")
        desc.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(desc)
        self.diff_combo = QComboBox()
        self.diff_combo.addItems(["Easy", "Medium", "Hard"])
        self.diff_combo.setStyleSheet("font-size:16px;padding:6px;")
        self.layout.addWidget(self.diff_combo, alignment=Qt.AlignCenter)
        start_btn = QPushButton("Start Quiz")
        start_btn.setStyleSheet(
            "background:#2d89ef;color:white;font-size:16px;padding:8px 24px;border-radius:8px;"
        )
        start_btn.clicked.connect(self.start_quiz)
        self.layout.addWidget(start_btn, alignment=Qt.AlignCenter)
        self.layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def start_quiz(self):
        self.difficulty = self.diff_combo.currentText().lower()
        self.questions = [
            q for q in self.all_questions if q["difficulty"] == self.difficulty
        ]
        self.current = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self.clear_layout()
        if self.current >= len(self.questions):
            self.finish_quiz()
            return
        q = self.questions[self.current]
        q_label = QLabel(f"<b>Q{self.current+1}:</b> {q['question']}")
        q_label.setWordWrap(True)
        q_label.setStyleSheet("font-size:27px;margin-bottom:18px;")
        self.layout.addWidget(q_label)
        self.button_group = QButtonGroup(self)
        self.option_buttons = []
        for i, opt in enumerate(q["options"]):
            btn = QPushButton(opt)
            btn.setCheckable(True)
            btn.setStyleSheet(
                "font-size:24px;padding:12px 24px;margin:8px;border-radius:9px;"
            )
            self.layout.addWidget(btn)
            self.button_group.addButton(btn, i)
            self.option_buttons.append(btn)
        self.button_group.setExclusive(True)
        # Add submit button only once
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setStyleSheet(
            "background:#2d89ef;color:white;font-size:24px;padding:12px 36px;border-radius:12px;margin-top:16px;"
        )
        self.submit_btn.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_btn)
        # Add score and stats labels only once
        self.score_label = QLabel(f"<b>Score:</b> {self.score}")
        self.score_label.setStyleSheet("font-size:22px;margin-top:16px;")
        self.layout.addWidget(self.score_label)
        self.stats_label = QLabel(
            f"<b>High Score:</b> {self.high_score} | <b>Attempts:</b> {self.db.get_attempts()}"
        )
        self.stats_label.setStyleSheet("font-size:20px;color:#666;")
        self.layout.addWidget(self.stats_label)

    def check_answer(self):
        selected = None
        for btn in self.option_buttons:
            if btn.isChecked():
                selected = btn.text()
        if selected is None:
            QMessageBox.warning(self, "No selection", "Please select an answer.")
            return
        correct = self.questions[self.current]["answer"]
        if selected == correct:
            self.score += 1
            QMessageBox.information(self, "Correct!", "That's the right answer!")
        else:
            QMessageBox.information(
                self, "Incorrect", f"Wrong answer! Correct: {correct}"
            )
        self.current += 1
        self.show_question()

        def check_answer(self):
            selected = None
            for btn in self.option_buttons:
                if btn.isChecked():
                    selected = btn.text()
            if selected is None:
                QMessageBox.warning(self, "No selection", "Please select an answer.")
                return
            correct = self.questions[self.current]["answer"]
            if selected == correct:
                self.score += 1
                QMessageBox.information(
                    self, "Correct!", "That's the right answer!", QMessageBox.Ok
                )
            else:
                QMessageBox.information(
                    self,
                    "Incorrect",
                    f"Wrong answer! Correct: {correct}",
                    QMessageBox.Ok,
                )
            self.current += 1
            self.show_question()

    def finish_quiz(self):
        self.db.save_attempt(self.score)
        if self.score > self.high_score:
            self.high_score = self.score
            self.db.save_high_score(self.high_score)
        QMessageBox.information(
            self,
            "Quiz Finished",
            f"Your score: {self.score}\nHigh Score: {self.high_score}",
        )
        self.close()

        def finish_quiz(self):
            self.db.save_attempt(self.score)
            if self.score > self.high_score:
                self.high_score = self.score
                self.db.save_high_score(self.high_score)
            msg = QMessageBox(self)
            msg.setWindowTitle("Quiz Finished")
            msg.setText(
                f"<h2>Quiz Finished!</h2><p>Your score: <b>{self.score}</b><br>High Score: <b>{self.high_score}</b></p>"
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.show_difficulty_selection()
