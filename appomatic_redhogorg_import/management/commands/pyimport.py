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
                published = datetime.datetime(1970, 1, 1)

            license_url = data.get('license_url', '')
            if '://' not in license_url: license_url = None

            license = None
            if license_url:
                licenses = appomatic_redhogorg_data.models.License.objects.filter(url = license_url)
                if licenses:
                    license = licenses[0]
                else:
                    license = appomatic_redhogorg_data.models.License(url = license_url, name = data['license'])
                    license.save()
            
            projects = appomatic_redhogorg_data.models.Project.objects.filter(title = data['name'])
            if projects:
                project = projects[0]
                project.content = data['short_description'],
                project.license = license,
                project.published = published
            else:
                project = appomatic_redhogorg_data.models.Project(
                    source = self.source,
                    url = "/Projects/" + data['name'],
                    content = data['short_description'],
                    title = data['name'],
                    license = license,
                    published = published)
            project.save()
            project.tags.add(self.add_tag("Software"))

    def handle2(self, path, *args, **options):
        self.importroot = path
        self.set_source(self.importroot)
        self.add(path)
