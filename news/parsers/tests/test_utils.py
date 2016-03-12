from django.test import TestCase

from pyquery import PyQuery as pq

from ..utils import html_to_text, collapse_whitespace


class UtilsTests(TestCase):
    def test_collapse_whitespace(self):
        text = u'\r\n\f\u200b \n\t '
        self.assertEquals(collapse_whitespace(text), "")

    def test_html_to_text_one_element(self):
        html = pq("<div>&#65; simple test case &copy;</div>")
        text = html_to_text(html)

        self.assertEquals(u"\u0041 simple test case \u00A9\n", text)

    def test_html_to_text_with_script(self):
        html = pq("<div>&#65; simple test case &copy;<script>This should be "
                  "ignored.</script> with a tail &copy;</div>")
        text = html_to_text(html)

        self.assertEquals(
            u"\u0041 simple test case \u00A9 with a tail \u00A9\n", text
        )

    def test_html_to_text_with_script_with_children(self):
        html = pq("<div>&#65; simple test case &copy;<script><p>This should "
                  "be ignored as well</p>This should be ignored.</script> "
                  "with a tail &copy;</div>")
        text = html_to_text(html)

        self.assertEquals(
            u"\u0041 simple test case \u00A9 with a tail \u00A9\n", text
        )

    def test_html_to_text_multiple_levels(self):
        html = pq("<div>&#65; test case &copy; <div><p>with multiple "
                  "levels </p>and a tail &copy;</div> and another tail "
                  "&copy;</div>")
        text = html_to_text(html)

        expected = u"A test case \u00A9 with multiple levels \nand " \
                   u"a tail \u00A9\nand another tail \u00A9\n"

        self.assertEquals(text, expected)

    def test_html_to_text_with_comments(self):
        html = pq("<!-- IGNORE --><div>text<p><!-- comment which should be "
                  "ignored --> and more text</p></div>")
        text = html_to_text(html)

        self.assertEquals(u"text and more text\n", text)
