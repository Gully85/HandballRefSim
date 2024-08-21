# Python class file to hold the Record class
# This is a container class to hold a rule question,
# possible answer options, and which answers are correct

from dataclasses import dataclass, field


@dataclass
class Record:
    question: str = ""
    answers: list[str] = field(default_factory=[])
    correct_answers: list[bool] = field(default_factory=[])

    def add_question_line(self, line: str) -> None:
        """Add or append one line to this record's question. If this is the first line to be added,
        remove the numbering."""
        if self.question == "":
            line_without_numbering: str = line.split(". ")[1]
            self.question = line_without_numbering
            return
        # If there is already a line, handle empty space.
        self.question = self.question.rstrip() + " " + line.lstrip()

    def add_new_answer(self, line: str) -> None:
        """Add a new answer option."""
        self.answers.append(line)

    def add_new_line_to_answer(self, line: str) -> None:
        """Append given line to the last answer"""
        last_answer: str = self.answers[-1]
        if last_answer == "":
            raise ValueError(
                f"Found line {line} without preceding answer-option. Question was: {self.question}"
            )
        self.answers[-1] = last_answer.rstrip() + " " + line.lstrip()
