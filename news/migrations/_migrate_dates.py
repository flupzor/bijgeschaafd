from news.dateparsers import (
    NosNLDateParser, NuNLDateParser, TelegraafDateParser, MetroDateParser)


def migrate_dates(apps, schema_editor, source):
    date_parser_mapping = {
        'nos.nl': NosNLDateParser,
        'nu.nl': NuNLDateParser,
        'telegraaf.nl': TelegraafDateParser,
        'metronieuws.nl': MetroDateParser
    }

    Version = apps.get_model("news", "Version")

    versions = Version.objects.filter(article__source=source)
    total = versions.count()
    failures = 0
    for version in versions:
        parser = date_parser_mapping[version.article.source]

        content = version.content
        try:
            newline_position = content.find('\n')
            firstline = content[:newline_position]
        except Exception:
            pass

        try:
            # Store the date as a datetime in the database.
            version.modified_date_in_article = \
                parser.process(firstline)
            # Remove the date in the content.
            version.content = version.content[newline_position+1:]
            version.save(update_fields=['modified_date_in_article', 'content'])
        except ValueError:
            failures += 1

#    print "Failures {}/{}".format(failures, total)
