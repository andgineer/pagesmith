import re

from lxml import etree, html

HTML_TAG_REPLACEMENT = "htmlpagesmith"


def parse_partial_html(input_html: str) -> etree._Element | None:  # noqa: C901,PLR0912
    """Parse string with HTML fragment into an lxml tree.

    Supports partial HTML content.
    Removes comments and CDATA.
    """

    # Clean up comments
    open_count = input_html.count("<!--")
    close_count = input_html.count("-->")
    if open_count != close_count:
        input_html = input_html.replace("<!--", "&lt;!--")

    # Clean up CDATA
    input_html = re.sub(r"[\n\r]+", " ", input_html)
    input_html = re.sub(r"(<!\[CDATA\[.*?]]>|<!DOCTYPE[^>]*?>)", "", input_html, flags=re.DOTALL)

    # Temporarily replace HTML tags to avoid special treatment by lxml
    input_html = re.sub(
        r"<html(\s[^>]*)?>",
        rf"<{HTML_TAG_REPLACEMENT}\1>",
        input_html,
        flags=re.IGNORECASE,
    )
    input_html = re.sub(r"</html>", rf"</{HTML_TAG_REPLACEMENT}>", input_html, flags=re.IGNORECASE)

    parser = etree.HTMLParser(recover=True, remove_comments=True, remove_pis=True)
    try:
        # Use HTML parser with fragments_fromstring
        fragments = html.fragments_fromstring(input_html, parser=parser)
    except AssertionError:
        try:
            wrapped_html = f"<root>{input_html}</root>"
            fragments = etree.fromstring(wrapped_html, parser=parser)
        except Exception:  # noqa: BLE001
            # Last resort: return as text in a fake root element
            fragments = html.Element("root")
            fragments.text = input_html

    if isinstance(fragments, list) and len(fragments) == 1:
        result = fragments[0]
    elif isinstance(fragments, list):
        # Create a container for multiple fragments
        container = html.Element("root")
        for fragment in fragments:
            if isinstance(fragment, str):
                if len(container) == 0:
                    container.text = (container.text or "") + fragment
                else:
                    container[-1].tail = (container[-1].tail or "") + fragment
            else:
                container.append(fragment)
        result = container
    else:
        result = fragments

    if isinstance(result, etree._Element):  # noqa: SLF001
        html_tags = result.xpath(f".//{HTML_TAG_REPLACEMENT}")

        # Root element has the target tag - rename it
        if result.tag == HTML_TAG_REPLACEMENT:
            result.tag = "html"
        # Only one element in the entire tree has the target tag - rename it
        elif len(html_tags) == 1:
            html_tags[0].tag = "html"
        # Multiple elements have the target tag - unwrap them all
        else:
            for element in html_tags:
                unwrap_element(element)

    return result


def unwrap_element(element: etree.Element) -> None:  # noqa: PLR0912,C901
    """Unwrap an element, replacing with its content."""
    parent = element.getparent()
    if parent is None:
        return

    pos = parent.index(element)

    # Handle text content
    if element.text:
        if pos > 0:
            # Add to tail of previous sibling
            prev = parent[pos - 1]
            if prev.tail:
                prev.tail += element.text
            else:
                prev.tail = element.text
        # Add to parent's text
        elif parent.text:
            parent.text += element.text
        else:
            parent.text = element.text

    # Move each child to parent
    children = list(element)
    for i, child in enumerate(children):
        parent.insert(pos + i, child)

    # Handle tail text
    if element.tail:
        if len(children) > 0:
            # Add to tail of last child
            if children[-1].tail:
                children[-1].tail += element.tail
            else:
                children[-1].tail = element.tail
        elif pos > 0:
            # Add to tail of previous sibling
            prev = parent[pos - 1]
            if prev.tail:
                prev.tail += element.tail
            else:
                prev.tail = element.tail
        # Add to parent's text
        elif parent.text:
            parent.text += element.tail
        else:
            parent.text = element.tail

    parent.remove(element)


def etree_to_str(root: etree._Element | None) -> str:
    """Convert etree back to string, removing root wrapper."""
    if root is None:
        return ""

    if isinstance(root, str):
        return root

    # If this is our root wrapper, extract its contents
    if root.tag == "root":
        result = root.text or ""
        for child in root:
            result += html.tostring(child, encoding="unicode", method="html")
        return result

    # For normal elements, return as-is using HTML serialization
    return html.tostring(root, encoding="unicode", method="html")  # type: ignore[no-any-return]
