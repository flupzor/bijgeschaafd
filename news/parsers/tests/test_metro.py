from django.test import TestCase

import os
from django.utils._os import upath

from ..metro import MetroParser


TEST_DIR = os.path.join(os.path.dirname(upath(__file__)), 'data')


class MetroParserTests(TestCase):
    maxDiff = None

    def test_metro_binnenland(self):
        """
        http://www.metronieuws.nl/nieuws/binnenland/2016/03/sapjes-en-fris-stijgen-sneller-in-prijs-dan-alcohol
        """

        article_name = 'www_metronieuws_nl_nieuws_binnenland_2016_03_sapjes-en-fris-stijgen-sneller-in-prijs-dan-alcohol'
        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = MetroParser('', html=article_file.read())

        expected = \
        u"Mineraalwater, sap en frisdrank zijn de afgelopen vijf jaar flink " \
        u"in prijs gestegen: ruim 17 procent. Dat is aanzienlijk meer dan " \
        u"de algemene prijsstijging van goederen en diensten in Nederland. " \
        u"Die bedroeg 7,5 procent in de afgelopen 5 jaar. En het is ook " \
        u"flink meer in vergelijking met de prijsstijging van alcoholische " \
        u"dranken, die bedroeg 10 procent. Dat blijkt donderdag uit cijfers " \
        u"van CBS.\n" \
        u"Alcohol\n" \
        u"\u201eGeen goede ontwikkeling\u201d, stelt Wim van Dalen van " \
        u"STAP, het Nederlands Instituut voor alcoholbeleid. Liever had " \
        u"hij gezien dat de overheid de prijs van alcoholische dranken nog " \
        u"meer had opgeschroefd met accijnzen, zodat deze dranken in " \
        u"vergelijking met de niet-alcoholische dranken harder zouden " \
        u"stijgen in prijs.\n" \
        u"\u201eDat fris en water harder in prijs stijgen dan alcohol is " \
        u"een vreemd signaal\u201d, zegt Van Dalen.\n" \
        u"Belasting\n" \
        u"Een groot deel van de prijsstijging van niet-alcoholische " \
        u"dranken werd veroorzaakt door hogere verbruiksbelasting. Tot " \
        u"en met eind 2015 was de verbruiksbelasting op mineraalwater en " \
        u"vruchten- en groentesappen lager dan de belasting op frisdrank. " \
        u"Vanaf dit jaar is de verbruiksbelasting gelijkgesteld aan die " \
        u"op frisdrank. Tegelijkertijd is deze belasting, die speciaal " \
        u"gericht is op alcoholvrije dranken, verhoogd\n" \
        u"Maar ook alcoholische dranken stegen in prijs door onder " \
        u"andere belastingwijzigingen in de afgelopen vijf jaar. " \
        u"\u201eVooropgesteld ben ik blij met de accijns op alcohol, " \
        u"anders waren alcoholische dranken helemaal spotgoedkoop\u201d, " \
        u"zegt Van Dalen. \u201eMaar de overheid zou veel meer moeten " \
        u"sturen in prijs als je ziet dat de reguliere prijsstijging " \
        u"van alcoholische dranken veel minder snel stijgt dan van " \
        u"bijvoorbeeld sap en water.\u201d\n" \
        u"Dat iemand in de supermarkt bewust kiest voor een flesje sap " \
        u"in plaats van een biertje vanwege de prijs, dat denkt Van " \
        u"Dalen niet. \u201eMaar prijzen zijn onbewust zeker " \
        u"belangrijk voor consumentengedrag. Het was positiever " \
        u"geweest als die prijsstijging van sap\xa0en alcohol andersom " \
        u"was geweest.\"\xa0\n" \
        u"Mineraalwater\n" \
        u"Van alle dranken die verkocht worden in supermarkten en " \
        u"slijterijen steeg de prijs van mineraalwater het meest. Een " \
        u"fles of pak mineraalwater werd in vijf jaar tijd 30 procent " \
        u"duurder. Zorgelijk voor onze gezondheid? Niet echt, vindt " \
        u"Stef Kremers, Hoogleraar Preventie van obesitas. \u201eWater " \
        u"komt ook uit de kraan. Ik denk niet dat mensen minder water " \
        u"gaan drinken, omdat mineraalwater in de supermarkt duurder " \
        u"is geworden.\u201d \xa0Het Voedingscentrum reageert: " \
        u"\u201eJammer dat mineraalwater nu in het rijtje van sappen " \
        u"en frisdrank staat wat betreft prijsverhoging, maar wij " \
        u"bevelen ook kraanwater aan.\"\xa0\n"

        self.assertEquals(expected, parsed_article.body)

    def test_metra_extra(self):
        article_name = 'www_metronieuws_nl_nieuws_extra_2016_03_wetenschappers-ontdekken-perfecte-suikervervanger'

        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = MetroParser('', html=article_file.read())

        expected = \
        u"Suiker is alweer tijden een onderwerp van discussie. Menig " \
        u"expert meldt dat het witte spul ontzettend ongezond is. Maar " \
        u"er is hoop: Belgische wetenschappers denken nu de perfecte " \
        u"vervanger gevonden te hebben, meldt RTL Z op hun website.\n" \
        u"De suikermolecuul die volgens de wetenschappers op ten duur " \
        u"normale suiker kan vervangen heet Kojibiose. Nieuw is het " \
        u"niet; kojibiose zit nu al in kleine hoeveelheden in Japanse " \
        u"rijstwijn. Het molecuul eruit toveren bleek echter nog een " \
        u"hele klus.\n" \
        u"En dat was niet het enige probleem: toen Gentse onderzoekers " \
        u"eindelijk een manier hadden gevonden om genoeg van het goedje " \
        u"te verzamelen bleek het zo\u2019n 1 miljoen euro per kilo (!) " \
        u"te kosten. Inmiddels hebben ze het enzym dat kojibiose " \
        u"produceert dusdanig weten te verbeteren dat het betaalbaarder " \
        u"is geworden.\n" \
        u"Droomgoedje?\n" \
        u"Kojibiose lijkt een droomgoedje: het heeft geen negatief " \
        u"effect op je gebit, is net zo zoet als gewone suiker en " \
        u"als toppunt blijkt dat kojibiose weinig calorie\xebn heeft!" \
        u" Het zou zelfs een goed stofje voor je darmflora zijn, al " \
        u"moet dat laatste nog bewezen worden. Het enige nadeel is " \
        u"dat de suikervervanger nogal wat gasvorming veroorzaakt. " \
        u"Mocht je op ten duur dus een kopje thee met kojibiose " \
        u"drinken, waarschuw je partner dan maar alvast\u2026\xa0\n"

        self.assertEquals(expected, parsed_article.body)

