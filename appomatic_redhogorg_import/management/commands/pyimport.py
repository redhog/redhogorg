import django.db
import django.core.management.base
import appomatic_redhogorg_data.models
import optparse
import contextlib
import datetime
import os.path
import datetime
from django.conf import settings
import django.core.files.storage
import django.db.models.fields.files
import appomatic_redhogorg_import.baseimport
import codecs
import markdown
import git

class Command(appomatic_redhogorg_import.baseimport.ImportCommand):
    TOOLNAME = "pyimport"
    help = 'Imports a directory of projects described by python files'
    args = '<path>'

    def add(self, path):
        for name in os.listdir(path):
            if not name.endswith('.py'): continue
            data = {}
            execfile(os.path.join(path, name), data)

            try:
                published = datetime.datetime(int((data.get('copyright_years', '') or '').split("-")[-1]), 1, 1)
            except:
                published = None

            if 'license' in data and 'license_url' in data and '://' in data['license_url']:
                self.set_license(data['license'], data['license_url'])
            
            project = self.upsert(
                appomatic_redhogorg_data.models.Project,
                "title",
                source = self.source,
                author = self.user,
                license = self.license,
                url = "/Projects/" + data['name'],
                content = data['short_description'],
                title = data['name'],
                published = published)
            project.tags.add(self.add_tag("Software"))

    def handle2(self, path, *args, **options):
        self.importroot = path
        self.set_source(self.importroot)
        self.add(path)
