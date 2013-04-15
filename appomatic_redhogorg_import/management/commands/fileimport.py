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
import magic

def importfile(self, path, save=True):
    self.name = path
    setattr(self.instance, self.field.name, self.name)

    # Update the filesize cache
    with self.storage.open(path) as content:
        self._size = content.size
    self._committed = True

    # Save the object because it has changed, unless save is False
    if save:
        self.instance.save()
importfile.alters_data = True
django.db.models.fields.files.FieldFile.importfile = importfile

class Command(appomatic_redhogorg_import.baseimport.ImportCommand):
    TOOLNAME = "fileimport"
    help = 'Imports a directory of files. The files must reside under %s' % settings.MEDIA_ROOT
    args = '<path>'

    def remove(self):
        for file in appomatic_redhogorg_data.models.File.objects.filter(source = self.source):
            try:
                file.content.open()
                file.content.close()
            except:
                print "DELETE", file.title
                file.delete()
        for image in appomatic_redhogorg_data.models.Image.objects.filter(source = self.source):
            try:
                image.content.open()
                image.content.close()
            except:
                print "DELETE", file.title
                image.delete()


    def add(self, path):
        print path
        if os.path.isdir(path):
            for name in os.listdir(path):
                self.add(os.path.join(path, name))
        elif not path.endswith(".__info__.py"):
            mime = magic.from_file(path, mime=True)

            localpath = path[len(self.importroot):]
            
            # Normalize the path to be under MEDIA_ROOT regardless of confusing symlinks...
            path = os.path.realpath(path)
            root = os.path.realpath(settings.MEDIA_ROOT)
            mediapath = path[len(root) + 1:]

            filename = os.path.basename(path)
            title = os.path.splitext(filename)[0]

            if (mime.startswith('image/png') or
                mime.startswith('image/gif') or
                mime.startswith('image/jpeg') or
                mime.startswith('image/bmp') or
                mime.startswith('image/x-windows-bmp') or
                mime.startswith('image/svg')):
                File = appomatic_redhogorg_data.models.Image
            else:
                File = appomatic_redhogorg_data.models.File

            infopath = path + ".__info__.py"
            info = {
                "source": self.source,
                "author": self.user,
                "license": self.license,
                "url": localpath,
                "title": title}

            if os.path.exists(infopath):
                data = {}
                execfile(infopath, data)
                for key in ('title', 'description'):
                    if key in data:
                        info[key] = data[key]

            files = File.objects.filter(url = localpath)
            if len(files):
                file = files[0]
                for key, value in info.iteritems():
                    setattr(file, key, value)
            else:
                info["published"] = None
                file = File(**info)
                file.content.importfile(mediapath)
                file.save()

            tag = localpath.split('/')[1:-1]
            if tag:
                file.tags.add(self.add_tag('/'.join(tag)))

    def handle2(self, path, *args, **options):
        self.importroot = path
        if self.importroot.endswith('/'): self.importroot = self.importroot[:-1]

        self.set_source(self.importroot)
        with django.db.transaction.commit_on_success():
            self.remove()
            self.add(path)
