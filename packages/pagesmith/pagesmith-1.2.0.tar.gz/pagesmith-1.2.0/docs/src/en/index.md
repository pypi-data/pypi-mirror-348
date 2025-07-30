# pagesmith

Splitting HTML into pages, preserving HTML tags while respecting the original document structure and text integrity.

Utilize blazing fast lxml parser.

Provides utilities for working with pages such as refining HTML.

Also contains class for splitting to pages and extracting Table of Content from pure text

!!! note "How It Works"
    The `HtmlPageSplitter` class intelligently splits HTML content into appropriately sized pages while ensuring all HTML tags remain properly closed and valid. This preserves both the document structure and styling.

## Installation

```bash
pip install pagesmith
```

## Usage
- [Split HTML to Pages](html_splitter.md)
- [Split Text to Pages](text_splitter.md)
- [Refine HTML](refine.md)
