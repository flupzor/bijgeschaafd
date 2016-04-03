from django.test import TestCase, override_settings

import os
from django.utils._os import upath

from ..telegraaf import TelegraafParser
import responses


TEST_DIR = os.path.join(os.path.dirname(upath(__file__)), 'data')


class TelegraafParserTests(TestCase):
    maxDiff = None

    @responses.activate
    @override_settings(NEWS_SOURCES=['news.parsers.telegraaf.TelegraafParser', ])
    def test_telegraaf_nl_urls(self):
        page_name = 'www_telegraaf_nl'
        page_path = os.path.join(TEST_DIR, page_name)
        page_file = open(page_path, 'rb')

        responses.add(responses.GET, 'http://www.telegraaf.nl',
                      body=page_file.read(), status=200,
                      content_type='text/html')

        urls = TelegraafParser.request_urls()

        expected = set([
        'http://www.telegraaf.nl/buitenland/25430745/__Pelgrims_omgekomen_in_gekantelde_bus__.html',
        'http://www.telegraaf.nl/binnenland/25431391/__Politie_lost_schot_bij_aanhouding_15-jarige__.html',
        'http://www.telegraaf.nl/binnenland/25429044/__Slagter_schrijft_CDA_wet_voor__.html',
        'http://www.telegraaf.nl/binnenland/25429468/__Burgemeester_had_piket__.html',
        'http://www.telegraaf.nl/binnenland/25430774/__Man_vraagt_de_weg_en_wordt_beroofd__.html',
        'http://www.telegraaf.nl/gezondheid/25420741/__Zorgen_om_medicijntekort__.html',
        'http://www.telegraaf.nl/binnenland/25430767/__Bruinvis_aangespoeld__.html',
        'http://www.telegraaf.nl/binnenland/25431248/__Dode_man_in_IJssel_bij_Kampen_gevonden__.html',
        'http://www.telegraaf.nl/binnenland/25430649/__Student_krijgt_11.000_euro_van_HvA__.html',
        'http://www.telegraaf.nl/buitenland/25430128/__Russen_sluiten_aanslag_na_crash__.html',
        'http://www.telegraaf.nl/buitenland/25430759/__Duitser_dreigt_met_bom_in_auto__.html',
        'http://www.telegraaf.nl/buitenland/25429481/__Team_vertrokken_naar_ISS__.html',
        'http://www.telegraaf.nl/buitenland/25430095/__Abdeslam_en_Choukri_uit_ziekenhuis__.html',
        'http://www.telegraaf.nl/buitenland/25430368/__Nederlandse_dj_omgekomen__.html',
        'http://www.telegraaf.nl/binnenland/25430783/__Landelijke_Opschoondag_populair__.html',
        'http://www.telegraaf.nl/buitenland/25430039/__Flydubai_geschokt_na_crash__.html',
        'http://www.telegraaf.nl/buitenland/25430543/__Overvaller_accepteert_salade__.html',
        'http://www.telegraaf.nl/binnenland/25429753/__VD_zoekt_personeel__.html',
        'http://www.telegraaf.nl/binnenland/25426247/__Vrouw_loopt_hersenbloeding_op_bij_verkrachting__.html',
        'http://www.telegraaf.nl/digitaal/25421409/__Apple-medewerkers_dreigen_met_ontslag_om_FBI__.html',
        'http://www.telegraaf.nl/binnenland/25430960/__Opstootjes_bij_AZC-demonstratie_Utrecht__.html',
        'http://www.telegraaf.nl/binnenland/25429297/__Levensreddend_medicijn_te_duur__.html',
        'http://www.telegraaf.nl/watuzegt/25413635/__Laat_de_Staat_het_ABP_terugbetalen__.html',
        'http://www.telegraaf.nl/buitenland/25428523/__Abdeslam_heeft_mogelijk_advocaat__.html',
        'http://www.telegraaf.nl/binnenland/25430816/__Verkeerde_namen_op_Joods_monument__.html',
        'http://www.telegraaf.nl/buitenland/25430319/__Doden_bij_explosie_in_winkelstraat_Istanbul__.html',
        'http://www.telegraaf.nl/buitenland/25430808/__Abdeslam_wil_niet_naar_Frankrijk__.html',
        'http://www.telegraaf.nl/binnenland/25430489/___Ik_ben_van_plan_heel_oud_te_worden___.html',
        'http://www.telegraaf.nl/buitenland/25430404/__Verse_astronauten_voor_ISS__.html',
        'http://www.telegraaf.nl/gezondheid/25420696/___Kinderen_wachten_te_lang_op_hulp___.html',
        'http://www.telegraaf.nl/binnenland/25430424/__Afvalophaler_in_Breda_opzettelijk_aangereden__.html',
        'http://www.telegraaf.nl/buitenland/25429773/__Hulk_Hogan_krijgt_115_miljoen_in_sekstapezaak__.html',
        'http://www.telegraaf.nl/gezondheid/25425439/__Zo_slecht_is_het_om_nachtenlang_door_te_halen__.html',
        'http://www.telegraaf.nl/digitaal/25422875/___Liefde_op_het_tweede_gezicht__.html',
        'http://www.telegraaf.nl/binnenland/25430762/__Gestolen_trucks_op_terrein__.html',
        'http://www.telegraaf.nl/binnenland/25429148/__Kalfjes_uit_buik_ree_gesneden__.html',
        'http://www.telegraaf.nl/binnenland/25425024/__Opheldering_over_D66-reisje__.html',
        'http://www.telegraaf.nl/binnenland/25429472/__Koe_dood_na_eten_zwerfafval__.html',
        'http://www.telegraaf.nl/gezondheid/25420267/__Duidelijke_grenzen_voor_medische_noodzaak_operatie__.html',
        'http://www.telegraaf.nl/binnenland/25429941/__Dode_door_auto_tegen_boom_Utrecht__.html',
        'http://www.telegraaf.nl/watuzegt/25413661/__Den_Haag__doe_iets_aan_Draghi__.html',
        'http://www.telegraaf.nl/binnenland/25426983/___Brutaal__speels_en_kleurrijk____.html',
        'http://www.telegraaf.nl/binnenland/25431121/__Kuzu_gaat_lijst_van_DENK_aanvoeren__.html',
        'http://www.telegraaf.nl/digitaal/25416646/__Nieuwe_versie_ransomware_is__onkraakbaar___.html',
        'http://www.telegraaf.nl/binnenland/25429765/__Misbruikzaken_in__t_geheim__.html',
        'http://www.telegraaf.nl/binnenland/25425791/__Politie_lost_belofte_in__Johan_krijgt_taart__.html',
        'http://www.telegraaf.nl/dft/25426564/__VD_houdt_laatste_uitverkoop__.html',
        'http://www.telegraaf.nl/watuzegt/25413616/__Pensioenbobo_s__kom_in_actie___.html',
        'http://www.telegraaf.nl/buitenland/25429739/__Vliegtuig_neergestort__.html',
        'http://www.telegraaf.nl/binnenland/25429348/__Terrorist_viel_amper_op__.html',
        'http://www.telegraaf.nl/digitaal/25425694/__Twitter_houdt_limiet_van_140_tekens__.html',
        'http://www.telegraaf.nl/binnenland/25429757/___Voorman_sluist_8_miljoen_weg___.html',
        'http://www.telegraaf.nl/buitenland/25429069/__Gouden_tip_nekte__bangste_terrorist___.html',
        'http://www.telegraaf.nl/digitaal/25421466/__Hoe_kies_je_de_perfecte_tablet___.html',
        'http://www.telegraaf.nl/buitenland/25425792/__Abdeslam_levend_gepakt__.html',
        'http://www.telegraaf.nl/binnenland/25429878/__Ook_tweede_inzittende_dood__.html',
        'http://www.telegraaf.nl/binnenland/25428369/__Felle_reacties_op_Turkije-deal__.html',
        'http://www.telegraaf.nl/binnenland/25429518/__Buschauffeur_overvallen__.html',
        ])

        self.assertEquals(urls, expected)

    def test_telegraaf_buitenland(self):
        """
        http://www.telegraaf.nl/buitenland/24775234/__Dreiging_met_bommen_Belgie__.html
        """
        article_name = 'www_telegraaf_nl_buitenland_24775234_' \
                       '__Dreiging_met_bommen_Belgie__.html'
        article_path = os.path.join(TEST_DIR, article_name)
        article_file = open(article_path, 'rb')

        parsed_article = TelegraafParser.parse_new_version('', article_file.read())

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

        self.assertEquals(parsed_article.get('content'), expected)

        self.assertEquals(parsed_article.get('date'), None)
