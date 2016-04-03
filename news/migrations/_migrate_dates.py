from news.dateparsers import (
    NosNLDateParser, NuNLDateParser, TelegraafDateParser, MetroDateParser)


# Copied from: https://djangosnippets.org/snippets/1170/
def batch_qs(qs, batch_size=1000):
    """
    Returns a (start, end, total, queryset) tuple for each batch in the given
    queryset.

    Usage:
        # Make sure to order your querset
        article_qs = Article.objects.order_by('id')
        for start, end, total, qs in batch_qs(article_qs):
            print "Now processing %s - %s of %s" % (start + 1, end, total)
            for article in qs:
                print article.body
    """
    total = qs.count()
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        yield (start, end, total, qs[start:end])


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
    for start, end, total, qs in batch_qs(versions):
        print "Now processing %s - %s of %s" % (start + 1, end, total)

        for version in qs:
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
