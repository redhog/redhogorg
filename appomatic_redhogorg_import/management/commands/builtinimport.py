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
    TOOLNAME = "builtinimport"
    help = '"Imports" the builtin elements'
    args = '<path>'

    def add(self):
        for (url, subtype, title) in (("/mainmenu", "MainMenu", "Main menu"),
                                      ("/badge/facebook", "Badge/FaceBook", "FaceBook badge"),
                                      ("/badge/github", "Badge/GitHub", "GitHub badge"),
                                      ("/badge/twitter", "Badge/Twitter", "Twitter badge"),
                                      ):

            project = appomatic_redhogorg_data.models.StaticTemplate(
                source = self.source,
                author = self.user,
                license = self.license,
                url = url,
                title = title,
                published = None,
                render_subtype = subtype
                ).save()

        for (url, title, items) in (("/sidebar/left", "Left sidebar", ("/mainmenu", "/badge/facebook")),
                                    ("/sidebar/right", "Left sidebar", ("/badge/github", "/badge/twitter"))):

            collection = appomatic_redhogorg_data.models.ListCollection(
                source = self.source,
                author = self.user,
                license = self.license,
                url = url,
                title = title,
                published = None)
            collection.save()
            for ordering, item in enumerate(items):
                appomatic_redhogorg_data.models.ListCollectionMember(
                    collection = collection,
                    node = appomatic_redhogorg_data.models.Node.objects.get(url=item),
                    ordering = ordering).save()

    def handle2(self, *args, **options):
        self.set_source("builtin")
        self.add()
