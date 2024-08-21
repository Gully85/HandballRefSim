# Python script file to read the german localization of the rule-questions
# This requires the input "Fragenkatalog" pdf file as parameter (or uses default in the main folder)
# This will create or update localizations/german.csv

# This assumes that questions and their answers are not broken over page boundaries

from pypdf import PdfReader
import re
from enum import Enum, auto

from record import Record

sourcefile: str = "Fragenkatalog_Grundausbildung_mit_Loesungen_Stand_01062024.pdf"
headerpages_to_skip: int = 2

# Index of the first page with solutions. This is set by sweeping the input document before the actual parsing begins
first_page_with_solutions: int

# Regex explanation: question_marker should match the first line of each question. Running number (no leading zeros,
# but multiple digits are allowed), a dot, one space, then an uppercase letter, then anything.
# Questions can be broken over multiple lines, so we grab every line until one matches answer_marker.
question_marker: str = r"[1-9]\d*\. [A-Z].*"

# answer lines always start with a lowercase letter, then ")", then a space, then anything.
# Answers can also be broken over multiple lines. This marker only matches the first line of an answer.
answer_marker: str = r"[a-z]\) .*"


class ParserState(Enum):
    # outside of any question or answer, e.g. table-of-contents or page-header/-footer
    NEUTRAL = auto()

    # between the first line of a question, and the first answer-option
    QUESTION = auto()

    # behind the first line of the first answer-option
    ANSWER = auto()


def main() -> None:
    reader: PdfReader = PdfReader(sourcefile)

    print(f"Total pages in inputfile: {len(reader.pages)}")

    results: list[Record] = []
    current_record: Record
    current_index: int = 0

    sweep_for_solutions(reader)

    for page in reader.pages[headerpages_to_skip:]:
        fulltext: str = page.extract_text()
        lines: list[str] = fulltext.splitlines()
        state: ParserState = ParserState.NEUTRAL

        for line in lines:
            if state == ParserState.NEUTRAL:
                if not re.match(question_marker, line):
                    continue
                state = ParserState.QUESTION
                current_record = Record(question=line)
                current_index = int(line.split(". ")[0])

            elif state == ParserState.QUESTION:
                if not re.match(answer_marker, line):
                    current_record.add_question_line(line)
                else:
                    state = ParserState.ANSWER
                    current_record.add_new_answer(line)

            elif state == ParserState.ANSWER:
                if re.match(answer_marker, line):
                    current_record.add_new_answer(line)
                elif not re.match(question_marker, line):
                    current_record.add_new_line_to_answer(line)
                else:
                    # finalize last record, then start a new one with the question line
                    find_and_add_correct_answers(current_index, current_record)
                    results.append(current_record)

                    state = ParserState.QUESTION
                    current_record = Record(question=line)
                    current_index = int(line.split(". ")[0])

        # during testing, only use the first not-skipped page
        break

    # print(reader.pages[8].extract_text())


def sweep_for_solutions(reader: PdfReader) -> None:
    """Look for the pages where the correct answers are defined. Sets the module-wide variable first_page_with_solutions"""

    # The Solutions page starts with a date-timestamp, and then the keyword "Lösungen" (which for some reason ends up in the
    # same line when reading with PdfReader and splitting with str.splitlines(). )
    solutions_marker: str = r"\d\d\.\d\d\.\d{4}\s+Lösungen"

    # The first solutions-page should start with a page-number header, then the big keyword "Lösungen"
    for pagenumber, page in enumerate(reader.pages):
        print("\n")
        fulltext = page.extract_text()
        for line in fulltext.splitlines():
            if re.match(solutions_marker, line):
                print(line)

    global first_page_with_solutions
    first_page_with_solutions = pagenumber


def find_and_add_correct_answers(int, Record) -> None:
    pass


if __name__ == "__main__":
    main()
