import os
from datetime import datetime

from django.test import TestCase, override_settings
from django.utils._os import upath

import pytz
import responses

from ..metro import MetroParser

TEST_DIR = os.path.join(os.path.dirname(upath(__file__)), 'data')


class MetroParserTests(TestCase):
    maxDiff = None

    def setUp(self):
        self.timezone = pytz.timezone("Europe/Amsterdam")
        super(MetroParserTests, self).setUp()

    @responses.activate
    @override_settings(NEWS_SOURCES=['news.parsers.metro.MetroParser', ])
    def test_metro_urls(self):
        page_name = 'www_metronieuws_nl'
        page_path = os.path.join(TEST_DIR, page_name)
        page_file = open(page_path, 'rb')

        responses.add(responses.GET, 'http://www.metronieuws.nl',
                      body=page_file.read(), status=200,
                      content_type='text/html')

        urls = MetroParser.request_urls()

        expected = set([
        'http://www.metronieuws.nl/nieuws/rotterdam/2016/03/mevlana-moskee-wil-bushalte-voor-de-deur',
        'http://www.metronieuws.nl/nieuws/koffiepauze/2016/03/vluchteling-woont-al-een-jaar-op-vliegveld',
        'http://www.metronieuws.nl/nieuws/koffiepauze/2016/03/veteranen-met-ptsd-krijgen-puppies',
        'http://www.metronieuws.nl/nieuws/buitenland/2016/03/frankrijk-verwacht-snelle-uitlevering-abdeslam',
        'http://www.metronieuws.nl/nieuws/showbizz/2016/03/michael-jacksons-aap-krijgt-animatiefilm',
        'http://www.metronieuws.nl/nieuws/showbizz/2016/03/is-dit-de-nieuwe-one-direction',
        'http://www.metronieuws.nl/nieuws/koffiepauze/2016/03/starbucks-voor-de-rechter-om-gebrek-aan-koffie',
        'http://www.metronieuws.nl/nieuws/binnenland/2016/03/kat-zit-al-dagen-vast-in-dakgoot',
        'http://www.metronieuws.nl/nieuws/amsterdam/2016/03/club-capital-pasen-bij-het-foodfestival-amsterdam',
        'http://www.metronieuws.nl/nieuws/buitenland/2016/03/protesten-brazilie-hoogste-rechter-doet-uitspraak',
        'http://www.metronieuws.nl/nieuws/showbizz/2016/03/blauwe-pyjama-nodig-peter-jan-rens-veilt-zn-zooi',
        'http://www.metronieuws.nl/nieuws/koffiepauze/2016/03/het-eerste-dat-deze-dove-vrouw-hoort-is-een-aanzoek',
        'http://www.metronieuws.nl/nieuws/buitenland/2016/03/tiener-dood-per-ongeluk-vriend-met-pistool',
        'http://www.metronieuws.nl/nieuws/binnenland/2016/03/prijs-treinkaartje-moet-alsnog-omlaag',
        'http://www.metronieuws.nl/nieuws/buitenland/2016/03/doden-en-gewonden-bij-zelfmoordaanslag-in-istanboel',
        'http://www.metronieuws.nl/nieuws/binnenland/2016/03/62000-paaltjes-vervangen-voor-nieuwe-betaalwijze-ov',
        'http://www.metronieuws.nl/nieuws/koffiepauze/2016/03/hond-met-twee-snuiten-gered-dankzij-viral-video',
        'http://www.metronieuws.nl/nieuws/showbizz/2016/03/youtube-sterren-stuktv-hebben-nu-1-miljoen-abonnees',
        'http://www.metronieuws.nl/nieuws/rotterdam/2016/03/ns-regelt-feyenoordbus-als-vervangend-vervoer',
        'http://www.metronieuws.nl/nieuws/koffiepauze/2016/03/pasgetrouwd-stel-viert-huwelijk-met-videoclip',
        'http://www.metronieuws.nl/nieuws/extra/2016/03/wetenschap-wil-12000-jaar-oude-pup-tot-leven-wekken',
        'http://www.metronieuws.nl/nieuws/buitenland/2016/03/vliegtuig-stort-neer-op-russisch-vliegveld',
        'http://www.metronieuws.nl/nieuws/binnenland/2016/03/het-wordt-een-zonnig-paasweekend',
        'http://www.metronieuws.nl/nieuws/amsterdam/2016/03/club-capital-blooker',
        'http://www.metronieuws.nl/nieuws/extra/2016/03/porsche-rijden-kan-zo-verslavend-zijn-als-chocolade',
        'http://www.metronieuws.nl/nieuws/binnenland/2016/03/oproep-voor-gestolen-tas-met-herinnering-aan-moeder',
        'http://www.metronieuws.nl/nieuws/buitenland/2016/03/veroorzaken-rubberkorrels-in-kunstgras-kanker',
        'http://www.metronieuws.nl/nieuws/binnenland/2016/03/bekend-politiepaard-eric-30-overleden',
        'http://www.metronieuws.nl/nieuws/rotterdam/2016/03/gratis-compost-voor-rotterdammers-met-groene-vingers',
        'http://www.metronieuws.nl/nieuws/buitenland/2016/03/nieuwe-klopjacht-op-abdeslam-in-molenbeek',
        'http://www.metronieuws.nl/nieuws/koffiepauze/2016/03/supermarkt-geeft-wanhopige-winkeldief-een-baan',
        'http://www.metronieuws.nl/nieuws/binnenland/2016/03/zaak-wilders-een-overzicht',
        'http://www.metronieuws.nl/nieuws/buitenland/2016/03/derde-verdachte-gearresteerd-in-molenbeek',
        'http://www.metronieuws.nl/nieuws/extra/2016/03/slapende-man-wordt-wakker-van-knabbelende-vos',
        'http://www.metronieuws.nl/nieuws/binnenland/2016/03/nog-een-keertje-winkelen-bij-de-vd',
        'http://www.metronieuws.nl/nieuws/koffiepauze/2016/03/hond-wacht-nog-steeds-op-overleden-baasje',
        'http://www.metronieuws.nl/nieuws/amsterdam/2016/03/amsterdam-krijgt-iconisch-skydeck',
        'http://www.metronieuws.nl/nieuws/rotterdam/2016/03/man-vraagt-de-weg-en-wordt-beroofd',
        'http://www.metronieuws.nl/nieuws/amsterdam/2016/03/ho-hotels',
        'http://www.metronieuws.nl/nieuws/showbizz/2016/03/nieuw-programma-jinek-voor-amerikaanse-verkiezingen',
        'http://www.metronieuws.nl/nieuws/amsterdam/2016/03/achterhuis-als-escaperoom-doet-veel-stof-opwaaien',
        'http://www.metronieuws.nl/nieuws/rotterdam/2016/03/zaterdagtip-eeterij-op-wielen',
        'http://www.metronieuws.nl/nieuws/buitenland/2016/03/ontsnapte-leeuw-uit-park-valt-man-aan',
        'http://www.metronieuws.nl/nieuws/rotterdam/2016/03/ook-bewoners-joliottoren-kampen-met-horrorliften',
        'http://www.metronieuws.nl/nieuws/binnenland/2016/03/grote-werkzaamheden-utrecht-centraal-in-paasweekend',
        'http://www.metronieuws.nl/nieuws/extra/2016/03/10-feitjes-over-het-grootste-cruiseschip-ter-wereld',
        'http://www.metronieuws.nl/nieuws/binnenland/2016/03/man-start-zoektocht-naar-zijn-weggegeven-hond',
        'http://www.metronieuws.nl/nieuws/rotterdam/2016/03/feyenoordsupporters-boos-om-kaarten-op-marktplaats',
        ])

        self.assertEquals(urls, expected)

    def test_metro_binnenland(self):
        """
        http://www.metronieuws.nl/nieuws/binnenland/2016/03/sapjes-en-fris-stijgen-sneller-in-prijs-dan-alcohol
        """

        article_name = 'www_metronieuws_nl_nieuws_binnenland_2016_03_sapjes-en-fris-stijgen-sneller-in-prijs-dan-alcohol'
        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = MetroParser.parse_new_version('', article_file.read())

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

        self.assertEquals(expected, parsed_article.get('content'))

        expected_date = self.timezone.localize(datetime(2016, 3, 10, 16, 42))

        self.assertEquals(parsed_article.get('date'), expected_date)

    def test_metra_extra(self):
        article_name = 'www_metronieuws_nl_nieuws_extra_2016_03_wetenschappers-ontdekken-perfecte-suikervervanger'

        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = MetroParser.parse_new_version('', article_file.read())

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

        self.assertEquals(expected, parsed_article.get('content'))

        expected_date = self.timezone.localize(datetime(2016, 3, 11, 22, 43))

        self.assertEquals(parsed_article.get('date'), expected_date)
