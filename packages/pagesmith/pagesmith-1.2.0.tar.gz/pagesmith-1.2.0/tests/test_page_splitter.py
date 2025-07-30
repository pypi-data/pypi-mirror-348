import re

import allure
from pagesmith.page_splitter import PageSplitter


def normalize(text: str) -> str:
    """Make later processing more simple."""
    # if self.escape_html:
    #     text = escape(text)
    text = re.sub(r"(\r?\n|\u2028|\u2029)", " <br/> ", text)
    text = re.sub(r"\r", "", text)
    return re.sub(r"[ \t]+", " ", text)


@allure.epic("Page splitter")
def test_paragraph_end_priority(mock_page_splitter):
    # Paragraph end is within 25% error margin but farther than sentence end
    text = (
        "a" * 25 + ".  " + "b" * 5 + "\n\n" + "a" * 22 + "\r\n\t\r\n" + "b" * 3 + ". \r" + "a" * 10
    )
    splitter = PageSplitter(text)
    pages = list(splitter.pages())
    assert len(pages) == 3
    assert "a" * 25 + ". " + "b" * 5 + "\n\n" == pages[0]
    assert "a" * 22 + "\n \n" == pages[1]
    assert "b" * 3 + ". " + "a" * 10 == pages[2]


@allure.epic("Page splitter")
def test_sentence_end_priority(mock_page_splitter):
    # Sentence end near farther than word end
    text = "a" * 29 + " aaa" + ". " + "b" * 5 + " next  sentence.\n"
    splitter = PageSplitter(text)
    pages = list(splitter.pages())
    assert len(pages) == 2
    assert "a" * 29 + " aaa" + ". " == pages[0]

    # now no sentence - will split nearer to target by words
    text = "a" * 29 + " aaa" + "  " + "b" * 5 + " next  sentence.\n"
    splitter = PageSplitter(text)
    pages = list(splitter.pages())
    assert len(pages) == 2
    assert "a" * 29 == pages[0]


@allure.epic("Page splitter")
def test_word_end_priority(mock_page_splitter):
    # No paragraph or sentence end, splitting by word
    text = "A long text without special ends here"
    splitter = PageSplitter(text)
    pages = list(splitter.pages())
    assert len(pages) == 2


@allure.epic("Page splitter")
def test_no_special_end(mock_page_splitter):
    # A long string without any special end
    text = "a" * 60
    splitter = PageSplitter(text)
    pages = list(splitter.pages())
    assert len(pages) == 2
    len(pages[0]) == 30


@allure.epic("Page splitter")
def test_chapter_pattern(mock_page100_splitter, chapter_pattern):
    splitter = PageSplitter(f"aa{chapter_pattern}34")
    pages = list(splitter.pages())
    assert len(splitter.toc) == 1, f"chapter_pattern: {chapter_pattern}"
    assert splitter.toc[0] == (chapter_pattern.strip(), 1, 1)  # first word with index 0 is "aa"


@allure.epic("Page splitter")
def test_wrong_chapter_pattern(mock_page_splitter, wrong_chapter_pattern):
    splitter = PageSplitter(f"aa{wrong_chapter_pattern}34")
    list(splitter.pages())
    assert len(splitter.toc) == 0, f"chapter_pattern: {wrong_chapter_pattern}"


@allure.epic("Page splitter")
def test_pages_shift_if_heading(mock_page_splitter):
    chapter_pattern = "\n\nCHAPTER VII.\n\n"
    splitter = PageSplitter("a" * 16 + chapter_pattern + " " + "aaa")
    pages = list(splitter.pages())
    assert len(pages) == 3
    assert pages[0] == "a" * 16
    assert pages[1] == chapter_pattern

    splitter = PageSplitter("a" * 16 + "\n123 aaaaaaaa\n" + "aaa")
    pages = list(splitter.pages())
    assert len(pages) == 2
    assert pages[0] == "a" * 16 + "\n123 aaaaaaaa\n"
    assert pages[1] == "aaa"

    splitter = PageSplitter("a" * 20 + " aa\n\n" + "d" * 21 + "\n\n34")
    pages = list(splitter.pages())
    print(pages)
    print([len(page) / splitter.PAGE_LENGTH_TARGET for page in pages])
    assert len(pages) == 3
    assert pages[0] == "a" * 20 + " aa\n\n"
