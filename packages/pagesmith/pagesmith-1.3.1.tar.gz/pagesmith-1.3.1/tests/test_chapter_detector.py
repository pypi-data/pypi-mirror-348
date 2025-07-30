import allure

from pagesmith import ChapterDetector, PageSplitter
from pagesmith.page_splitter import PAGE_LENGTH_TARGET


@allure.epic("Book import")
@allure.feature("Chapter detection")
def test_get_word_num_words(sentence_6_words):
    splitter = ChapterDetector()
    assert splitter.get_word_num(sentence_6_words, len(sentence_6_words)) == 6


@allure.epic("Book import")
@allure.feature("Chapter detection")
def test_get_word_num_no_separators():
    splitter = ChapterDetector()
    assert splitter.get_word_num("a" * 10) == 1


@allure.epic("Book import")
@allure.feature("Page splitting")
def test_toc_word_counts_simple():
    """Test that TOC entries have correct word numbers for a simple case."""
    # A simple text with one chapter heading
    text = """Some introductory text.

Chapter 1

This is the first chapter content."""

    splitter = PageSplitter(text)
    # Collect all pages
    pages = list(splitter.pages())

    # The TOC should have one entry for Chapter 1
    assert len(splitter.toc) == 1
    chapter, page_num, word_num = splitter.toc[0]

    assert chapter == "Chapter 1"
    assert page_num == 1  # First page

    # Calculate expected word count
    intro_words = len("Some introductory text.".split())
    expected_word_count = intro_words  # Words before "Chapter 1"

    assert word_num == expected_word_count


@allure.epic("Book import")
@allure.feature("Page splitting")
def test_toc_word_counts_multiple_chapters():
    """Test that TOC entries have correct word numbers for multiple chapters."""
    # Text with multiple chapters
    text = """Prologue words here.

Chapter I

First chapter text.

Chapter II

Second chapter text."""

    splitter = PageSplitter(text)
    # Collect all pages
    pages = list(splitter.pages())

    # The TOC should have two entries
    assert len(splitter.toc) == 2

    # Check first chapter
    chapter1, page_num1, word_num1 = splitter.toc[0]
    assert chapter1 == "Chapter I"
    print(pages[page_num1 - 1], word_num1)
    assert page_num1 == 1

    # Words before "Chapter I"
    prologue_words = len("Prologue words here.".split())
    expected_chapter1_word = prologue_words  # Count words from 0
    assert word_num1 == expected_chapter1_word

    # Check second chapter
    chapter2, page_num2, word_num2 = splitter.toc[1]
    assert chapter2 == "Chapter II"
    assert page_num2 == 1  # Still on first page

    # Words before "Chapter II" (prologue + first chapter heading + first chapter text)
    first_chapter_text_words = len("First chapter text.".split())
    expected_word_count2 = (
        expected_chapter1_word + 2 + first_chapter_text_words
    )  # +2 for "Chapter I"
    assert word_num2 == expected_word_count2


@allure.epic("Book import")
@allure.feature("Page splitting")
def test_toc_word_counts_across_pages():
    """Test that TOC entries have correct word numbers when chapters span multiple pages."""
    # Create a long text that will span multiple pages
    word_len = len("x ")
    first_page_filler_words_count = int(PAGE_LENGTH_TARGET * 0.9) // word_len

    # Create first page with a chapter at the end closer than target size possible tolerance
    first_page = "x " * first_page_filler_words_count + "\n\nChapter 1\n\n" + "Some text. " * 5

    # Create second page with a chapter even closer to the target size
    second_page = "\n\nChapter 2\n\nMore text."

    text = first_page + second_page

    splitter = PageSplitter(text)
    # Collect all pages
    pages = list(splitter.pages())
    print(pages)
    print(first_page_filler_words_count)
    print(first_page_filler_words_count * word_len / PAGE_LENGTH_TARGET)
    print([(len(page), len(page) / PAGE_LENGTH_TARGET) for page in pages])

    # The TOC should have two entries
    assert len(splitter.toc) == 2

    # Check first chapter
    chapter1, page_num1, word_num1 = splitter.toc[0]
    assert chapter1 == "Chapter 1"
    assert page_num1 == 1  # First page
    assert word_num1 == first_page_filler_words_count

    # Check second chapter
    chapter2, page_num2, word_num2 = splitter.toc[1]
    assert chapter2 == "Chapter 2"
    assert page_num2 == 2  # Second page
    assert word_num2 == 0


@allure.epic("Book import")
@allure.feature("Page splitting")
def test_toc_integration_with_chapter_detector():
    """Test that PageSplitter correctly integrates with ChapterDetector for word counting."""
    # Create a mock ChapterDetector that we can spy on
    original_get_word_num = ChapterDetector.get_word_num

    call_args = []

    def mock_get_word_num(self, text, end=None):
        call_args.append((text, end))
        return original_get_word_num(self, text, end)

    # Replace the method temporarily
    ChapterDetector.get_word_num = mock_get_word_num

    try:
        # Text with a chapter
        text = """Intro text.

Chapter 5

Chapter content."""

        splitter = PageSplitter(text)
        # Process all pages
        pages = list(splitter.pages())

        # Verify that get_word_num was called with the right parameters
        assert len(call_args) > 0

        # The TOC should have one entry
        assert len(splitter.toc) == 1
        chapter, page_num, word_num = splitter.toc[0]

        assert chapter == "Chapter 5"
        assert page_num == 1

        # Verify that the word count matches what we expect
        intro_words = len("Intro text.".split())
        assert word_num == intro_words

    finally:
        # Restore the original method
        ChapterDetector.get_word_num = original_get_word_num


@allure.epic("Book import")
@allure.feature("Page splitting")
def test_toc_word_counts_in_complex_book(complex_book_text):
    """Test TOC word counts in a more complex book with multiple pages and chapters."""
    splitter = PageSplitter(complex_book_text)
    pages = list(splitter.pages())

    # Should have 4 chapters in the TOC
    assert len(splitter.toc) == 4

    # Check that each chapter is on the correct page
    # and has a reasonable word number
    for i, (chapter, page_num, word_num) in enumerate(splitter.toc, 1):
        # Chapter title should match pattern
        assert f"Chapter {i}" in chapter

        # Word number should be a non-positive integer
        assert word_num >= 0

        # For chapters after the first, page number should increase
        if i > 1:
            prev_page = splitter.toc[i - 2][1]
            assert page_num >= prev_page
