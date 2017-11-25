from datetime import datetime

import pytz


class DateParser(object):
    def __init__(self, source):
        self.source = source
        self.index = 0
        self.size = -1  # TODO: Raise error.

    def _position(self, size):
        if size == 1:
            return "{}".format(self.index + 1)

        return "{}-{}".format(self.index + 1, self.index + size)

    def parse_number(self, size, min_size=0):
        """
        Parse a variable-sized number.
        """

        while size > min_size:
            number = self.source[self.index:+self.index+size]
            if number.isdigit():
                self.index += size
                return int(number)
            size -= 1

        raise ValueError("No variable sized number found.")

    def parse_from_dict(self, size, mapping, min_size=0):
        while size > min_size:
            key = self.source[self.index:self.index+size]

            if key in mapping:
                value = mapping[key]
                self.index += size

                return value
            size -= 1

        raise ValueError(
            "{} on position {} not one of {}".format(
                key, self._position(size), ",".join(mapping.keys())))

    def assert_string(self, expected_string):
        size = len(expected_string)

        found_string = self.source[self.index:self.index + size]

        if found_string != expected_string:
            raise ValueError(
                "Found the string '{}' but expected the string '{}'"
                " on position {}".format(
                    found_string, expected_string, self._position(size)
                )
            )
        self.index += size

    def parse(self):
        return self._parse()

    @classmethod
    def process(cls, source):
        parser = cls(source)
        return parser.parse()


class NosNLDateParser(DateParser):
    def __init__(self, source):
        self.source = source
        self.index = 0
        self.size = 24
        self.timezone = pytz.timezone("Europe/Amsterdam")

    def _parse(self):
        year = self.parse_number(4)
        self.assert_string("-")
        month = self.parse_number(2)
        self.assert_string("-")
        day = self.parse_number(2)
        self.assert_string("T")
        hour = self.parse_number(2)
        self.assert_string(":")
        minute = self.parse_number(2)
        self.assert_string(":")
        second = self.parse_number(2)
        self.assert_string("+")
        timezone = self.parse_number(4)

        result = self.timezone.localize(
            datetime(year, month, day, hour, minute, second))
        expected_timezone = result.strftime("%z")
        given_timezone = "+{0:04d}".format(timezone)

        # TODO: For now just make sure the given timezone is
        # equal to the one we localize the datetime with.
        if given_timezone != expected_timezone:
            raise ValueError(
                "The given timezone was: {}, while the "
                "timezone expected was: {}".format(
                    given_timezone, expected_timezone))

        return result


class NuNLDateParser(DateParser):
    def __init__(self, source):
        self.source = source
        self.index = 0
        self.size = 14
        self.timezone = pytz.timezone("Europe/Amsterdam")

    def _parse(self):
        # 01-01-16 10:35

        day = self.parse_number(2)
        self.assert_string("-")
        month = self.parse_number(2)
        self.assert_string("-")
        year = self.parse_number(2) + 2000
        self.assert_string(" ")
        hour = self.parse_number(2)
        self.assert_string(":")
        minute = self.parse_number(2)

        return self.timezone.localize(datetime(year, month, day, hour, minute))


class TelegraafDateParser(DateParser):
    day_of_week_mapping = {
        'ma': 1, 'di': 2,
        'wo': 3, 'do': 4,
        'vr': 5, 'za': 6,
        'zo': 7
    }
    month_mapping = {
        'jan': 1, 'feb': 2,
        'mrt': 3, 'apr': 4,
        'mei': 5, 'jun': 6,
        'jul': 7, 'aug': 8,
        'sep': 9, 'okt': 10,
        'nov': 11, 'dec': 12,
    }

    def __init__(self, source):
        self.source = source
        self.index = 0
        self.size = 21
        self.timezone = pytz.timezone("Europe/Amsterdam")

    def _parse(self):
        self.parse_from_dict(2, self.day_of_week_mapping)
        self.assert_string(" ")
        day = self.parse_number(2)
        self.assert_string(" ")
        month = self.parse_from_dict(3, self.month_mapping)
        self.assert_string(" ")
        year = self.parse_number(4)
        self.assert_string(", ")
        hour = self.parse_number(2)
        self.assert_string(":")
        minute = self.parse_number(2)

        return self.timezone.localize(datetime(year, month, day, hour, minute))


class MetroDateParser(DateParser):
    # 10 maart 2016 om 16:54
    month_mapping = {
        'januari': 1, 'februari': 2,
        'maart': 3, 'april': 4,
        'mei': 5, 'juni': 6,
        'juli': 7, 'augustus': 8,
        'september': 9, 'oktober': 10,
        'november': 11, 'december': 12,
    }

    def __init__(self, source):
        self.source = source
        self.index = 0
        self.timezone = pytz.timezone("Europe/Amsterdam")

    def _parse(self):
        day = self.parse_number(2)
        self.assert_string(" ")
        month = self.parse_from_dict(7, self.month_mapping)
        self.assert_string(" ")
        year = self.parse_number(4)
        self.assert_string(" om ")
        hour = self.parse_number(2)
        self.assert_string(":")
        minute = self.parse_number(2)

        return self.timezone.localize(datetime(year, month, day, hour, minute))
