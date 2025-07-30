"""Detect headings."""

import logging
import re
from typing import TypeAlias

log = logging.getLogger()


TocEntry: TypeAlias = tuple[str, int, int]  # <title>, <page num>, <word on the page num>
Toc: TypeAlias = list[TocEntry]
ChapterMatch: TypeAlias = tuple[str, int, int, int]  # <title>, <position>, <page_num>, <word_num>


class ChapterDetector:
    """Detect chapters."""

    def get_chapters(self, page_text: str, page_num: int) -> list[ChapterMatch]:
        """Detect chapter headings in the text.

        Return a list of tuples (chapter, position, page, word).
        Position is the character position in the text where the chapter starts.
        """
        patterns = self.prepare_chapter_patterns()
        headings: list[ChapterMatch] = []
        for pattern in patterns:
            for match in pattern.finditer(page_text):
                title = match.group().replace("<br/>", " ").strip()
                position = match.start()
                word_num = self.get_word_num(page_text, position)
                headings.append((title, position, page_num, word_num))
        return headings

    def prepare_chapter_patterns(self) -> list[re.Pattern[str]]:  # pylint: disable=too-many-locals
        """Prepare regex patterns for detecting chapter headings."""
        # Form 1: Chapter I, Chapter 1, Chapter the First, CHAPTER 1
        # Ways of enumerating chapters, e.g.
        space = r"[ \t]"
        line_sep = rf"{space}*(\r?\n|\u2028|\u2029|{space}*<br\/>{space}*)"
        arabic_numerals = r"\d+"
        roman_numerals = "(?=[MDCLXVI])M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})"
        number_words_by_tens_list = [
            "twenty",
            "thirty",
            "forty",
            "fifty",
            "sixty",
            "seventy",
            "eighty",
            "ninety",
        ]
        number_words_list = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "fifteen",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen",
        ] + number_words_by_tens_list
        number_word = "(" + "|".join(number_words_list) + ")"
        ordinal_number_words_by_tens_list = [
            "twentieth",
            "thirtieth",
            "fortieth",
            "fiftieth",
            "sixtieth",
            "seventieth",
            "eightieth",
            "ninetieth",
        ] + number_words_by_tens_list
        ordinal_number_words_list = (
            [
                "first",
                "second",
                "third",
                "fourth",
                "fifth",
                "sixth",
                "seventh",
                "eighth",
                "ninth",
                "twelfth",
                "last",
            ]
            + [f"{numberWord}th" for numberWord in number_words_list]
        ) + ordinal_number_words_by_tens_list
        ordinal_word = "(the )?(" + "|".join(ordinal_number_words_list) + ")"
        enumerators = rf"({arabic_numerals}|{roman_numerals}|{number_word}|{ordinal_word})"
        chapter_name = r"[\w \t '`\"\.’\?!:\/-]{1,120}"
        name_line = rf"{line_sep}{space}*{chapter_name}{space}*"

        templ_key_word = (
            rf"(chapter|glava|глава|часть|том){space}+"
            rf"({enumerators}(\.|{space}){space}*)?({space}*{chapter_name})?({name_line})?"
        )
        templ_numbered = (
            rf"({arabic_numerals}|{roman_numerals})\.{space}*({chapter_name})?({name_line})?"
        )
        templ_numbered_dbl_empty_line = (
            rf"({arabic_numerals}|{roman_numerals})"
            rf"(\.|{space}){space}*({chapter_name})?({name_line})?{line_sep}"
        )
        # todo may be we should extract only titles with names?
        return [
            re.compile(
                f"{line_sep}{line_sep}{templ_key_word}{line_sep}{line_sep}",
                re.IGNORECASE,
            ),
            re.compile(
                f"{line_sep}{line_sep}{templ_numbered}{line_sep}{line_sep}",
                re.IGNORECASE,
            ),
            re.compile(
                f"{line_sep}{line_sep}{templ_numbered_dbl_empty_line}{line_sep}{line_sep}",
                re.IGNORECASE,
            ),
        ]

    def get_word_num(self, text: str, end: int | None = None) -> int:
        """Get word number up to the given position.

        Count words from 0.
        """
        if end is None:
            end = len(text)
        ignore_words = ["<br/>"]
        return sum(1 for word in re.split(r"\s+", text[:end]) if word and word not in ignore_words)
