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
    TOOLNAME = "gitimport"
    help = 'Imports a directory of git repositories. The directory must reside under %s' % settings.MEDIA_ROOT
    args = '<path>'

    def add(self, path):
        for name in os.listdir(path):
            repopath = os.path.join(path, name)
            content = ''
            for readme in ("README.md", "readme.md", "README.txt", "readme.txt", "README", "readme"):
                readme = os.path.join(repopath, readme)
                if os.path.exists(readme):
                    with codecs.open(readme, mode="r", encoding="utf-8") as f:
                        content = f.read()
                    if readme.lower().endswith(".md"):
                        content = markdown.markdown(content)
                    break

            repo = git.Repo(repopath)
            assert repo.bare == False

            remote = repo.remotes.origin.url

            if 'github.com/' not in remote:
                print "IGNORING %s (%s not a github repo)" % (name, remote)

            remote = remote.split("github.com")[1][1:] # Remove everything before github.com/ or github.com:
            remote = remote.split("/")

            username = remote[0]

            if remote[1] != name + ".git":
                print "IGNORING %s (remote name %s not same as local name)" % (name, remote[1])

            project = appomatic_redhogorg_data.models.Project(
                source = self.source,
                url = "/" + name,
                content = content,
                title = name,
                repository_name = name,
                github_username = username,
                published = datetime.datetime.now())
            project.save()
            project.tags.add(self.add_tag("Software"))

    def handle2(self, path, *args, **options):
        self.importroot = path
        if self.importroot.endswith('/'): self.importroot = self.importroot[:-1]

        self.set_source(self.importroot)
        self.add(path)
