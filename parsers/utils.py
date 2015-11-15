import lxml

def _html_to_text(element, parent=None, level=0):
    add_tail = False
    add_text = False
    strip_text = False
    add_newline = False
    look_at_children = True

    if isinstance(element, lxml.etree._Comment):
        if parent.tag == 'p' or parent.tag == 'a' or \
           parent.tag == 'br':
            add_tail = True
        add_text = False
        look_at_children = False

    if element.tag == 'script':
        if parent.tag == 'p':
            add_tail = True
        add_text = False
        look_at_children = False
    elif element.tag == 'br':
        add_tail = True
        add_text = False
        add_newline = True
        look_at_children = False
    elif element.tag == 'p':
        add_tail = False
        add_text = True
        add_newline = True
        look_at_children = True
    elif element.tag == 'em':
        add_tail = True
        add_text = True
        look_at_children = True
    elif element.tag == 'a':
        if parent.tag == 'p':
            add_tail = True
        add_text = True
        look_at_children = True
    elif element.tag == 'h1' or element.tag == 'h2' or \
            element.tag == 'h3':
        add_tail = True
        add_text = True
        add_newline = True
        look_at_children = True
    elif element.tag == 'div':
        add_tail = False

        if element.text and element.text.strip():
            add_text = True
            strip_text = True
            add_newline = True
        look_at_children = True

    text = []

#    print "{} tag: {}: text: '{}' ({}) tail: '{}' ({}) newline: {}".format(
#        level,
#        element.tag,
#        "None" if element.text is None else element.text.encode("unicode-escape"),
#        "y" if add_text else "n",
#        "None" if element.tail is None else element.tail.encode("unicode-escape"),
#        "y" if add_tail else "n",
#        "y" if add_newline else "n"
#    )

    if add_text and element.text:
        if strip_text:
            text += [element.text.strip(), ]
        else:
            text += [element.text, ]

    if look_at_children:
        for child in element.getchildren():
            text += _html_to_text(child, element, level=level+1)

    if add_newline:
        text += ['\n']

    if add_tail and element.tail:
        text += [element.tail, ]

    return text


def html_to_text(elements):
    """
    Convert the text within a HTML DOM tree to a unicode string.

    :elements PyQuery or lxml Element that should be converted to text.
    :return unicode string
    """

    if isinstance(elements, lxml.etree._Element) and elements.tag == 'script':
        return u''

    text = []
    for element in elements:
        text += _html_to_text(element)

    return ''.join([p for p in text])
