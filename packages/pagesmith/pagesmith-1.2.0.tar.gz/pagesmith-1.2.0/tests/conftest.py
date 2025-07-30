import pytest

from pagesmith import PageSplitter


@pytest.fixture(scope="function", params=["Hello 123 <br/> word/123 123-<word>\n<br/> and last!"])
def sentence_6_words(request):
    return request.param


@pytest.fixture
def complex_book_text():
    """Generate a complex book text with multiple chapters."""
    chapters = [
        "Chapter 1\n\nFirst chapter content.",
        "Chapter 2\n\nSecond chapter with more text.",
        "Chapter 3\n\nThird chapter with even more text.",
        "Chapter 4\n\nFourth and final chapter.",
    ]

    # Add some space between chapters to force page breaks
    padding = "\n\n" + ". " * 500 + "\n\n"
    return padding.join(chapters)


def set_book_page_length(page_length):
    PageSplitter.PAGE_LENGTH_TARGET = page_length  # Mocked target length for testing
    PageSplitter.PAGE_LENGTH_ERROR_TOLERANCE = 0.5
    PageSplitter.PAGE_MIN_LENGTH = int(
        PageSplitter.PAGE_LENGTH_TARGET * (1 - PageSplitter.PAGE_LENGTH_ERROR_TOLERANCE)
    )
    PageSplitter.PAGE_MAX_LENGTH = int(
        PageSplitter.PAGE_LENGTH_TARGET * (1 + PageSplitter.PAGE_LENGTH_ERROR_TOLERANCE)
    )


def mock_book_plain_text(page_length: int):
    original_target = PageSplitter.PAGE_LENGTH_TARGET
    set_book_page_length(page_length)
    yield
    set_book_page_length(original_target)


@pytest.fixture
def mock_page_splitter():
    yield from mock_book_plain_text(30)


@pytest.fixture
def mock_page100_splitter():
    yield from mock_book_plain_text(100)


@pytest.fixture(
    scope="function",
    params=[
        "\n\nCHAPTER VII.\nA Mad Tea-Party\n\n",
        "\n\nCHAPTER I\n\n",
        "\n\nCHAPTER Two\n\n",
        "\n\nCHAPTER Third\n\n",
        "\n\nCHAPTER four. FALL\n\n",
        "\n\nCHAPTER twenty two. WINTER\n\n",
        "\n\nCHAPTER last inline\nunderline\n\n",
        "\n\nI. A SCANDAL IN BOHEMIA\n \n",
        "\n\nV.\nПет наранчиних сjеменки\n\n",
    ],
)
def chapter_pattern(request):
    return request.param


@pytest.fixture(
    scope="function",
    params=[
        "\ncorrespondent could be.\n\n",
    ],
)
def wrong_chapter_pattern(request):
    return request.param
