from django.test import TestCase, override_settings
from datetime import datetime
import os
import pytz
from django.utils._os import upath

from ..nosnl import NOSNLParser
import responses


TEST_DIR = os.path.join(os.path.dirname(upath(__file__)), 'data')


class NOSNLParserTests(TestCase):
    maxDiff = None

    def setUp(self):
        self.timezone = pytz.timezone("Europe/Amsterdam")
        super(NOSNLParserTests, self).setUp()

    @responses.activate
    @override_settings(NEWS_SOURCES=['news.parsers.nosnl.NOSNLParser', ])
    def test_nu_nl_urls(self):
        page_name = 'www_nos_nl'
        page_path = os.path.join(TEST_DIR, page_name)
        page_file = open(page_path, 'rb')

        responses.add(responses.GET, 'http://www.nos.nl',
                      body=page_file.read(), status=200,
                      content_type='text/html')

        urls = NOSNLParser.request_urls()

        expected = set([
        'http://www.nos.nl/artikel/2093795-milaan-sanremo-gehinderd-door-aardverschuiving.html',
        'http://www.nos.nl/artikel/2093716-62-doden-bij-vliegtuigongeluk-in-rusland.html',
        'http://www.nos.nl/artikel/2093810-luchtaanvallen-op-is-steden-raqqa-en-palmyra.html',
        'http://www.nos.nl/artikel/2093799-turkije-waakzaam-in-aanloop-naar-koerdische-feestdag.html',
        'http://www.nos.nl/artikel/2093686-vrachtauto-verliest-ruim-150-kratten-bier-op-rotonde-helmond.html',
        'http://www.nos.nl/artikel/2093752-stil-leven-sterke-ontmoeting-tussen-armando-en-vanfleteren.html',
        'http://www.nos.nl/artikel/2093808-fanara-wint-laatste-reuzenslalom-van-het-seizoen.html',
        'http://www.nos.nl/artikel/2093598-eu-roept-om-sancties-tegen-moskou-krim-annexatie-twee-jaar-geleden.html',
        'http://www.nos.nl/artikel/2092834-sponsor-wust-gaat-door-tot-spelen-2018.html',
        'http://www.nos.nl/artikel/2093789-griekenland-zit-nog-met-duizend-vragen.html',
        'http://www.nos.nl/artikel/2093785-lid-clientenraad-ziekenhuis-heerlen-weg-na-intimidatie.html',
        'http://www.nos.nl/artikel/2093400-michelle-obama-brengt-single-uit-voor-het-goede-doel.html',
        'http://www.nos.nl/artikel/2093626-wie-is-terreurverdachte-salah-abdeslam.html',
        'http://www.nos.nl/artikel/2093726-geld-maakt-niet-gelukkig-tenzij-je-arm-bent.html',
        'http://www.nos.nl/artikel/2093793-in-molenbeek-wist-iedereen-waar-abdeslam-was.html',
        'http://www.nos.nl/artikel/2093186-hond-redt-bejaarde-duitser-van-de-bevriezingsdood.html',
        'http://www.nos.nl/artikel/2093585-koning-opent-wildlands-adventure-zoo-in-emmen.html',
        'http://www.nos.nl/artikel/2093748-willem-alexander-gaf-zichzelf-een-onmogelijke-opdracht.html',
        'http://www.nos.nl/artikel/2093618-feyenoord-wil-een-nieuw-stadion-langs-de-maas.html',
        'http://www.nos.nl/artikel/2093732-williams-en-azarenka-naar-finale-indian-wells.html',
        'http://www.nos.nl/artikel/2093783-shiffrin-onderstreept-klasse-in-laatste-wb-slalom.html',
        'http://www.nos.nl/artikel/2093803-frikadellenbakker-van-duinen-wil-via-roda-slagen-in-dusseldorf.html',
        'http://www.nos.nl/artikel/2093770-scoren-in-de-kuip-heeft-puur-te-maken-met-kwaliteit.html',
        'http://www.nos.nl/artikel/2093433-google-wil-af-van-maker-van-terminators.html',
        'http://www.nos.nl/artikel/2093755-terreurverdachte-abdeslam-verzet-zich-tegen-uitlevering.html',
        'http://www.nos.nl/artikel/2093792-terreurdreigingsniveau-drie-blijft-van-kracht-in-belgie.html',
        'http://www.nos.nl/artikel/2093764-doden-en-gewonden-bij-aanslag-in-centrum-istanbul.html',
        'http://www.nos.nl/artikel/2093794-politie-treft-man-aan-die-nog-170-000-euro-aan-boetes-moet-betalen.html',
        'http://www.nos.nl/artikel/2093782-na-taart-in-milaan-wil-cancellara-champagne-in-sanremo.html',
        'http://www.nos.nl/artikel/2093707-fabeltjeskrant-keert-terug-in-digitale-versie.html',
        'http://www.nos.nl/artikel/2093767-rossi-twee-jaar-langer-bij-yamaha.html',
        'http://www.nos.nl/artikel/2093768-the-passion-in-new-orleans-a-live-2-hour-epic-musical-event.html',
        'http://www.nos.nl/artikel/2093453-verdronken-hond-na-5-weken-teruggevonden.html',
        'http://www.nos.nl/artikel/2093813-hennis-er-moet-zeker-2-miljard-bij-voor-defensie.html',
        'http://www.nos.nl/artikel/2093496-ook-b-staal-schaatser-koelizjnikov-positief.html',
        'http://www.nos.nl/artikel/2093737-volkskrant-kreeg-ook-pleitnota-wilders-aangeboden.html',
        'http://www.nos.nl/artikel/2093778-voorman-noorse-broeders-vast-voor-verduistering-acht-miljoen-euro.html',
        'http://www.nos.nl/artikel/2093345-speciale-app-waarschuwt-olympiers-in-rio-voor-gevaar.html',
        'http://www.nos.nl/artikel/2093776-onderzeeer-in-poolgebied-breekt-door-ijs-heen.html',
        'http://www.nos.nl/artikel/2093744-veel-geheime-schikkingen-over-seksueel-misbruik-rk-kerk.html',
        'http://www.nos.nl/artikel/2093282-privacyorganisaties-ontevreden-over-datadeal-europa-vs.html',
        'http://www.nos.nl/artikel/2093502-azarenka-verder-na-double-bagel-in-indian-wells.html',
        'http://www.nos.nl/artikel/2093757-tweede-inzittende-na-auto-ongeluk-sneek-overleden.html',
        'http://www.nos.nl/artikel/2093769-50plus-wil-gedoe-achter-zich-laten.html',
        'http://www.nos.nl/artikel/2093704-djokovic-kraakt-sterke-tsonga-nadal-langs-nishikori.html',
        'http://www.nos.nl/artikel/2093774-samba-sam-is-terug-larsson-laat-friesland-swingen.html',
        'http://www.nos.nl/artikel/2093807-golfer-chowrasia-nieuwe-leider-in-india.html',
        'http://www.nos.nl/artikel/2093432-mabel-en-beatrix-bij-uitreiking-friso-prijs.html',
        'http://www.nos.nl/artikel/2093631-voor-het-eerst-meer-dan-8-miljoen-auto-s-op-de-weg.html',
        'http://www.nos.nl/artikel/2093750-oud-v-d-ers-nog-even-achter-de-toonbank-bij-leegverkoop.html',
        'http://www.nos.nl/artikel/2092942-koelizjnikov-reageert-ik-denk-niet-aan-zelfmoord.html',
        'http://www.nos.nl/artikel/2093741-ik-laat-me-niet-nog-keer-door-de-daders-tot-zwijgen-dwingen.html',
        'http://www.nos.nl/artikel/2093788-f1-teams-willen-snel-aanpassing-van-waardeloze-kwalificatieopzet.html',
        'http://www.nos.nl/artikel/2093797-noc-nsf-baas-hendriks-blij-met-terugkeer-bonnes-bij-judobond.html',
        ])

        self.assertEquals(urls, expected)

    def test_nos_nl(self):
        """
        http://nos.nl/artikel/2069130-dodental-parijs-op-129-maar-zal-nog-stijgen.html
        """

        article_name = "www_nos_nl_artikel_2069130-dodental-parijs-op-129" \
                       "-maar-zal-nog-stijgen.html"

        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = NOSNLParser.parse_new_version('', article_file.read())

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

        self.assertEquals(parsed_article.get('content'), expected)

        expected_date = self.timezone.localize(datetime(2015, 11, 14, 19, 28, 38))

        self.assertEquals(parsed_article.get('date'), expected_date)

