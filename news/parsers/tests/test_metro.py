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

        self.assertEqual(urls, expected)

    def test_metro_binnenland(self):
        """
        http://www.metronieuws.nl/nieuws/binnenland/2016/03/sapjes-en-fris-stijgen-sneller-in-prijs-dan-alcohol
        """

        article_name = 'www_metronieuws_nl_nieuws_binnenland_2016_03_sapjes-en-fris-stijgen-sneller-in-prijs-dan-alcohol'
        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = MetroParser.parse_new_version('', article_file.read())

        expected = \
        "Mineraalwater, sap en frisdrank zijn de afgelopen vijf jaar flink " \
        "in prijs gestegen: ruim 17 procent. Dat is aanzienlijk meer dan " \
        "de algemene prijsstijging van goederen en diensten in Nederland. " \
        "Die bedroeg 7,5 procent in de afgelopen 5 jaar. En het is ook " \
        "flink meer in vergelijking met de prijsstijging van alcoholische " \
        "dranken, die bedroeg 10 procent. Dat blijkt donderdag uit cijfers " \
        "van CBS.\n" \
        "Alcohol\n" \
        "\u201eGeen goede ontwikkeling\u201d, stelt Wim van Dalen van " \
        "STAP, het Nederlands Instituut voor alcoholbeleid. Liever had " \
        "hij gezien dat de overheid de prijs van alcoholische dranken nog " \
        "meer had opgeschroefd met accijnzen, zodat deze dranken in " \
        "vergelijking met de niet-alcoholische dranken harder zouden " \
        "stijgen in prijs.\n" \
        "\u201eDat fris en water harder in prijs stijgen dan alcohol is " \
        "een vreemd signaal\u201d, zegt Van Dalen.\n" \
        "Belasting\n" \
        "Een groot deel van de prijsstijging van niet-alcoholische " \
        "dranken werd veroorzaakt door hogere verbruiksbelasting. Tot " \
        "en met eind 2015 was de verbruiksbelasting op mineraalwater en " \
        "vruchten- en groentesappen lager dan de belasting op frisdrank. " \
        "Vanaf dit jaar is de verbruiksbelasting gelijkgesteld aan die " \
        "op frisdrank. Tegelijkertijd is deze belasting, die speciaal " \
        "gericht is op alcoholvrije dranken, verhoogd\n" \
        "Maar ook alcoholische dranken stegen in prijs door onder " \
        "andere belastingwijzigingen in de afgelopen vijf jaar. " \
        "\u201eVooropgesteld ben ik blij met de accijns op alcohol, " \
        "anders waren alcoholische dranken helemaal spotgoedkoop\u201d, " \
        "zegt Van Dalen. \u201eMaar de overheid zou veel meer moeten " \
        "sturen in prijs als je ziet dat de reguliere prijsstijging " \
        "van alcoholische dranken veel minder snel stijgt dan van " \
        "bijvoorbeeld sap en water.\u201d\n" \
        "Dat iemand in de supermarkt bewust kiest voor een flesje sap " \
        "in plaats van een biertje vanwege de prijs, dat denkt Van " \
        "Dalen niet. \u201eMaar prijzen zijn onbewust zeker " \
        "belangrijk voor consumentengedrag. Het was positiever " \
        "geweest als die prijsstijging van sap\xa0en alcohol andersom " \
        "was geweest.\"\xa0\n" \
        "Mineraalwater\n" \
        "Van alle dranken die verkocht worden in supermarkten en " \
        "slijterijen steeg de prijs van mineraalwater het meest. Een " \
        "fles of pak mineraalwater werd in vijf jaar tijd 30 procent " \
        "duurder. Zorgelijk voor onze gezondheid? Niet echt, vindt " \
        "Stef Kremers, Hoogleraar Preventie van obesitas. \u201eWater " \
        "komt ook uit de kraan. Ik denk niet dat mensen minder water " \
        "gaan drinken, omdat mineraalwater in de supermarkt duurder " \
        "is geworden.\u201d \xa0Het Voedingscentrum reageert: " \
        "\u201eJammer dat mineraalwater nu in het rijtje van sappen " \
        "en frisdrank staat wat betreft prijsverhoging, maar wij " \
        "bevelen ook kraanwater aan.\"\xa0\n"

        self.assertEqual(expected, parsed_article.get('content'))

        expected_date = self.timezone.localize(datetime(2016, 3, 10, 16, 42))

        self.assertEqual(parsed_article.get('date'), expected_date)

    def test_metra_extra(self):
        article_name = 'www_metronieuws_nl_nieuws_extra_2016_03_wetenschappers-ontdekken-perfecte-suikervervanger'

        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = MetroParser.parse_new_version('', article_file.read())

        expected = \
        "Suiker is alweer tijden een onderwerp van discussie. Menig " \
        "expert meldt dat het witte spul ontzettend ongezond is. Maar " \
        "er is hoop: Belgische wetenschappers denken nu de perfecte " \
        "vervanger gevonden te hebben, meldt RTL Z op hun website.\n" \
        "De suikermolecuul die volgens de wetenschappers op ten duur " \
        "normale suiker kan vervangen heet Kojibiose. Nieuw is het " \
        "niet; kojibiose zit nu al in kleine hoeveelheden in Japanse " \
        "rijstwijn. Het molecuul eruit toveren bleek echter nog een " \
        "hele klus.\n" \
        "En dat was niet het enige probleem: toen Gentse onderzoekers " \
        "eindelijk een manier hadden gevonden om genoeg van het goedje " \
        "te verzamelen bleek het zo\u2019n 1 miljoen euro per kilo (!) " \
        "te kosten. Inmiddels hebben ze het enzym dat kojibiose " \
        "produceert dusdanig weten te verbeteren dat het betaalbaarder " \
        "is geworden.\n" \
        "Droomgoedje?\n" \
        "Kojibiose lijkt een droomgoedje: het heeft geen negatief " \
        "effect op je gebit, is net zo zoet als gewone suiker en " \
        "als toppunt blijkt dat kojibiose weinig calorie\xebn heeft!" \
        " Het zou zelfs een goed stofje voor je darmflora zijn, al " \
        "moet dat laatste nog bewezen worden. Het enige nadeel is " \
        "dat de suikervervanger nogal wat gasvorming veroorzaakt. " \
        "Mocht je op ten duur dus een kopje thee met kojibiose " \
        "drinken, waarschuw je partner dan maar alvast\u2026\xa0\n"

        self.assertEqual(expected, parsed_article.get('content'))

        expected_date = self.timezone.localize(datetime(2016, 3, 11, 22, 43))

        self.assertEqual(parsed_article.get('date'), expected_date)
