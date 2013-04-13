import django.db
import django.core.management.base
import appomatic_redhogorg_data.models
import optparse
import contextlib
import datetime
import os.path
import datetime
from django.conf import settings

class ImportCommand(django.core.management.base.BaseCommand):
    TOOLNAME = 'import'

    def add_tag(self, path):
        tag = None
        for item in path.split("/"):
            tags = appomatic_redhogorg_data.models.Tag.objects.filter(name = item, parent = tag)
            if len(tags):
                tag = tags[0]
            else:
                tag = appomatic_redhogorg_data.models.Tag(name = item, parent = tag)
                tag.save()
        return tag

    def set_source(self, argument):
        sources = appomatic_redhogorg_data.models.Source.objects.filter(tool=self.TOOLNAME, argument = argument)
        if len(sources):
            self.source = sources[0]
        else:
            self.source = appomatic_redhogorg_data.models.Source(
                tool=self.TOOLNAME,
                argument = argument)
            self.source.save()

    def handle(self, *args, **options):
        try:
            return self.handle2(*args, **options)
        except Exception, e:
            print type(e), e
            import traceback
            traceback.print_exc()
            raise
