import django.db
import django.core.management.base
import appomatic_redhogorg_data.models
import optparse
import contextlib
import datetime
import feedparser
import os.path
import django.template.defaultfilters
import appomatic_redhogorg_import.baseimport

def dictreader(cur):
    for row in cur:
        yield dict(zip([col[0] for col in cur.description], row))

def csvdictreader(c):
    header = [col.decode('latin-1') for col in c.next()]
    for row in c:
        yield dict(zip(header, (col.decode('latin-1') for col in row)))

class Command(appomatic_redhogorg_import.baseimport.ImportCommand):
    TOOLNAME = "articlerssimort"
    help = 'Imports articles from csv'
    args = '<filename>'

    def handle2(self, filename, *args, **options):
        self.set_source(filename)
        for entry in feedparser.parse(filename).entries:
            article = self.upsert(
                appomatic_redhogorg_data.models.Article,
                "url",
                url = '/blog/' + django.template.defaultfilters.slugify(entry.title),
                source = self.source,
                author = self.user,
                license = self.license,
                title = entry.title,
                content = entry.description,
                published = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z"))
            for tag in entry.tags:
                article.tags.add(self.add_tag(tag.term))
