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

    def set_license(self, name = "GPL", url = "http://www.gnu.org/copyleft/gpl.html"):
        licenses = appomatic_redhogorg_data.models.License.objects.filter(name = name)
        if len(licenses):
            self.license = licenses[0]
        else:
            self.license = appomatic_redhogorg_data.models.License(name = name, url = url)
            self.license.save()

    def set_user(self):
        users = django.contrib.auth.models.User.objects.filter(username = "redhog")
        if len(users):
            self.user = users[0]
        else:
            self.user = django.contrib.auth.models.User(username = "redhog")
            self.user.save()

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
