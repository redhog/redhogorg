import django.db
import django.core.management.base
import appomatic_redhogorg_data.models
import optparse
import contextlib
import datetime
import csv
import os.path
import datetime
import appomatic_redhogorg_import.baseimport

def dictreader(cur):
    for row in cur:
        yield dict(zip([col[0] for col in cur.description], row))

def csvdictreader(c):
    header = [col.decode('latin-1') for col in c.next()]
    for row in c:
        yield dict(zip(header, (col.decode('latin-1') for col in row)))

class Command(appomatic_redhogorg_import.baseimport.ImportCommand):
    TOOLNAME = "articlecsvimport"
    help = 'Imports articles from csv'
    args = '<filename>'

    def handle2(self, filename, *args, **options):
        self.set_source(filename)
        with open(filename) as f:
            for row in csvdictreader(csv.reader(f)):
                articles = appomatic_redhogorg_data.models.Article.objects.filter(url = row['url'])
                if len(articles):
                    article = articles[0]
                else:
                    article = appomatic_redhogorg_data.models.Article(
                        source = self.source,
                        url = row['url'],
                        title = row['title'],
                        content = row['body'],
                        published = datetime.datetime.utcfromtimestamp(int(row['timestamp'])))
                    article.save()
                article.tags.add(self.add_tag(row['category']))
