import django.db
import django.core.management.base
import appomatic_redhogorg_data.models
import optparse
import contextlib
import datetime
import os.path
import datetime
from django.conf import settings
import django.contrib.auth.models

class ImportCommand(django.core.management.base.BaseCommand):
    TOOLNAME = 'import'

    def upsert(self, Model, *keys, **args):
        lookup = dict((key, args[key])
                      for key in keys)
        objs = Model.objects.filter(**lookup)
        if len(objs):
            obj = objs[0]
        else:
            print "CREATE", lookup
            obj = Model()
        for name, value in args.iteritems():
            setattr(obj, name, value)
        obj.save()
        return obj

    def add_tag(self, path):
        tag = None
        for item in path.split("/"):
            tag = self.upsert(appomatic_redhogorg_data.models.Tag, "name", "parent", name = item, parent = tag)
        return tag

    def set_source(self, argument):
        self.source = self.upsert(appomatic_redhogorg_data.models.Source, "tool", "argument", tool=self.TOOLNAME, argument = argument)

    def set_license(self, name = "GPL", url = "http://www.gnu.org/copyleft/gpl.html"):
        self.license = self.upsert(appomatic_redhogorg_data.models.License, "name", name=name, url=url)

    def set_user(self, username = 'redhog'):
        self.user = self.upsert(django.contrib.auth.models.User, "username", username = username)

    def handle(self, *args, **options):
        try:
            self.set_user()
            self.set_license()
            return self.handle2(*args, **options)
        except Exception, e:
            print type(e), e
            import traceback
            traceback.print_exc()
            raise
