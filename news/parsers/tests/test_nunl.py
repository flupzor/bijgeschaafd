import os
from datetime import datetime

from django.test import TestCase, override_settings
from django.utils._os import upath

import pytz
import responses
from news.parsers.exceptions import NotInteresting

from ..nunl import NuNLParser

TEST_DIR = os.path.join(os.path.dirname(upath(__file__)), 'data')


class NuNLParserTests(TestCase):
    maxDiff = None

    def setUp(self):
        self.timezone = pytz.timezone("Europe/Amsterdam")
        super(NuNLParserTests, self).setUp()

    @responses.activate
    @override_settings(NEWS_SOURCES=['news.parsers.nunl.NuNLParser', ])
    def test_nu_nl_urls(self):
        page_name = 'www_nu_nl'
        page_path = os.path.join(TEST_DIR, page_name)
        page_file = open(page_path, 'rb')

        responses.add(responses.GET, 'http://www.nu.nl',
                      body=page_file.read(), status=200,
                      content_type='text/html')

        urls = NuNLParser.request_urls()

        expected = set([
        'http://www.nu.nl/economie/4232128/duitse-bank-wil-rente-heffen-bij-grote-som-spaargeld.html',
        'http://www.nu.nl/wetenschap/4231966/zwart-gat-bombardeert-aarde-met-straling-.html',
        'http://www.nu.nl/economie/4232143/verenigde-staten-voeren-importheffing-in-tata-steel-nederland.html',
        'http://www.nu.nl/economie/4231853/opnieuw-daalt-prijspeil-in-eurozone.html',
        'http://www.nu.nl/economie/4231987/britse-centrale-bank-verwacht-lagere-investeringen-bij-brexit.html',
        'http://www.nu.nl/gezondheid/4231912/artsen-willen-tabak-niet-meer-in-supermarkt.html',
        'http://www.nu.nl/achterklap/4232051/boer-frans-boer-zoekt-vrouw-vader-geworden-van-tweeling.html',
        'http://www.nu.nl/achterklap/4232241/vrouw-van-jamie-oliver-in-verwachting.html',
        'http://www.nu.nl/achterklap/4232232/blake-shelton-weerspreekt-roddels-ede.html',
        'http://www.nu.nl/internet/4232055/nieuwe-versie-ransomware-onkraakbaar.html',
        'http://www.nu.nl/algemeen/4232145/in-spanje-onderzoekt-gedrag-psv-supporters.html',
        'http://www.nu.nl/achterklap/4232182/iggy-azalea-druk-met-huwelijksvoorbereidingen.html',
        'http://www.nu.nl/algemeen/4232214/veel-meer-doden-dan-gedacht-aanval-markt-jemen.html',
        'http://www.nu.nl/economie/4231891/havenbedrijven-in-beroep-besluit-europese-commissie-belastingen.html',
        'http://www.nu.nl/politiek/4232059/kamervoorzitter-wil-mogelijk-extra-vragenuur.html',
        'http://www.nu.nl/tennis/4232089/federer-maakt-komende-week-in-miami-rentree.html',
        'http://www.nu.nl/media/4232093/britse-krant-the-guardian-schrapt-250-banen.html',
        'http://www.nu.nl/reizen/4232109/pretpark-universal-studios-krijgt-restaurant-met-willy-wonka-thema.html',
        'http://www.nu.nl/achterklap/4232210/bbc-presentator-rolf-harris-ontkent-nieuwe-gevallen-van-misbruik.html',
        'http://www.nu.nl/opmerkelijk/4232028/man-gooit-per-ongeluk-peperdure-trouwring-van-echtgenote-weg.html',
        'http://www.nu.nl/binnenland/4231135/twintig-tips-man-hoofd-achterliet-in-amsterdam.html',
        'http://www.nu.nl/games/4232091/pokemon-games-279-miljoen-keer-verkocht.html',
        'http://www.nu.nl/binnenland/4232008/apache-moet-voorzorgslanding-maken-in-weiland-foutmelding.html',
        'http://www.nu.nl/buitenland/4232097/rechter-brazilie-blokkeert-aanstelling-omstreden-oud-president.html',
        'http://www.nu.nl/apps/4232054/app-gaat-nederlandse-olympiers-in-rio-waarschuwen-gevaar.html',
        'http://www.nu.nl/politiek/4232048/rutte-ziet-geen-alternatieve-oplossing-eu-turkije-top.html',
        'http://www.nu.nl/binnenland/4231751/agent-schiet-met-mes-dreigende-man-dood-in-kwakel.html',
        'http://www.nu.nl/economie/4231852/winst-en-omzet-gasunie-gedaald-in-2015.html',
        'http://www.nu.nl/muziek/4232133/mumford--sons-en-the-national-werken-coveralbum-grateful-dead.html',
        'http://www.nu.nl/media/4232152/jan-slagter-niet-eens-met-kritiek-staatssecretaris-dekker.html',
        'http://www.nu.nl/dvn/4231682/staat-er-spel-tijdens-asieltop-met-eu-en-turkije.html',
        'http://www.nu.nl/belastingaangifte/4232060/wiebes-oneens-met-onvoldoende-belastingtelefoon.html',
        'http://www.nu.nl/buitenland/4231541/joran-van-sloot-zegt-schuldig-in-zaak-natalee-holloway.html',
        'http://www.nu.nl/ondernemen/4228901/britse-keten-wil-winkels-perry-sport-en-aktiesport-overnemen.html',
        'http://www.nu.nl/dieren/4232195/boord-geslagen-hond-vijf-weken-terecht.html',
        'http://www.nu.nl/internet/4232202/kickstarter-neemt-muziekdienst-drip.html',
        'http://www.nu.nl/vd/4231972/helft-nederlanders-deed-in-afgelopen-jaar-nog-aankoop-bij-vd.html',
        'http://www.nu.nl/algemeen/4232225/stille-tocht-onthoofde-nabil-amzieb-in-amsterdam.html',
        'http://www.nu.nl/opmerkelijk/4231903/inwoner-seattle-confronteert-dieven-en-haalt-gestolen-fietsen-terug.html',
        'http://www.nu.nl/dvn/4227806/we-weten-vondst-van-hoofd-in-amsterdam.html',
        'http://www.nu.nl/achterklap/4232212/vrouw-simon-keizer-kreeg-miskraam.html',
        'http://www.nu.nl/mobiel/4232183/windows-10-beschikbaar-gesteld-oudere-telefoons.html'])

        self.assertEqual(urls, expected)

    def test_nu_nl_lifeblog(self):
        """
        http://www.nu.nl/champions-league/4136168/reacties-psv-3-2-nederlaag-bij-cska-moskou-gesloten.html
        """
        article_name = 'www_nu_nl_champions-league_4136168_reacties' \
                       '-psv-3-2-nederlaag-bij-cska-moskou-gesloten.html'
        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        with self.assertRaises(NotInteresting):
            parsed_article = NuNLParser.parse_new_version('', article_file.read())

    def test_nu_nl_article(self):
        """
        http://www.nu.nl/politiek/4163338/bestuur-kamer-stelt-onderzoek-in-wegens-lekken-commissie-stiekem.html
        """

        article_name = 'www_nu_nl_politiek_4163338_bestuur-kamer-stelt-' \
                       'onderzoek-in-wegens-lekken-commissie-stiekem.html'

        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = NuNLParser.parse_new_version('', article_file.read())

        # Hint for a update: I used fold -s -w 58 and some regex
        expected = \
            "Het presidium, het dagelijks bestuur van de Tweede Kamer, " \
            "stelt een onderzoekscommissie in naar het lekken uit de " \
            "zogenoemde commissie-Stiekem. \n" \
            "Dat is donderdag bekendgemaakt door Kamervoorzitter Anouchka van " \
            "Miltenburg na afloop van een vergadering van het " \
            "presidium.\xa0\n" \
            "Eerder deze week werd bekend dat er aangifte is " \
            "gedaan wegens het lekken uit de\xa0Commissie voor de " \
            "Inlichtingen- en Veiligheidsdiensten, oftewel de " \
            "commissie-Stiekem,\xa0naar\xa0NRC Handelsblad. De " \
            "commissie-Stiekem\xa0bestaat uit de fractievoorzitters " \
            "van de gekozen partijen.\xa0Lekken uit deze commissie " \
            "geldt als een ambtsmisdrijf.\n" \
            "Woensdag liet het OM weten dat " \
            "zij de zaak, die al anderhalf jaar speelt, niet verder " \
            "behandelt en neerlegt bij de Kamer.\xa0De Grondwet " \
            "bepaalt dat de opdracht tot vervolging van een Kamerlid " \
            "alleen door de regering of de Tweede Kamer kan worden " \
            "gegeven.\n" \
            "Voldoende gronden\n" \
            "Van Miltenburg maakte donderdag bekend dat " \
            "de\xa0onderzoekscommissie moet\xa0onderzoeken\xa0of er " \
            "voldoende gronden zijn om tot vervolging over te gaan. " \
            "Van Miltenburg zei niet te weten wie van de " \
            "fractieleiders gelekt heeft. \"Door het OM is geen " \
            "inhoudelijke informatie overgedragen over deze zaak. Noch " \
            "de kamer, noch het presidium, noch de Kamervoorzitter " \
            "beschikt over het dossier.\"\n" \
            "Zij zal later op de avond een " \
            "brief sturen naar de Tweede Kamer met nadere details over " \
            "het onderzoek. Volgende week stemmen de Kamerleden over " \
            "de samenstelling en de taakopdracht van de " \
            "onderzoekscommissie.\n" \
            "Aanleiding\n" \
            "Aanleiding is de rel die " \
            "vorig jaar speelde rond minister van Binnenlandse Zaken " \
            "Ronald Plasterk en de aangifte die vervolgens werd gedaan " \
            "door VVD-fractievoorzitter Halbe Zijlstra in zijn rol als " \
            "voorzitter van de zogeheten commissie-Stiekem.\n" \
            "In 2014 kwam Plasterk in grote\xa0politieke problemen\xa0doordat hij de " \
            "Amerikanen verweet 1,8 miljoen tapgegevens\xa0te hebben " \
            "opgehaald\xa0in Nederland. In werkelijkheid bleek dat " \
            "Nederland deze taps zelf had uitgevoerd en geleverd aan " \
            "de Amerikanen.\n" \
            "Hij zou de Kamer hierover echter niet " \
            "direct\xa0hebben ge\xefnformeerd toen hij zijn fout " \
            "ontdekte.\xa0In de Kamer kreeg hij van een groot deel " \
            "van\xa0de oppositie daarom een motie van wantrouwen aan " \
            "de broek, inclusief van toenmalig gedoogpartner D66.\xa0\n" \
            "Het zorgde voor een behoorlijke ruzie tussen PvdA-leider " \
            "Diederik Samsom en D66-leider Alexander Pechtold. Vlak na " \
            "het debat bleek waarom.\n" \
            "Commissie-Stiekem\n" \
            "NRC\xa0wist te melden dat de Commissie voor de Inlichtingen- " \
            "en Veiligheidsdiensten, oftewel de commissie-Stiekem, wel " \
            "degelijk eerder vertrouwelijk was ge\xefnformeerd over de " \
            "werkelijke herkomst van de taps.\n" \
            "En aangezien lekken uit deze commissie strafbaar is " \
            "deed Zijlstra aangifte. Nu, ruim anderhalf jaar later, " \
            "komt het Openbaar Ministerie er pas achter dat het niet " \
            "bevoegd is om te beslissen over de vervolging van een " \
            "Kamerlid.\xa0\n" \
            "Wel zijn er aanwijzingen dat \xe9\xe9n of " \
            "meerdere fractievoorzitters zich mogelijk schuldig hebben " \
            "gemaakt aan een ambtsmisdrijf, zo liet het OM " \
            "weten.\n" \
            "Presidium\n" \
            "Daarom is het dossier\xa0overgedragen aan " \
            "het presidium, het orgaan waar bijna alle fracties en de " \
            "Kamervoorzitter in zijn vertegenwoordigd.\xa0\n" \
            "Een besluit om " \
            "tot vervolging over te gaan kan grote gevolgen hebben, " \
            "aangezien \xe9\xe9n of meerdere fractievoorzitters dan " \
            "voor de Hoge Raad zullen moeten verschijnen.\n"

        self.assertEqual(parsed_article.get('content'), expected)

        expected_date = self.timezone.localize(datetime(2015, 11, 12, 12, 7))

        self.assertEqual(parsed_article.get('date'), expected_date)

    def test_nu_nl_review(self):
        """
        www_nu_nl_reviews_4235935_review-trackmania-turbo-brengt-extreem-raceplezier-consoles.html
        """

        article_name = 'www_nu_nl_reviews_4235935_review-trackmania-turbo-' \
                       'brengt-extreem-raceplezier-consoles.html'

        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = NuNLParser.parse_new_version('', article_file.read())

        expected = \
            'Supersnel, supercompleet en supercool - superlatieven ' \
            'schieten tekort om Trackmania Turbo te beschrijven. Het spel ' \
            'is makkelijk op te pikken maar blijft uitdagingen bieden. De ' \
            'vele multiplayermogelijkheden zorgen ervoor dat de game lang ' \
            'leuk blijft. \n' \
            'Trackmania Turbo bevindt zich op het snijpunt tussen ' \
            'bikkelharde competitie en puur plezier.\xa0Pc-gamers die de ' \
            'eerdere versies van Trackmania hebben gespeeld wisten dat ' \
            'allang, maar met dit consoledebuut van Trackmania maken ' \
            'ook PlayStation 4- en Xbox One-bezitters kennis met de ' \
            'bijzondere snelle gamereeks.\n' \
            'Simpel gezegd draait Trackmania om weinig anders dan zo ' \
            'snel mogelijke tijden noteren. In de praktijk dien je ' \
            'daarvoor extreme hindernissen op de circuits te bedwingen: ' \
            'reuzensprongen, loopings en halfpipes, maar ook onverharde ' \
            'paden, plotselinge tempowisselingen en eindeloos ' \
            'doordraaiende bochtencombinaties.\xa0\n' \
            'Je kunt het zo gek niet bedenken of je komt het tegen in de ' \
            'tweehonderd verschillende parcoursen (veelal van A naar B, ' \
            'maar ook circuits die rondlopen) die worden meegeleverd.\n' \
            'De game bevat vier kleurrijke thema\'s: de geasfalteerde ' \
            'woestenij van Canyon Grand Drift, de modderpaden van Valley ' \
            'Down & Dirty, het exotische Rollercoaster Lagoon en het ' \
            'sensationele International Stadium.\xa0In elke omgeving ' \
            'gebruik je een specifieke auto, die je slechts beperkt ' \
            'naar eigen smaak kunt aanpassen met verschillende kleurtjes ' \
            'en logo\'s.\n' \
            'Stuurmanskunst\n' \
            'Je input is in de basis beperkt tot gas geven, remmen en ' \
            'een gevoelig stuur. Belangrijker nog is je racelijn over ' \
            'elk parcours: neem je meer snelheid mee over een schans, ' \
            'of rem je eerst even af om beter uit te komen voor de ' \
            'daaropvolgende bocht? Ook kun je vloeiend door bochten ' \
            'driften.\xa0\n' \
            'Uiteindelijk komt het allemaal aan op je eigen vaardigheden: ' \
            'geen powerups, maar pure stuurmanskunst \u2013 al kun je met ' \
            'genoeg vindingrijkheid ook mooie stukken afsnijden.\n' \
            'Lukt het een keer niet, dan kun je met een druk op de knop ' \
            'zonder vertraging opnieuw starten. Dat houdt het tempo erin ' \
            'wanneer je om medailles strijdt in de hoofdmodus, of als ' \
            'je vrienden probeert te verslaan nadat ze je een uitdaging ' \
            'hebben gestuurd.\n' \
            'Multiplayer\n' \
            'Trackmania staat niet voor niets al jaren hoog ' \
            'aangeschreven binnen de eSports-wereld. De ontwikkelaars ' \
            'hebben een online multiplayerstand gebouwd waarin maar ' \
            'liefst honderd spelers het tegelijkertijd tegen elkaar ' \
            'kunnen opnemen.\n' \
            'In de praktijk betekent dat dat je maximaal 99 anderen ' \
            'als spoken over de baan ziet gaan, om te voorkomen dat je ' \
            'elkaar in de weg zit op jacht naar een perfecte run.\xa0\n' \
            'Dat klinkt misschien minder spannend, maar in de praktijk ' \
            'werkt het erg motiverend om jezelf tijdens een potje direct ' \
            'en constant te kunnen meten met een groot aantal ' \
            'tegenstanders. Bovendien wordt je positie op de ' \
            'internationale, nationale en zelfs regionale ranglijst ' \
            'constant bijgehouden, waardoor de snelheidsstrijd lang ' \
            'kan aanhouden.\n' \
            'Double Driver\n' \
            'Ook op lokaal niveau is er genoeg competitie mogelijk. ' \
            'Maximaal zestien spelers kunnen het \xe9\xe9n voor ' \
            '\xe9\xe9n tegen elkaar opnemen, of je kunt met maximaal ' \
            'vier man op een gedeeld scherm racen -\xa0een functie\xa0die ' \
            'we binnen dit genre nog maar weinig zien.\xa0\n' \
            'Nog origineler is de Double Driver-stand, waarin je met twee ' \
            'spelers \xe9\xe9n auto bestuurt. De auto luistert in deze ' \
            'stand naar de besturing van beide chauffeurs en voert het ' \
            '\u2018gemiddelde\u2019 uit.\n' \
            'Om de gekkigheid compleet te maken, is er een veelvoud aan ' \
            'speciale standen te kiezen door \'geheime\' toetsencombinaties ' \
            'in te voeren. Zo kun je plots in een Mario Kart-achtige race ' \
            'm\xe9t power-ups terechtkomen of alle spelers verplichten ' \
            'binnen het scherm van de snelste te blijven.\n' \
            'Bouwen\n' \
            'Er is ook een uitgebreide modus om je eigen circuits op te ' \
            'bouwen. De mogelijkheden zijn dusdanig uitgebreid dat we maar ' \
            'wat blij zijn dat de game je ze op verschillende niveaus laat ' \
            'benutten: instappers kunnen met plezier aan de slag en een ' \
            'baantje in elkaar knutselen, terwijl diehards uit hun dak ' \
            'kunnen met de meest knotsgekke creaties.\xa0\n' \
            'Ook de functie die willekeurig een circuit genereert werkt ' \
            'goed. Je kunt alle banen online delen en via een website ' \
            'toevoegen aan je favorietenlijst, waarna ze gemakkelijk te ' \
            'selecteren zijn voor een potje.\n' \
            'Uiterlijk\n' \
            'Bij de combinatie van al die verschillende ' \
            'gameplaymogelijkheden past de kleurrijke, frisse en coole ' \
            'audiovisuele stijl, die de arcade-insteek van Trackmania ' \
            'Turbo onderstreept.\n' \
            'Blauwe luchten, grote neonreclameborden, zeppelins en ' \
            'retro-lettertypes vormen -\xa0in samenwerking met het ' \
            'rijgedrag -\xa0een dikke knipoog richting de hoogtijdagen ' \
            'van OutRun, Daytona USA en Ridge Racer.\xa0\n' \
            'De pompende electromuziek is een perfecte match, al is ' \
            'het wat jammer dat er telkens een nieuw nummer wordt ' \
            'ingestart wanneer je een nieuwe run begint. Voor de ' \
            'techniek vooral respect: de framerate van de ' \
            'PlayStation 4-versie (met een resolutie van 1080p) is ' \
            'nagenoeg rotsvast, de Xbox One-versie (in 900p) kent iets ' \
            'meer (kleine) haperingen.\n' \
            'Conclusie\n' \
            'De kwaliteiten van Trackmania waren racefans op zich ' \
            'al bekend. Maar het is juist de uitvoering in de vorm ' \
            'van Trackmania Turbo, nota bene als debuut op de ' \
            'spelcomputers van Sony en Microsoft, waar we heel erg ' \
            'blij van kunnen worden.\n' \
            'Dit is niet alleen een razendsnelle, uitdagende en ' \
            'zeer complete arcaderacer, maar ook een flitsend en ' \
            'levendig eerbetoon aan de kunst van zo hard mogelijk gaan.\n' \
            'Razendsnelle gameplay\n' \
            'Zowel toegankelijk als uitdagend\n' \
            'Veel multiplayermodi\n' \
            'Uitgebreide circuitbouwer\n' \
            'Kleine audiovisuele problemen\n' \
            'BEOORDELING\n' \
            'Trackmania Turbo is vanaf donderdag beschikbaar voor ' \
            'PlayStation 4, Xbox One en pc. Voor deze review zijn ' \
            'enkel de consoleversies gespeeld.\n'

        self.assertEqual(parsed_article.get('content'), expected)

        expected_date = self.timezone.localize(datetime(2016, 3, 24, 12, 15))
        self.assertEqual(parsed_article.get('date'), expected_date)

    def test_nu_nl_algemeen(self):
        """
        www_nu_nl_algemeen_4225459_automobilisten-krijgen-last-van-gladheid-en-mist.html
        """

        article_name = 'www_nu_nl_algemeen_4225459_automobilisten-krijgen-' \
                       'last-van-gladheid-en-mist.html'
        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = NuNLParser.parse_new_version('', article_file.read())

        expected = \
            'Automobilisten krijgen zaterdagavond en -nacht weer te maken met ' \
            'gladheid \n' \
            'Tijdens opklaringen kunnen natte wegen bevriezen. Vooral in ' \
            'het midden, oosten en noorden van het land kan mist ontstaan. ' \
            'Lokaal is er kans op dichte mist met minder dan 200 ' \
            'meter zicht.\n' \
            'Later in de nacht raakt het in het westen en zuiden van ' \
            'Nederland bewolkt en volgt er regen of iets verder ' \
            'landinwaarts natte sneeuw. "Ook in de rest van het land ' \
            'is richting de ochtend een beetje regen of een vlokje ' \
            '(natte) sneeuw niet uitgesloten. In combinatie met ' \
            'wegdektemperaturen onder nul kan het dan verraderlijk ' \
            'glad worden", aldus Weeronline.\n' \
            'Zondag overdag breiden bewolking en neerslag zich verder ' \
            'uit over het hele land. Vooral in de middag wordt er ' \
            'regen verwacht, met in het binnenland ook natte sneeuw.\n'

        self.assertEqual(parsed_article.get('content'), expected)

        expected_date = self.timezone.localize(datetime(2016, 3, 5, 17, 4))
        self.assertEqual(parsed_article.get('date'), expected_date)
