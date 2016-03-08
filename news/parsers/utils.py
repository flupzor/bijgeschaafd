import lxml


def is_whitespace(c):
    if c == ' ' or c == '\n':
        return True

    return False


def collapse_whitespace(text):
    """
    http://www.w3.org/TR/REC-html40/struct/text.html#h-9.1
    """
    new_text = u''

    for i, char in enumerate(text):
        next_char = text[i + 1] if i + 1 < len(text) else None

        if next_char is not None \
           and is_whitespace(char) and is_whitespace(next_char):
            continue

        new_text += char

    # If all the characters are whitespace the contents is
    # considered empty.
    if len(new_text) == 1 and is_whitespace(new_text):
        return ''

    return new_text


def collapse_newline(text):
    new_text = u''

    for i, char in enumerate(text):
        next_char = text[i + 1] if i + 1 < len(text) else None

        if char == '\n' and next_char == '\n':
            continue

        new_text += char

    return new_text


def remove_whitespace_after_newline(text):
    newline = True
    new_text = u''

    for c in text:
        if c == '\n':
            newline = True

        if not is_whitespace(c):
            newline = False

        if newline and is_whitespace(c):
            if c == '\n':
                new_text += c

            continue

        new_text += c

    return new_text


def _html_to_text(element, parent=None, level=0, exclude_fn=None):
    add_tail = True
    add_text = True
    add_newline = False
    add_newline_force = False
    look_at_children = True
    exclude = False

    if exclude_fn and exclude_fn(element, parent, level):
        add_tail = False
        add_text = False
        look_at_children = False
        exclude = True
    elif isinstance(element, lxml.etree._Comment):
        add_tail = True
        add_text = False
        look_at_children = False
    elif element.tag == 'script':
        add_tail = True
        add_text = False
        look_at_children = False
    elif element.tag == 'br':
        add_tail = True
        add_text = False
        add_newline = True
        add_newline_force = True
        look_at_children = False
    elif element.tag == 'p':
        add_tail = True
        add_text = True
        add_newline = True
        look_at_children = True
    elif element.tag == 'h1' or element.tag == 'h2' or \
            element.tag == 'h3':
        add_tail = True
        add_text = True
        add_newline = True
        look_at_children = True
    elif element.tag == 'div':
        add_tail = True
        add_text = True
        add_newline = True
        look_at_children = True

    text = u''

#    print "{} tag: {}: text: '{}' ({}) tail: '{}' ({}) newline: {} {}".format(
#        level,
#        element.tag,
#        "None" if element.text is None else element.text.encode("unicode-escape"),
#        "y" if add_text else "n",
#        "None" if element.tail is None else element.tail.encode("unicode-escape"),
#        "y" if add_tail else "n",
#        "y" if add_newline else "n",
#        "exclude" if exclude else ""
#    )

    if add_text and element.text:
        text += collapse_whitespace(element.text)

    if look_at_children:
        for child in element.getchildren():
            text += _html_to_text(child, element, level=level+1, exclude_fn=exclude_fn)

    if add_newline_force or (add_newline and len(text) > 0):
        text += '\n'

    if add_tail and element.tail:
        text += collapse_whitespace(element.tail)

    return text


def html_to_text(elements, exclude_fn=None):
    """
    Convert the text within a HTML DOM tree to a unicode string.

    :elements PyQuery or lxml Element that should be converted to text.
    :return unicode string
    """

    if isinstance(elements, lxml.etree._Element) and elements.tag == 'script':
        return u''

    text = u''
    for element in elements:
        text += _html_to_text(element, exclude_fn=exclude_fn)

    # We collapse newlines here because I do not feel like figuring
    # out when we should have one and when we should have two newlines.
    # This is not correct, ofcourse.
    return collapse_newline(remove_whitespace_after_newline(text))
