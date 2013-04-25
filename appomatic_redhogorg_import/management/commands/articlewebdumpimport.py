import django.db
import django.core.management.base
import appomatic_redhogorg_data.models
import optparse
import contextlib
import datetime
import os.path
import django.template.defaultfilters
import appomatic_redhogorg_import.baseimport
import lxml.html.soupparser

def dictreader(cur):
    for row in cur:
        yield dict(zip([col[0] for col in cur.description], row))

def csvdictreader(c):
    header = [col.decode('latin-1') for col in c.next()]
    for row in c:
        yield dict(zip(header, (col.decode('latin-1') for col in row)))

def tostring(s):
    if isinstance(s, lxml.html.HtmlElement):
        return lxml.html.tostring(s)
    return unicode(s)


class Command(appomatic_redhogorg_import.baseimport.ImportCommand):
    TOOLNAME = "articlewebdumpimport"
    help = 'Imports articles from old blog'
    args = '<filename>'

    def handle2(self, filename, *args, **options):
        self.set_source(filename)
        with open(filename) as f:
            data = f.read()
        
        data = lxml.html.soupparser.fromstring(data)
        content = data.xpath("//div[@id='content']")[0]

        date = None
        for entry in content.xpath("*"):
            if entry.tag == 'h2':
                month, day, year = [int(item.lstrip("0")) for item in entry.text.split("/")]
                date = datetime.datetime(year, month, day)
            else:
                title = entry.xpath("h3//text()")[0]
                categories = entry.xpath(".//*[@class='post-categories']//li//text()")

                authorinfo = entry.xpath(".//*[@class='meta']/text()")[1]
                authorinfo = authorinfo.split(u' \u2014')[1]
                author, time = authorinfo.split("@")
                author = author.strip()
                time = time.strip()
                time = datetime.datetime.strptime(date.strftime("%Y-%m-%d") + " " + time, "%Y-%m-%d %H:%M:%S")
                
                content = ''.join(tostring(x) for x in entry.xpath(".//*[@class='storycontent']/node()"))

                self.set_user(author)

                article = self.upsert(
                    appomatic_redhogorg_data.models.Article,
                    "url",
                    url = '/blog/' + django.template.defaultfilters.slugify(title),
                    source = self.source,
                    author = self.user,
                    license = self.license,
                    title = title,
                    content = content,
                    published = time)

                for tag in categories:
                    article.tags.add(self.add_tag("Personal/Dagbok/Australien/" + tag))
