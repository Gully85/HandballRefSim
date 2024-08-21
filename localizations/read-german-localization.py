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

# Regex explanation: question_marker should match the first line of each question. Running number (no leading zeros,
# but multiple digits are allowed), a dot, one space, then an uppercase letter, then anything.
# Questions can be broken over multiple lines, so we grab every line until one matches answer_marker.
question_marker: str = r"[1-9]\d*\. [A-Z].*"

# answer lines always start with a lowercase letter, then ")", then a space, then anything.
# Answers can also be broken over multiple lines. This marker only matches the first line of an answer.
answer_marker: str = r"[a-z]\) .*"


class ParserState(Enum):
    NEUTRAL = auto()
    QUESTION = auto()
    ANSWER = auto()


def main() -> None:
    reader: PdfReader = PdfReader(sourcefile)

    print(f"Total pages in inputfile: {len(reader.pages)}")

    results: list[Record] = []
    current_record: Record = Record()
    current_index: int = 0

    for page in reader.pages[headerpages_to_skip:]:
        fulltext: str = page.extract_text()
        lines: list[str] = fulltext.splitlines()
        state: ParserState = ParserState.NEUTRAL

        for line in lines:
            if state == ParserState.NEUTRAL:
                if not re.match(question_marker, line):
                    continue

        # during testing, only use the first not-skipped page
        break

    # print(reader.pages[8].extract_text())


if __name__ == "__main__":
    main()
