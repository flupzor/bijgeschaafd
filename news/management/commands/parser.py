from django.core.management.base import BaseCommand

from news import parsers


class Command(BaseCommand):
    help = 'Parse a specific website'

    def add_arguments(self, parser):
        parser.add_argument('parser', nargs='?', type=unicode)
        parser.add_argument('url', nargs='?', type=unicode)

    def handle(self, *args, **options):

        if options['parser'] is None and options['url'] is None:
            self.stdout.write("Available parsers")
            for parser_name in parsers.parser_dict.keys():
                self.stdout.write(parser_name)
        elif options['parser'] is not None and options['url'] is None:
            parser = parsers.parser_dict[options['parser']]
            urls = parser.feed_urls()

            for url in urls:
                self.stdout.write(url)
        elif options['parser'] is not None and options['url'] is not None:
            parser = parsers.parser_dict[options['parser']]

            parsed_article = parser(options['url'])

            self.stdout.write(unicode(parsed_article))
