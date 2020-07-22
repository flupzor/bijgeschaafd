from datetime import datetime

from django.test import TestCase

from pytz import timezone

from ..dateparsers import (
    MetroDateParser, NosNLDateParser, NuNLDateParser, TelegraafDateParser
)


class DateParserTests(TestCase):
    def setUp(self):
        super(DateParserTests, self).setUp()
        self.amsterdam = timezone("Europe/Amsterdam")

    def test_metro(self):
        self.assertEquals(
            MetroDateParser.process("10 maart 2016 om 16:54"),
            self.amsterdam.localize(datetime(2016, 3, 10, 16, 54))
        )

        self.assertEquals(
            MetroDateParser.process("9 maart 2016 om 07:59"),
            self.amsterdam.localize(datetime(2016, 3, 9, 7, 59))
        )

    def test_telegraaf(self):
        self.assertEquals(
            TelegraafDateParser.process("za 02 jan 2016, 08:08"),
            self.amsterdam.localize(datetime(2016, 1, 2, 8, 8))
        )

        self.assertEquals(
            TelegraafDateParser.process("do 30 jun 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 6, 30, 23, 59))
        )

        # Make sure all months are parsed properly.
        self.assertEquals(
            TelegraafDateParser.process("ma 04 jan 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 1, 4, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 08 feb 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 2, 8, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 07 mrt 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 3, 7, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 04 apr 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 4, 4, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 02 mei 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 5, 2, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 06 jun 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 6, 6, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 04 jul 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 7, 4, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 01 aug 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 8, 1, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 05 sep 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 9, 5, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 03 okt 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 10, 3, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 07 nov 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 11, 7, 23, 59))
        )

        self.assertEquals(
            TelegraafDateParser.process("ma 05 dec 2016, 23:59"),
            self.amsterdam.localize(datetime(2016, 12, 5, 23, 59))
        )

    def test_nu_nl(self):
        self.assertEquals(
            NuNLDateParser.process("01-01-16 10:35"),
            self.amsterdam.localize(datetime(2016, 1, 1, 10, 35))
        )

    def test_nos_nl(self):
        self.assertEquals(
            NosNLDateParser.process("2016-01-02T08:58:39+0100"),
            self.amsterdam.localize(datetime(2016, 1, 2, 8, 58, 39))
        )

        self.assertEquals(
            NosNLDateParser.process("2016-06-30T23:59:00+0200"),
            self.amsterdam.localize(datetime(2016, 6, 30, 23, 59, 0))
        )

        with self.assertRaises(ValueError) as context:
            NosNLDateParser.process("2016-06-30T23:59:00+0300"),

        self.assertEquals(
            'The given timezone was: +0300, while the timezone '
            'expected was: +0200',
            str(context.exception)
        )

        with self.assertRaises(ValueError) as context:
            NosNLDateParser.process("2016-06-31T23:59:00+0200"),

        self.assertEquals(
            'day is out of range for month',
            str(context.exception)
        )
