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
                row['source'] = self.source
                row['author'] = self.user
                row['license'] = self.license
                row['content'] = row['body']
                row['published'] = datetime.datetime.utcfromtimestamp(int(row['timestamp']))
                row['url'] = "/" + row['url']

                article = self.upsert(
                    appomatic_redhogorg_data.models.Article,
                    "url",
                    **row)
                article.tags.add(self.add_tag(row['category']))
