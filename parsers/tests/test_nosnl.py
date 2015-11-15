from django.test import TestCase

import os
from django.utils._os import upath

from ..nosnl import NOSNLParser


TEST_DIR = os.path.join(os.path.dirname(upath(__file__)), 'data')


class NOSNLParserTests(TestCase):
    maxDiff = None

    def test_nos_nl(self):
        """
        http://nos.nl/artikel/2069130-dodental-parijs-op-129-maar-zal-nog-stijgen.html
        """

        article_name = "www_nos_nl_artikel_2069130-dodental-parijs-op-129" \
                       "-maar-zal-nog-stijgen.html"

        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = NOSNLParser('', html=article_file.read())

        expected = \
            u"Bij de aanslagen in Parijs zijn 129 mensen omgekomen. Dat " \
            u"aantal zal nog stijgen,\xa0heeft de openbaar aanklager " \
            u"gezegd\xa0op een persconferentie.\xa0352 mensen raakten gewond. " \
            u"99 van hen verkeren in kritieke toestand.\xa0\n" \
            u"Alleen al in de concertzaal Bataclan zijn 89 mensen gedood. De " \
            u"terroristen\xa0noemden Syri\xeb en Irak tijdens hun aanslag.\xa0\n" \
            u"Openbaar aanklager Molins zei verder dat zeven aanvallers " \
            u"zijn gedood. De terroristen hadden drie teams gevormd, die " \
            u"hun zes\xa0aanslagen\xa0met elkaar hadden afgestemd. Ze " \
            u"droegen alle zeven\xa0kalasjnikovs en bomgordels met " \
            u"precies\xa0hetzelfde type explosieven.\n" \
            u"Een van de aanvallers van Bataclan was een man van 29. " \
            u"Hij werd\xa0sinds 2010 in de gaten gehouden\xa0door\xa0de " \
            u"veiligheidsdiensten omdat hij radicaliseerde. Hij is " \
            u"meerdere keren voor kleine vergrijpen in aanraking gekomen " \
            u"met de politie, maar heeft nooit gevangen gezeten. Volgens " \
            u"Franse media heette de man Isma\xebl M. en woonde\xa0hij " \
            u"in Chartres.\xa0\n" \
            u"Ook circuleert de naam\xa0Abbdulakbak B. als een van de " \
            u"terroristen in Bataclan.\xa0Hij zou via het Griekse eiland " \
            u"Leros Europa zijn binnengekomen.\n" \
            u"Belgi\xeb\n" \
            u"Er is ook een verband met buurland Belgi\xeb. " \
            u"Twee verdachte\xa0auto's in Parijs hadden Belgische " \
            u"kentekens. Vanochtend zijn bij een controle bij de " \
            u"Frans-Belgische grens drie mannen aangehouden. Een van " \
            u"hen was de huurder van de auto die bij Bataclan is " \
            u"aangetroffen.\xa0Vanmiddag zijn in\xa0Brussel ook " \
            u"drie\xa0verdachten opgepakt.\xa0\n" \
            u"Onder de dodelijke slachtoffers zijn zeker vijf " \
            u"buitenlanders: twee Belgen, een Portugees, een Spanjaard " \
            u"en een Brit.\n"

        self.assertEquals(parsed_article.body, expected)
