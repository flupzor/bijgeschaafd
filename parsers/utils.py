import lxml


def _html_to_text(element):
    if element.tag == 'script':
        return [element.tail, ]

    if isinstance(element, lxml.etree._Comment):
        return [element.tail, ]

    text = []

    if element.text:
        text += [element.text, ]
    for child in element.getchildren():
        text += _html_to_text(child)
    if element.tail:
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

    return ' '.join([p.strip() for p in text])
