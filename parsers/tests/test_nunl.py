from django.test import TestCase

import os
from django.utils._os import upath

from ..nunl import NuNLParser


TEST_DIR = os.path.join(os.path.dirname(upath(__file__)), 'data')


class NuNLParserTests(TestCase):
    maxDiff = None

    def test_nu_nl_lifeblog(self):
        """
        http://www.nu.nl/champions-league/4136168/reacties-psv-3-2-nederlaag-bij-cska-moskou-gesloten.html
        """
        article_name = 'www_nu_nl_champions-league_4136168_reacties' \
                       '-psv-3-2-nederlaag-bij-cska-moskou-gesloten.html'
        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = NuNLParser('', html=article_file.read())

        self.assertEquals(
            parsed_article.title,
            'Reacties PSV na 3-2 nederlaag bij CSKA Moskou (gesloten)'
        )
        self.assertEquals(
            parsed_article.body,
            u'In de tweede poulewedstrijd in de Champions League neemt PSV '
            u'het in Moskou op tegen CSKA. De aftrap is om 20.45 uur. '
            u'Daarnaast worden er nog zes duels gespeeld. De wedstrijd '
            u'Astana-Galatasaray begon al om 18.00 uur en is in 2-2 '
            u'ge\xebindigd.\n'
            u'Het duel tussen CSKA Moskou en PSV wordt live '
            u'uitgezonden door SBS6 en NU.nl.\n'
        )

    def test_nu_nl_article(self):
        """
        http://www.nu.nl/politiek/4163338/bestuur-kamer-stelt-onderzoek-in-wegens-lekken-commissie-stiekem.html
        """

        article_name = 'www_nu_nl_politiek_4163338_bestuur-kamer-stelt-' \
                       'onderzoek-in-wegens-lekken-commissie-stiekem.html'

        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = NuNLParser('', html=article_file.read())

        # Hint for a update: I used fold -s -w 58 and some regex
        expected = \
            u"Het presidium, het dagelijks bestuur van de Tweede Kamer, " \
            u"stelt een onderzoekscommissie in naar het lekken uit de " \
            u"zogenoemde commissie-Stiekem.\n" \
            u"Dat is donderdag bekendgemaakt door Kamervoorzitter Anouchka van " \
            u"Miltenburg na afloop van een vergadering van het " \
            u"presidium.\xa0\n\n" \
            u" Eerder deze week werd bekend dat er aangifte is " \
            u"gedaan wegens het lekken uit de\xa0Commissie voor de " \
            u"Inlichtingen- en Veiligheidsdiensten, oftewel de " \
            u"commissie-Stiekem,\xa0naar\xa0NRC Handelsblad. De " \
            u"commissie-Stiekem\xa0bestaat uit de fractievoorzitters " \
            u"van de gekozen partijen.\xa0Lekken uit deze commissie " \
            u"geldt als een ambtsmisdrijf.\n\n" \
            u" Woensdag liet het OM weten dat " \
            u"zij de zaak, die al anderhalf jaar speelt, niet verder " \
            u"behandelt en neerlegt bij de Kamer.\xa0De Grondwet " \
            u"bepaalt dat de opdracht tot vervolging van een Kamerlid " \
            u"alleen door de regering of de Tweede Kamer kan worden " \
            u"gegeven.\n" \
            u"Voldoende gronden\n" \
            u" Van Miltenburg maakte donderdag bekend dat " \
            u"de\xa0onderzoekscommissie moet\xa0onderzoeken\xa0of er " \
            u"voldoende gronden zijn om tot vervolging over te gaan. " \
            u"Van Miltenburg zei niet te weten wie van de " \
            u"fractieleiders gelekt heeft. \"Door het OM is geen " \
            u"inhoudelijke informatie overgedragen over deze zaak. Noch " \
            u"de kamer, noch het presidium, noch de Kamervoorzitter " \
            u"beschikt over het dossier.\"\n\n" \
            u" Zij zal later op de avond een " \
            u"brief sturen naar de Tweede Kamer met nadere details over " \
            u"het onderzoek. Volgende week stemmen de Kamerleden over " \
            u"de samenstelling en de taakopdracht van de " \
            u"onderzoekscommissie.\n" \
            u"Aanleiding\n" \
            u" Aanleiding is de rel die " \
            u"vorig jaar speelde rond minister van Binnenlandse Zaken " \
            u"Ronald Plasterk en de aangifte die vervolgens werd gedaan " \
            u"door VVD-fractievoorzitter Halbe Zijlstra in zijn rol als " \
            u"voorzitter van de zogeheten commissie-Stiekem.\n" \
            u"In 2014 kwam Plasterk in grote\xa0politieke problemen\xa0doordat hij de " \
            u"Amerikanen verweet 1,8 miljoen tapgegevens\xa0te hebben " \
            u"opgehaald\xa0in Nederland. In werkelijkheid bleek dat " \
            u"Nederland deze taps zelf had uitgevoerd en geleverd aan " \
            u"de Amerikanen.\n" \
            u"Hij zou de Kamer hierover echter niet " \
            u"direct\xa0hebben ge\xefnformeerd toen hij zijn fout " \
            u"ontdekte.\xa0In de Kamer kreeg hij van een groot deel " \
            u"van\xa0de oppositie daarom een motie van wantrouwen aan " \
            u"de broek, inclusief van toenmalig gedoogpartner D66.\xa0\n" \
            u"Het zorgde voor een behoorlijke ruzie tussen PvdA-leider " \
            u"Diederik Samsom en D66-leider Alexander Pechtold. Vlak na " \
            u"het debat bleek waarom.\n" \
            u"Commissie-Stiekem\n" \
            u" NRC\xa0wist te melden dat de Commissie voor de Inlichtingen- " \
            u"en Veiligheidsdiensten, oftewel de commissie-Stiekem, wel " \
            u"degelijk eerder vertrouwelijk was ge\xefnformeerd over de " \
            u"werkelijke herkomst van de taps.\n" \
            u"En aangezien lekken uit deze commissie strafbaar is " \
            u"deed Zijlstra aangifte. Nu, ruim anderhalf jaar later, " \
            u"komt het Openbaar Ministerie er pas achter dat het niet " \
            u"bevoegd is om te beslissen over de vervolging van een " \
            u"Kamerlid.\xa0\n" \
            u"Wel zijn er aanwijzingen dat \xe9\xe9n of " \
            u"meerdere fractievoorzitters zich mogelijk schuldig hebben " \
            u"gemaakt aan een ambtsmisdrijf, zo liet het OM " \
            u"weten.\n" \
            u"Presidium\n" \
            u" Daarom is het dossier\xa0overgedragen aan " \
            u"het presidium, het orgaan waar bijna alle fracties en de " \
            u"Kamervoorzitter in zijn vertegenwoordigd.\xa0\n" \
            u"Een besluit om " \
            u"tot vervolging over te gaan kan grote gevolgen hebben, " \
            u"aangezien \xe9\xe9n of meerdere fractievoorzitters dan " \
            u"voor de Hoge Raad zullen moeten verschijnen.\n"

        self.assertEquals(parsed_article.body, expected)
