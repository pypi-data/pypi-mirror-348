from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from kash.utils.common.url import Url

# We wrap each command as a convenient way to customize CLI docs and to make
# all imports lazy, since some of these actions have a lot of dependencies that
# make imports slow. This way CLI help etc feels snappy.
if TYPE_CHECKING:
    from kash.model import ActionResult


def setup(show: bool = False) -> None:
    """
    Run this first! Helps you log in and get an API key to get set up to use Textpress.
    """
    from texpr.config import interactive_setup, show_setup

    if show:
        show_setup()
    else:
        interactive_setup()


def import_clipboard(title: str, plaintext: bool = False) -> Path:
    """
    Import the contents of the OS (system) clipboard into a file in the workspace.
    Use to copy content from elsewhere (like a doc or chat session) and paste into
    a file for use by Textpress. Presumes Markdown format unless the `plaintext` flag
    is set.
    """

    import pyperclip
    from kash.model import Format, Item, ItemType
    from kash.workspaces import current_ws

    contents = pyperclip.paste()
    if not contents.strip():
        raise ValueError("Clipboard is empty")

    ws = current_ws()
    format = Format.plaintext if plaintext else Format.markdown
    store_path = ws.save(Item(type=ItemType.resource, format=format, title=title, body=contents))

    return store_path


def convert(md_path: Path | Url) -> ActionResult:
    """
    Convert a document to clean Markdown.

    This works well to convert docx files, especially Gemini Deep Research
    output: click to export a report to Google Docs, then select `File >
    Download > Microsoft Word (.docx)`.

    Uses MarkItDown/Mammoth/Markdownify and a few additional cleanups to
    convert docx files and flowmark for clean Markdown formatting.
    """
    from kash.exec import prepare_action_input

    from texpr.actions.textpress_convert import textpress_convert

    input = prepare_action_input(md_path)
    return textpress_convert(input)


def format(md_path: Path | Url, add_classes: str | None = None) -> ActionResult:
    """
    Convert and format text, Markdown, or an HTML fragment to pretty, formatted,
    minified HTML using the TextPress template. Result contains clean Markdown
    and HTML.

    Supports GFM-flavored Markdown tables and footnotes. Uses `convert` to convert
    docx files.
    """
    from kash.exec import prepare_action_input

    from texpr.actions.textpress_format import textpress_format

    input = prepare_action_input(md_path)
    return textpress_format(input, add_classes=add_classes)


def publish(path: Path | Url, add_classes: str | None = None) -> ActionResult:
    """
    Publish (or re-publish) a document as a Textpress webpage. Uses `format`
    to convert and format the content and publishes the result.
    """
    from kash.exec import prepare_action_input

    from texpr.actions.textpress_publish import textpress_publish

    input = prepare_action_input(path)
    return textpress_publish(input, add_classes=add_classes)
