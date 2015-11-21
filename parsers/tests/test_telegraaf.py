from django.test import TestCase

import os
from django.utils._os import upath

from ..telegraaf import TelegraafParser


TEST_DIR = os.path.join(os.path.dirname(upath(__file__)), 'data')


class TelegraafParserTests(TestCase):
    maxDiff = None

    def test_telegraaf_buitenland(self):
        """
        http://www.telegraaf.nl/buitenland/24775234/__Dreiging_met_bommen_Belgie__.html
        """
        article_name = 'www_telegraaf_nl_buitenland_24775234_' \
                       '__Dreiging_met_bommen_Belgie__.html'
        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = TelegraafParser('', html=article_file.read())

        expected = \
            u'De dreiging in Brussel betreft een concrete dreiging van ' \
            u'aanslagen met wapens en explosieven, te vergelijken met ' \
            u'de aanslagen in Parijs. Dat zei de Belgische premier ' \
            u'Charles Michel zaterdag tijdens een persconferentie.\n' \
            u'Hij reageerde op het verhogen van het dreigingsniveau in ' \
            u'het Brussels Gewest van 3 naar 4, het hoogste niveau. ' \
            u'Waar de dreiging vandaan komt, wilde Michel niet zeggen. ' \
            u'De dreiging is volgens de premier vooral gericht op de ' \
            u'winkelstraten, het openbaar vervoer en in het algemeen ' \
            u'evenementen waar veel volk op af komt.\n' \
            u'De regering heeft vier maatregelen genomen: het ' \
            u'afgelasten van grote evenementen, het stilleggen van het ' \
            u'metroverkeer, en meer politie en militairen op straat. ' \
            u'Ten slotte is er een telefoonnummer geopend waar ' \
            u'Brusselaars informatie en advies kunnen krijgen.\n' \
            u'De maatregelen gelden volgens Michel vooralsnog tot ' \
            u'zondagmiddag. Dan maakt antiterreurdienst OCAD een nieuwe ' \
            u'inschatting van de veiligheidsssituatie en komt opnieuw ' \
            u'de Belgische Veiligheidsraad bijeen. Daarin hebben ' \
            u'behalve de premier ook de ministers van Binnenlandse ' \
            u'Zaken, Justitie, Defensie en Buitenlandse Zaken zitting.\n' \
            u'Het Belgische Co\xf6rdinatieorgaan voor de ' \
            u'Dreigingsanalyse (OCAD) raadde mensen in de nacht van ' \
            u'vrijdag op zaterdag aan veiligheidsmaatregelen te nemen. ' \
            u'Zo moeten ze plekken waar veel mensen samenkomen zoals ' \
            u'concerten, stations, luchthavens en drukke winkelstraten ' \
            u'vermijden. Ook moet de bevolking veiligheidscontroles ' \
            u'respecteren en geen geruchten verspreiden, maar alleen ' \
            u'informatie van overheden en de politie.\n' \
            u'Ook het ministerie van Buitenlandse Zaken in Den Haag ' \
            u'heeft het reisadvies naar Belgi\xeb aangepast. Het ' \
            u'ministerie roept mensen daarom op plaatsen te vermijden ' \
            u'waar veel mensen komen en altijd instructies van de ' \
            u'autoriteiten op te volgen.\n' \
            u'Overzicht stilgelegde activiteiten\n' \
            u'In het Vlaams parlement in Brussel zijn alle activiteiten ' \
            u'zaterdag afgelast vanwege het dreigingsniveau. Ook het ' \
            u'bezoekerscentrum van het Europees Parlement, het ' \
            u'Parlamentarium, blijft zaterdag dicht.\n' \
            u'Een belangrijke attractie in de Belgische hoofdstad, het ' \
            u'Atomium, gaat zaterdag ook niet open in verband met de ' \
            u'afkondiging van het het hoogste terreuralarm. Dat was ' \
            u'acht jaar geleden voor het laatst van kracht in Brussel.\n' \
            u'Veel musea blijven dit weekend gesloten, meldt de ' \
            u'Museumraad van de Belgische hoofdstad. Onder meer de ' \
            u'Koninklijke Musea voor Schone Kunsten en voor Kunst en ' \
            u'Geschiedenis blijven zaterdag en zondag dicht. Ook het ' \
            u'Muziekinstrumentenmuseum, het Museum voor ' \
            u'Natuurwetenschappen en de Koninklijke Bibliotheek van ' \
            u'Belgi\xeb houden de deuren gesloten. Ook Train World, de ' \
            u'grote Kinepolis-bioscoop, het Museum van Elsene en het ' \
            u'Kindermuseum gaan zaterdag niet open. De raad zegt ervan ' \
            u'overtuigd te zijn "dat de bezoekers begrip hebben voor ' \
            u'deze preventieve maatregel".\n' \
            u'De Vrije Universiteit Brussel heeft alle lessen en ' \
            u'evenementen op haar campussen gecanceld. Diverse muzikale ' \
            u'evenementen gaan niet door. Ook zijn alle ' \
            u'hockeywedstrijden afgelast. De voetbalwedstrijd ' \
            u'Lokeren-Anderlecht is afgelast wegens te weinig politie.\n' \
            u'Het metroverkeer is volledig stilgelegd, maar de trams en ' \
            u'bussen rijden wel. Op het treinstation Schuman, het ' \
            u'centrum van de Europese instellingen, stoppen geen ' \
            u'treinen.\n' \
            u'Het vliegverkeer op Zaventem, de luchthaven van Brussel, ' \
            u'verloopt zaterdag vooralsnog wel zoals gepland. Brussels ' \
            u'Airport neemt voorlopig geen extra maatregelen.\n'

        self.assertEquals(parsed_article.body, expected)
